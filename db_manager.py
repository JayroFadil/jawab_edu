"""
Database Manager - Helper script untuk mengelola JSON database
Fitur:
- Konversi CSV ke JSON
- Update data
- Generate indexing otomatis
"""

import json
import csv
import os
from datetime import datetime
from abbreviation_expander import AbbreviationExpander

class DatabaseManager:
    def __init__(self, data_file='data_detail_pendidikan.json', index_file='index_data.json'):
        self.data_file = data_file
        self.index_file = index_file
    
    def csv_to_json(self, csv_path):
        """Konversi CSV ke JSON database.
        csv_path dapat berupa string tunggal atau list/tuple path CSV."""
        data_list = []
        doc_id = 1
        
        try:
            csv_paths = [csv_path] if isinstance(csv_path, str) else list(csv_path)
            for path in csv_paths:
                with open(path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        data_list.append({
                            "id": doc_id,
                            "tanggal": row.get('tanggal', ''),
                            "judul": row.get('judul', ''),
                            "isi_berita": row.get('isi_berita', ''),
                            "link": row.get('link', ''),
                            "kategori": self._extract_kategori(row.get('judul', ''))
                        })
                        doc_id += 1
            
            # Simpan ke JSON
            self.save_data({"data": data_list})
            print(f"✓ Berhasil konversi {len(data_list)} dokumen dari {len(csv_paths)} CSV ke JSON")
            
            # Generate indexing
            self.generate_index(data_list)
            return True
        
        except Exception as e:
            print(f"✗ Error konversi CSV: {e}")
            return False
    
    def _extract_kategori(self, judul):
        """Extract kategori dari judul"""
        judul_lower = judul.lower()
        if 'universitas' in judul_lower or 'kampus' in judul_lower or 'univ' in judul_lower:
            return 'universitas'
        elif 'jalur' in judul_lower or 'masuk' in judul_lower:
            return 'jalur-masuk'
        elif 'beasiswa' in judul_lower:
            return 'beasiswa'
        else:
            return 'umum'
    
    def generate_index(self, data_list):
        """Generate indexing otomatis dari data dengan abbreviation expansion"""
        index_list = []
        
        for item in data_list:
            # Tokenize judul dan isi berita dengan abbreviation expansion
            full_text = f"{item.get('judul', '')} {item.get('isi_berita', '')}"
            expanded_text = AbbreviationExpander.expand_document(full_text)
            tokens = expanded_text.lower().split()
            
            index_list.append({
                "id": item.get('id'),
                "tokens": tokens,
                "kategori": item.get('kategori', 'umum'),
                "timestamp": self._extract_date(item.get('tanggal', ''))
            })
        
        # Simpan index
        index_data = {
            "index": index_list,
            "metadata": {
                "total_documents": len(data_list),
                "indexed_fields": ["judul", "isi_berita"],
                "last_updated": datetime.now().isoformat(),
                "version": "1.1",
                "abbreviation_expansion": True
            }
        }
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Berhasil generate indexing untuk {len(index_list)} dokumen (dengan expansion singkatan)")
    
    def _extract_date(self, tanggal_str):
        """Extract tanggal dalam format YYYY-MM-DD"""
        # Format: "Minggu, 26 Apr 2026 19:00 WIB"
        try:
            parts = tanggal_str.split()
            day = parts[1].rstrip(',')
            month_str = parts[2]
            year = parts[3]
            
            months = {
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                'Mei': '05', 'Jun': '06', 'Jul': '07', 'Agu': '08',
                'Sep': '09', 'Okt': '10', 'Nov': '11', 'Des': '12'
            }
            
            month = months.get(month_str, '01')
            return f"{year}-{month}-{day.zfill(2)}"
        except:
            return datetime.now().strftime('%Y-%m-%d')
    
    def save_data(self, data):
        """Simpan data ke JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_data(self):
        """Load data dari JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def add_document(self, judul, isi_berita, link, tanggal=""):
        """Tambah dokumen baru"""
        data = self.load_data()
        
        if not data:
            data = {"data": []}
        
        if not tanggal:
            from datetime import datetime
            tanggal = datetime.now().strftime("%A, %d %b %Y %H:%M WIB")
        
        new_doc = {
            "id": len(data.get('data', [])) + 1,
            "tanggal": tanggal,
            "judul": judul,
            "isi_berita": isi_berita,
            "link": link,
            "kategori": self._extract_kategori(judul)
        }
        
        data['data'].append(new_doc)
        self.save_data(data)
        
        # Update index
        self.generate_index(data['data'])
        print(f"✓ Dokumen '{judul[:50]}...' berhasil ditambahkan")
    
    def search_documents(self, keyword):
        """Search dokumen berdasarkan keyword dengan abbreviation expansion"""
        data = self.load_data()
        results = []
        
        if data:
            # Expand keyword untuk mencocokkan singkatan
            expanded_keyword = AbbreviationExpander.expand_query(keyword)
            keyword_lower = expanded_keyword.lower()
            
            for item in data.get('data', []):
                judul = item.get('judul', '').lower()
                isi = item.get('isi_berita', '').lower()
                
                # Expand judul dan isi berita juga
                expanded_judul = AbbreviationExpander.expand_text(judul)
                expanded_isi = AbbreviationExpander.expand_text(isi)
                
                if keyword_lower in expanded_judul or keyword_lower in expanded_isi:
                    results.append(item)
        
        return results
    
    def get_by_kategori(self, kategori):
        """Get dokumen berdasarkan kategori"""
        data = self.load_data()
        results = []
        
        if data:
            for item in data.get('data', []):
                if item.get('kategori') == kategori:
                    results.append(item)
        
        return results


if __name__ == "__main__":
    db_manager = DatabaseManager()
    
    # Contoh penggunaan:
    # 1. Konversi beberapa CSV ke JSON sekaligus
    db_manager.csv_to_json([
        'data_detail_pendidikan.csv',
        'data_detail_pendidikan_kompass.csv'
    ])
    
    # 2. Tambah dokumen baru
    # db_manager.add_document(
    #     judul="Contoh Berita Terbaru",
    #     isi_berita="Isi berita di sini...",
    #     link="https://example.com"
    # )
    
    # 3. Search dokumen
    # results = db_manager.search_documents('universitas')
    # print(f"Ditemukan {len(results)} hasil")
    
    print("Database Manager loaded successfully!")
    print("Gunakan class DatabaseManager untuk mengelola JSON database")
