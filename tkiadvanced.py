import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.detik.com/edu/indeks?page={}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Filter kata kunci
kata_kunci = [
    "beasiswa", "lpdp", "kip", "bpi", 
    "perguruan tinggi", "ptn", "pts", "kampus", "universitas", 
    "utbk", "snbt", "snbp", "snmptn", "sbmptn", 
    "jalur mandiri", "penerimaan mahasiswa", "maba", "ukt", "ujian"
]

def ambil_isi_berita(url_detail):
    try:
        res = requests.get(url_detail, headers=headers, timeout=10)
        soup_detail = BeautifulSoup(res.text, "html.parser")

        tag_tgl = soup_detail.find("div", class_="detail__date")
        tanggal = tag_tgl.get_text(strip=True) if tag_tgl else "Tanggal tidak ditemukan"
        
        body = soup_detail.find("div", class_="detail__body-text")
        if body:
            paragraf = body.find_all("p")
            isi_lengkap = " ".join([p.get_text(strip=True) for p in paragraf])
        else:
            isi_lengkap = "Konten tidak ditemukan"
            
        return tanggal, isi_lengkap
    except:
        return "Gagal ambil tanggal", "Gagal ambil konten"

data = []
target = 1000
for page in range(1, 600):
    print(f"\n--- Scraping Halaman Indeks {page} ---")
    url = BASE_URL.format(page)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article")

        for article in articles:
            link_tag = article.find("a")
            title_tag = article.find("h2") or article.find("h3")

            if link_tag and title_tag:
                judul = title_tag.get_text(strip=True)
                link = link_tag.get("href")
                judul_lower = judul.lower()

                if any(kunci in judul_lower for kunci in kata_kunci):
                    print(f"Menemukan: {judul}. Membuka link...")

                    tanggal, isi_berita = ambil_isi_berita(link)
                    
                    data.append({
                        "tanggal": tanggal,
                        "judul": judul,
                        "isi_berita": isi_berita,
                        "link": link
                    })

                    time.sleep(0.5)

        if len(data) >= target:
            break
            
    except Exception as e:
        print(f"Error di halaman {page}: {e}")

if data:
    df = pd.DataFrame(data)
    df.to_csv("data_detail_pendidikan.csv", index=False, encoding="utf-8-sig")
    print(f"\nSelesai! Berhasil mengambil {len(df)} berita lengkap.")