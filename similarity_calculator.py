"""
Similarity Calculator - TF-IDF + Cosine Similarity
Untuk melengkapi BM25 scoring dengan cosine similarity
"""

import math
from collections import defaultdict
from abbreviation_expander import AbbreviationExpander

class SimilarityCalculator:
    """Calculate TF-IDF dan Cosine Similarity untuk documents"""
    
    def __init__(self, documents):
        """
        Initialize dengan list dokumen
        documents: list of list of tokens
        """
        self.documents = documents
        self.total_docs = len(documents)
        self.vocab = set()
        self.idf = {}
        self.doc_vectors = []
        
        self._build_vocabulary()
        self._calculate_idf()
        self._build_document_vectors()
    
    def _build_vocabulary(self):
        """Build vocabulary dari semua dokumen"""
        for doc in self.documents:
            self.vocab.update(doc)
    
    def _calculate_idf(self):
        """Calculate Inverse Document Frequency untuk setiap term"""
        doc_freq = defaultdict(int)
        
        # Count dokumen yang contain setiap term
        for doc in self.documents:
            for term in set(doc):
                doc_freq[term] += 1
        
        # Calculate IDF
        for term in self.vocab:
            if doc_freq[term] > 0:
                # IDF = log(total_docs / doc_frequency)
                self.idf[term] = math.log(self.total_docs / doc_freq[term])
            else:
                self.idf[term] = 0
    
    def _build_document_vectors(self):
        """Build TF-IDF vectors untuk setiap dokumen"""
        for doc in self.documents:
            vector = self._get_tfidf_vector(doc)
            self.doc_vectors.append(vector)
    
    def _get_tfidf_vector(self, doc):
        """Get TF-IDF vector untuk dokumen"""
        vector = {}
        
        # Calculate TF (term frequency)
        term_freq = defaultdict(int)
        for term in doc:
            term_freq[term] += 1
        
        # Calculate TF-IDF
        for term in term_freq:
            tf = term_freq[term]
            idf = self.idf.get(term, 0)
            vector[term] = tf * idf
        
        return vector
    
    def _normalize_vector(self, vector):
        """Normalize vektor ke unit length"""
        magnitude = math.sqrt(sum(v**2 for v in vector.values()))
        
        if magnitude == 0:
            return vector
        
        normalized = {}
        for term, value in vector.items():
            normalized[term] = value / magnitude
        
        return normalized
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity antara dua vectors"""
        # Normalize vectors
        vec1_norm = self._normalize_vector(vec1)
        vec2_norm = self._normalize_vector(vec2)
        
        # Calculate dot product
        dot_product = 0
        for term in vec1_norm:
            if term in vec2_norm:
                dot_product += vec1_norm[term] * vec2_norm[term]
        
        # Magnitude sudah 1 karena normalized, jadi similarity = dot_product
        # Cosine similarity adalah nilai antara 0 dan 1
        similarity_score = dot_product
        
        return similarity_score
    
    def get_similarities(self, query_tokens):
        """
        Get cosine similarity scores untuk query terhadap semua dokumen
        
        Returns: list of scores
        """
        # Build query vector
        query_vector = self._get_tfidf_vector(query_tokens)
        
        # Calculate similarity dengan setiap dokumen
        scores = []
        for doc_vector in self.doc_vectors:
            score = self._cosine_similarity(query_vector, doc_vector)
            scores.append(score)
        
        return scores
    
    @staticmethod
    def create_from_data(data_list):
        """Create SimilarityCalculator dari data list"""
        documents = []
        
        for item in data_list:
            full_text = f"{item.get('judul', '')} {item.get('isi_berita', '')}"
            expanded_text = AbbreviationExpander.expand_document(full_text)
            tokens = expanded_text.lower().split()
            documents.append(tokens)
        
        return SimilarityCalculator(documents)


# Test
if __name__ == "__main__":
    print("Testing Similarity Calculator:\n")
    
    # Sample documents
    docs = [
        ["universitas", "indonesia", "terbaik", "ranking"],
        ["universitas", "gadjah", "mada", "pendidikan"],
        ["ranking", "kampus", "dunia", "webometrics"],
        ["jalur", "masuk", "ptn", "pendaftaran"],
    ]
    
    # Create calculator
    calc = SimilarityCalculator(docs)
    
    # Test queries
    queries = [
        ["universitas", "terbaik"],
        ["ranking", "kampus"],
        ["jalur", "ptn"],
    ]
    
    for query in queries:
        scores = calc.get_similarities(query)
        print(f"Query: {' '.join(query)}")
        print(f"Scores: {[f'{s:.2f}' for s in scores]}")
        print()
    
    print("✓ Similarity Calculator test completed!")
