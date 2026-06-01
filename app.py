from flask import Flask, render_template, request
import json
from abbreviation_expander import AbbreviationExpander
from similarity_calculator import SimilarityCalculator
from bm25 import BM25
import os

app = Flask(__name__)

# Load data dari JSON
def load_data_from_json():
    json_path = os.path.join(os.path.dirname(__file__), 'data_detail_pendidikan.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('data', [])
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

# Load indexing data
def load_index_data():
    index_path = os.path.join(os.path.dirname(__file__), 'index_data.json')
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        return index_data.get('index', [])
    except Exception as e:
        print(f"Error loading index: {e}")
        return []

# Inisialisasi data dan BM25
data_list = load_data_from_json()
index_list = load_index_data()

# Siapkan dokumen untuk BM25
documents = []
data_map = {}

if data_list:
    for item in data_list:
        doc_id = item.get('id')
        data_map[doc_id] = item
        # Gabungkan judul dan isi berita untuk indexing dengan abbreviation expansion
        full_text = f"{item.get('judul', '')} {item.get('isi_berita', '')}"
        expanded_text = AbbreviationExpander.expand_document(full_text)
        doc = expanded_text.lower().split()
        documents.append(doc)
    
    bm25 = BM25(documents)
    similarity_calc = SimilarityCalculator.create_from_data(data_list)
else:
    bm25 = None
    similarity_calc = None
    documents = []

@app.route("/", methods=["GET", "POST"])
def index():
    pertanyaan = ""
    hasil = None

    if request.method == "POST":
        pertanyaan = request.form.get("pertanyaan", "")
        
        if bm25 and similarity_calc and data_list:
            # Expand singkatan dalam query dan tokenize
            expanded_query = AbbreviationExpander.expand_query(pertanyaan)
            query_tokens = expanded_query.lower().split()
            
            # Hitung BM25 scores
            bm25_scores = bm25.get_scores(query_tokens)
            
            # Hitung Cosine Similarity scores
            cosine_scores = similarity_calc.get_similarities(query_tokens)
            
            # Ambil top 10 untuk BM25
            bm25_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)
            bm25_top_indices = [i for i in bm25_indices if bm25_scores[i] > 0][:10]
            
            # Ambil top 10 untuk Cosine Similarity
            cosine_indices = sorted(range(len(cosine_scores)), key=lambda i: cosine_scores[i], reverse=True)
            cosine_top_indices = [i for i in cosine_indices if cosine_scores[i] > 0][:10]
            
            # Siapkan hasil untuk BM25 top 10
            bm25_results = []
            for rank, idx in enumerate(bm25_top_indices, 1):
                item = data_list[idx]
                isi_berita = item.get('isi_berita', '')
                isi_display = isi_berita[:250] + "..." if len(isi_berita) > 250 else isi_berita
                
                bm25_results.append({
                    "rank": rank,
                    "judul": item.get('judul', ''),
                    "jawaban": isi_display,
                    "sumber": item.get('link', ''),
                    "kategori": item.get('kategori', ''),
                    "tanggal": item.get('tanggal', ''),
                    "score": f"{bm25_scores[idx]:.2f}"
                })
            
            # Siapkan hasil untuk Cosine top 10
            cosine_results = []
            for rank, idx in enumerate(cosine_top_indices, 1):
                item = data_list[idx]
                isi_berita = item.get('isi_berita', '')
                isi_display = isi_berita[:250] + "..." if len(isi_berita) > 250 else isi_berita
                
                cosine_results.append({
                    "rank": rank,
                    "judul": item.get('judul', ''),
                    "jawaban": isi_display,
                    "sumber": item.get('link', ''),
                    "kategori": item.get('kategori', ''),
                    "tanggal": item.get('tanggal', ''),
                    "score": f"{cosine_scores[idx]:.2f}"
                })
            
            if bm25_results or cosine_results:
                hasil = {
                    "bm25_results": bm25_results,
                    "cosine_results": cosine_results,
                    "query": pertanyaan,
                    "expanded_query": expanded_query,
                    "bm25_count": len(bm25_results),
                    "cosine_count": len(cosine_results)
                }
            else:
                hasil = {
                    "jawaban": "Maaf, tidak ada hasil yang cocok untuk pencarian Anda.",
                    "sumber": "Tidak ada sumber yang cocok",
                    "bm25_results": [],
                    "cosine_results": []
                }
        else:
            hasil = {
                "jawaban": "Maaf, data belum berhasil dimuat.",
                "sumber": "Error"
            }

    return render_template("index.html", pertanyaan=pertanyaan, hasil=hasil)

if __name__ == "__main__":
    app.run(debug=True)
