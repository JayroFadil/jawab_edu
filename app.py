from flask import Flask, render_template, request
import pandas as pd
from rank_bm25 import BM25Okapi
import os

app = Flask(__name__)

# Load data dari CSV
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'data_detail_pendidikan.csv')
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

# Inisialisasi data dan BM25
df = load_data()

# Siapkan dokumen untuk BM25
if not df.empty:
    # Tokenize: split teks menjadi kata-kata
    documents = []
    for idx, row in df.iterrows():
        # Gabungkan judul dan isi berita untuk indexing
        doc = f"{row['judul']} {row['isi_berita']}".lower().split()
        documents.append(doc)
    
    bm25 = BM25Okapi(documents)
else:
    bm25 = None
    documents = []

@app.route("/", methods=["GET", "POST"])
def index():
    pertanyaan = ""
    hasil = None

    if request.method == "POST":
        pertanyaan = request.form.get("pertanyaan", "")
        
        if bm25 and not df.empty:
            # Tokenize query
            query_tokens = pertanyaan.lower().split()
            
            # Hitung BM25 scores
            scores = bm25.get_scores(query_tokens)
            
            # Ambil top hasil dengan score > 0
            top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
            top_indices = [i for i in top_indices if scores[i] > 0][:3]
            
            if top_indices:
                # Ambil hasil terbaik
                best_idx = top_indices[0]
                best_row = df.iloc[best_idx]
                hasil = {
                    "jawaban": best_row['isi_berita'][:500] + "..." if len(best_row['isi_berita']) > 500 else best_row['isi_berita'],
                    "judul": best_row['judul'],
                    "sumber": best_row['link'],
                    "score": f"{scores[best_idx]:.2f}"
                }
            else:
                hasil = {
                    "jawaban": "Maaf, tidak ada hasil yang cocok untuk pencarian Anda.",
                    "sumber": "Tidak ada sumber yang cocok"
                }
        else:
            hasil = {
                "jawaban": "Maaf, data belum berhasil dimuat.",
                "sumber": "Error"
            }

    return render_template("index.html", pertanyaan=pertanyaan, hasil=hasil)

if __name__ == "__main__":
    app.run(debug=True)
