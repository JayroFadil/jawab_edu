# BM25 Algorithm Verification

## Standar BM25 Formula

### IDF (Inverse Document Frequency)
```
IDF(qi) = ln((N - n(qi) + 0.5) / (n(qi) + 0.5) + 1)
```

### Scoring Formula
```
score(D, Q) = Σ IDF(qi) * (f(qi, D) * (k1 + 1)) / (f(qi, D) + k1 * (1 - b + b * |D| / avgdl))
```

**Parameter defaults:**
- k1 = 1.5 (controls term frequency saturation point)
- b = 0.75 (controls how much effect document length has on relevance)

---

## Implementasi di `bm25.py`

### ✅ IDF Calculation - BENAR

```python
self.idf[term] = math.log((self.N - df + 0.5) / (df + 0.5) + 1)
```

**Verifikasi:**
- `self.N` = N (total dokumen)
- `df` = n(qi) (dokumen yang mengandung term)
- Formula: ln((N - df + 0.5) / (df + 0.5) + 1) ✓
- Menggunakan `math.log()` = ln (natural logarithm) ✓

### ✅ Scoring Calculation - BENAR

```python
denom = freq + self.k1 * (1 - self.b + self.b * self.doc_len[idx] / self.avgdl)
score = token_idf * freq * (self.k1 + 1) / denom
scores[idx] += score
```

**Verifikasi:**
- `freq` = f(qi, D) (term frequency dalam dokumen)
- `self.k1` = k1 (default 1.5) ✓
- `self.b` = b (default 0.75) ✓  
- `self.doc_len[idx]` = |D| (panjang dokumen)
- `self.avgdl` = avgdl (panjang rata-rata dokumen)
- Denominator: freq + k1 * (1 - b + b * |D| / avgdl) ✓
- Numerator: token_idf * freq * (k1 + 1) ✓
- Accumulation untuk multiple query terms ✓

### ✅ Parameter Default - BENAR

```python
def __init__(self, documents, k1=1.5, b=0.75):
```

- k1 = 1.5 (standar) ✓
- b = 0.75 (standar) ✓

---

## Kesimpulan

**Status: ✅ SESUAI DENGAN STANDAR BM25**

Algoritma BM25 sudah diimplementasikan dengan **benar** dan sesuai dengan formula standar. Tidak ada masalah yang ditemukan.

### Karakteristik Output:
- **Range skor**: 0 sampai tak terbatas (unbounded)
- **Lebih tinggi**: Dokumen yang lebih relevan
- **Berbeda dengan Cosine**: Cosine similarity terbatas pada [0, 1]
