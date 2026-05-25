#!/usr/bin/env python3
"""
Test Script - Dual Ranking System
Menampilkan Top 10 BM25 dan Top 10 Cosine Similarity secara terpisah.
Tidak ada combined score / average score.
"""

from rank_bm25 import BM25Okapi
from similarity_calculator import SimilarityCalculator
from abbreviation_expander import AbbreviationExpander
from db_manager import DatabaseManager


def print_header(title):
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def format_score(score, width=6):
    return f"{score:>{width}.2f}"


def build_documents(data_list):
    documents = []
    for item in data_list:
        full_text = f"{item.get('judul', '')} {item.get('isi_berita', '')}"
        expanded_text = AbbreviationExpander.expand_document(full_text)
        documents.append(expanded_text.lower().split())
    return documents


def top_indices(scores, limit=10):
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return [i for i in ranked if scores[i] > 0][:limit]


def print_ranking(title, indices, scores, data_list):
    print(f"\n{title}")
    print(f"{'Rank':<5} {'Score':<8} {'Judul':<70}")
    print('-' * 90)

    if not indices:
        print('Tidak ada hasil.')
        return

    for rank, idx in enumerate(indices, 1):
        doc_title = data_list[idx].get('judul', '')[:68]
        print(f"{rank:<5} {format_score(scores[idx]):<8} {doc_title:<70}")


def test_dual_ranking():
    print_header('DUAL RANKING SYSTEM TEST')

    db = DatabaseManager()
    data = db.load_data()
    if not data or not data.get('data'):
        print('No data found')
        return

    data_list = data.get('data', [])
    documents = build_documents(data_list)

    bm25 = BM25Okapi(documents)
    similarity_calc = SimilarityCalculator(documents)

    test_queries = [
        'universitas indonesia',
        'ranking kampus',
        'jalur masuk ptn',
        'beasiswa pendidikan',
        'ui terbaik',
    ]

    for query in test_queries:
        print_header(f'Query: "{query}"')
        expanded = AbbreviationExpander.expand_query(query)
        query_tokens = expanded.lower().split()
        print(f'Expanded: "{expanded}"')

        bm25_scores = bm25.get_scores(query_tokens)
        cosine_scores = similarity_calc.get_similarities(query_tokens)

        bm25_top = top_indices(bm25_scores, limit=10)
        cosine_top = top_indices(cosine_scores, limit=10)

        print_ranking('TOP 10 BM25', bm25_top, bm25_scores, data_list)
        print_ranking('TOP 10 COSINE SIMILARITY', cosine_top, cosine_scores, data_list)
        print()


def compare_algorithms():
    print_header('ALGORITHM COMPARISON - SEPARATE TOP 10')

    db = DatabaseManager()
    data = db.load_data()
    if not data or not data.get('data'):
        print('No data found')
        return

    data_list = data.get('data', [])
    documents = build_documents(data_list)

    bm25 = BM25Okapi(documents)
    similarity_calc = SimilarityCalculator(documents)

    query = 'universitas ranking terbaik'
    expanded = AbbreviationExpander.expand_query(query)
    query_tokens = expanded.lower().split()

    bm25_scores = bm25.get_scores(query_tokens)
    cosine_scores = similarity_calc.get_similarities(query_tokens)

    bm25_top = top_indices(bm25_scores, limit=10)
    cosine_top = top_indices(cosine_scores, limit=10)

    print(f'Query: "{query}"')
    print(f'Expanded: "{expanded}"')
    print_ranking('TOP 10 BM25', bm25_top, bm25_scores, data_list)
    print_ranking('TOP 10 COSINE SIMILARITY', cosine_top, cosine_scores, data_list)


def score_statistics():
    print_header('SCORE STATISTICS - SEPARATE')

    db = DatabaseManager()
    data = db.load_data()
    if not data or not data.get('data'):
        print('No data found')
        return

    data_list = data.get('data', [])
    documents = build_documents(data_list)

    bm25 = BM25Okapi(documents)
    similarity_calc = SimilarityCalculator(documents)

    query = 'universitas'
    expanded = AbbreviationExpander.expand_query(query)
    query_tokens = expanded.lower().split()

    bm25_scores = bm25.get_scores(query_tokens)
    cosine_scores = similarity_calc.get_similarities(query_tokens)

    import statistics

    def get_stats(scores):
        non_zero = [s for s in scores if s > 0]
        if not non_zero:
            return {'min': 0, 'max': 0, 'avg': 0, 'median': 0, 'count': 0}
        return {
            'min': min(non_zero),
            'max': max(non_zero),
            'avg': statistics.mean(non_zero),
            'median': statistics.median(non_zero),
            'count': len(non_zero),
        }

    bm25_stats = get_stats(bm25_scores)
    cosine_stats = get_stats(cosine_scores)

    print(f'Query: "{query}" (expanded: "{expanded}")\n')
    print(f"{'Metric':<12} {'BM25':<15} {'Cosine':<15}")
    print('-' * 45)
    for metric, label in [
        ('min', 'Min'),
        ('max', 'Max'),
        ('avg', 'Average'),
        ('median', 'Median'),
        ('count', 'Count>0'),
    ]:
        if metric == 'count':
            print(f"{label:<12} {bm25_stats[metric]:<15} {cosine_stats[metric]:<15}")
        else:
            print(f"{label:<12} {bm25_stats[metric]:<15.2f} {cosine_stats[metric]:<15.2f}")


def main():
    print('\n' + '=' * 80)
    print('  DUAL RANKING SYSTEM - SEPARATE BM25 AND COSINE')
    print('=' * 80)

    for name, test_func in [
        ('Dual Ranking Search', test_dual_ranking),
        ('Algorithm Comparison', compare_algorithms),
        ('Score Statistics', score_statistics),
    ]:
        try:
            test_func()
        except Exception as e:
            print(f'Error in {name}: {e}')

    print_header('ALL TESTS COMPLETED')
    print(
        "\nNext Steps:\n"
        "1. Run: python app.py\n"
        "2. Open: http://localhost:5000\n"
        "3. Search and view two separate result lists:\n"
        "   - Top 10 BM25\n"
        "   - Top 10 Cosine Similarity\n\n"
        "Catatan:\n"
        "- BM25 dan Cosine tidak dijumlahkan.\n"
        "- BM25 dan Cosine tidak dibagi 2.\n"
        "- Masing-masing algoritma punya ranking sendiri.\n"
    )


if __name__ == '__main__':
    main()
