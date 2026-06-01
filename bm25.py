import math
from collections import Counter, defaultdict

class BM25:
    def __init__(self, documents, k1=1.5, b=0.75):
        self.documents = documents
        self.N = len(documents)
        self.k1 = k1
        self.b = b
        self.doc_len = [len(doc) for doc in documents]
        self.avgdl = sum(self.doc_len) / self.N if self.N else 1.0
        self.doc_freq = defaultdict(int)
        self.term_freqs = []

        for doc in documents:
            tf = Counter(doc)
            self.term_freqs.append(tf)
            for term in tf:
                self.doc_freq[term] += 1

        self.idf = {}
        for term, df in self.doc_freq.items():
            self.idf[term] = math.log((self.N - df + 0.5) / (df + 0.5) + 1)

    def get_scores(self, query_tokens):
        scores = [0.0] * self.N

        for token in query_tokens:
            token_idf = self.idf.get(token, 0.0)
            if token_idf == 0.0:
                continue

            for idx, tf in enumerate(self.term_freqs):
                freq = tf.get(token, 0)
                if freq == 0:
                    continue

                denom = freq + self.k1 * (1 - self.b + self.b * self.doc_len[idx] / self.avgdl)
                score = token_idf * freq * (self.k1 + 1) / denom
                scores[idx] += score

        return scores
