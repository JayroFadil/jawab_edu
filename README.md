# JawabEdu - UI Chat Sederhana

Project ini adalah tampilan sederhana untuk UAS mata kuliah Temu Kembali Informasi (TKI).

Tampilan sudah diubah menjadi model chat seperti ChatGPT, tetapi tetap ringan dan mudah dipahami.

## Fitur

- Tampilan chat sederhana
- Sidebar berisi nama aplikasi dan contoh pertanyaan
- Input pertanyaan di bagian bawah
- Bubble pertanyaan pengguna
- Bubble jawaban dari JawabEdu
- Sumber referensi jawaban
- Responsive untuk laptop dan HP

## Cara Menjalankan

```bash
pip install -r requirements.txt
python app.py
```

Buka browser:

```text
http://127.0.0.1:5000
```

Catatan: Project ini menampilkan dua ranking terpisah: Top 10 BM25 dan Top 10 Cosine Similarity. Skor tidak digabung atau dirata-ratakan.
