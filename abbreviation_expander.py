"""
Abbreviation Expander - Menangani singkatan untuk optimasi pencarian
"""

class AbbreviationExpander:
    """Expand singkatan menjadi bentuk lengkap untuk indexing yang lebih baik"""
    
    # Dictionary singkatan -> bentuk lengkap
    ABBREVIATIONS = {
        # Universitas
        'ui': 'universitas indonesia',
        'ugm': 'universitas gadjah mada',
        'itb': 'institut teknologi bandung',
        'unpad': 'universitas padjadjaran',
        'itk': 'institut teknologi keramat',
        'uii': 'universitas islam indonesia',
        'undip': 'universitas diponegoro',
        'ipb': 'institut pertanian bogor',
        'uin': 'universitas islam negeri',
        'nus': 'national university of singapore',
        'utm': 'universitas trunodjoyo madura',
        
        # Organisasi
        'the': 'times higher education',
        'csic': 'consejo superior de investigaciones cientificas',
        'scopus': 'scopus citation database',
        'scimago': 'scimago journal ranking',
        'webometrics': 'webometrics ranking',
        
        # Pendidikan
        'ptn': 'perguruan tinggi negeri',
        'pts': 'perguruan tinggi swasta',
        'sma': 'sekolah menengah atas',
        'ma': 'madrasah aliyah',
        'smk': 'sekolah menengah kejuruan',
        'mak': 'madrasah aliyah kejuruan',
        'mts': 'madrasah tsanawiyah',
        'smp': 'sekolah menengah pertama',
        'sd': 'sekolah dasar',
        
        # Organisasi Siswa
        'osis': 'organisasi siswa intra sekolah',
        'paskibra': 'pasukan pengibar bendera',
        'pmr': 'palang merah remaja',
        'kwarda': 'kwartir daerah pramuka',
        
        # Kecakapan
        'sku': 'syarat kecakapan umum',
        'skk': 'syarat kecakapan khusus',
        'tkk': 'tanda kecakapan khusus',
        
        # Lainnya
        'ri': 'republik indonesia',
        'wib': 'waktu indonesia bagian barat',
        'wit': 'waktu indonesia timur',
        'wita': 'waktu indonesia tengah',
        
        #ujian
        'snbt': 'seleksi nasional berdasarkan tes',
        'snbp': 'seleksi nasional berdasarkan prestasi',
        'utbk': 'ujian tulis berbasis komputer',
        'snpmb': 'seleksi nasional penerimaan mahasiswa baru',
        'uts': ''
    }
    
    @staticmethod
    def expand_text(text):
        """
        Expand singkatan dalam teks
        Contoh: "UI menduduki ranking terbaik" -> "universitas indonesia menduduki ranking terbaik"
        """
        result = text.lower()
        
        for abbrev, expansion in AbbreviationExpander.ABBREVIATIONS.items():
            # Match singkatan dengan word boundary
            import re
            # Pattern untuk mencocokkan singkatan standalone (bukan bagian dari kata lain)
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            result = re.sub(pattern, expansion, result, flags=re.IGNORECASE)
        
        return result
    
    @staticmethod
    def expand_query(query):
        """Expand query untuk pencarian yang lebih baik"""
        return AbbreviationExpander.expand_text(query)
    
    @staticmethod
    def expand_document(text):
        """Expand dokumen untuk indexing yang lebih baik"""
        return AbbreviationExpander.expand_text(text)
    
    @staticmethod
    def normalize_text(text):
        """
        Normalisasi teks dengan:
        1. Expand singkatan
        2. Hapus tanda baca berlebihan
        3. Normalize whitespace
        """
        import re
        
        # 1. Expand singkatan
        text = AbbreviationExpander.expand_text(text)
        
        # 2. Hapus tanda baca khusus, keep space
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # 3. Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def tokenize_with_expansion(text):
        """Tokenize teks dengan expansion terlebih dahulu"""
        normalized = AbbreviationExpander.normalize_text(text)
        tokens = normalized.split()
        return tokens
    
    @staticmethod
    def add_abbreviation(abbrev, expansion):
        """Add custom abbreviation"""
        AbbreviationExpander.ABBREVIATIONS[abbrev.lower()] = expansion.lower()
    
    @staticmethod
    def get_abbreviations():
        """Get semua abbreviations"""
        return AbbreviationExpander.ABBREVIATIONS.copy()


# Test
if __name__ == "__main__":
    print("Testing Abbreviation Expander:\n")
    
    # Test 1: Expand text
    text1 = "UI menduduki peringkat terbaik, diikuti UGM dan ITB"
    expanded1 = AbbreviationExpander.expand_text(text1)
    print(f"Original: {text1}")
    print(f"Expanded: {expanded1}\n")
    
    # Test 2: Normalize text
    text2 = "PTN di Indonesia (UI, UGM, ITB) memiliki standar tinggi."
    normalized2 = AbbreviationExpander.normalize_text(text2)
    print(f"Original: {text2}")
    print(f"Normalized: {normalized2}\n")
    
    # Test 3: Tokenize with expansion
    text3 = "Mahasiswa SMA dapat masuk PTN melalui jalur SNMPTN, UTBK, atau jalur mandiri PTN"
    tokens3 = AbbreviationExpander.tokenize_with_expansion(text3)
    print(f"Original: {text3}")
    print(f"Tokens: {tokens3}\n")
    
    # Test 4: Search query
    query = "universitas terbaik di UI"
    expanded_query = AbbreviationExpander.expand_query(query)
    print(f"Query: {query}")
    print(f"Expanded Query: {expanded_query}\n")
    
    print("✓ All tests completed!")
