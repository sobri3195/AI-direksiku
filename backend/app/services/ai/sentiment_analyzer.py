from textblob import TextBlob
from typing import Dict, List
import re
import nltk
from app.core.config import settings

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)


class SentimentAnalyzer:
    def __init__(self):
        self.negative_threshold = settings.SENTIMENT_THRESHOLD_NEGATIVE
        self.positive_threshold = settings.SENTIMENT_THRESHOLD_POSITIVE

        # Expanded lexicons for richer detection
        self.profanity_keywords = [
            'anjing', 'babi', 'tai', 'bangsat', 'bajingan', 'kampret',
            'tolol', 'goblok', 'bodoh', 'idiot', 'kontol', 'memek',
            'brengsek', 'tai', 'keparat', 'sialan'
        ]

        self.hate_speech_keywords = [
            'bunuh', 'mati', 'hancurkan', 'bakar', 'habisi',
            'kafir', 'komunis', 'antek', 'pribumi', 'aseng',
            'genosida', 'ekstremis'
        ]

        self.political_keywords = [
            'pemerintah', 'presiden', 'menteri', 'dpr', 'partai',
            'pemilu', 'pilkada', 'politik', 'oposisi', 'koalisi'
        ]

        # Positive/professional vocabulary
        self.professional_keywords = [
            'integritas', 'profesional', 'profesionalisme', 'akuntabilitas',
            'transparansi', 'melayani', 'pelayanan', 'merit', 'inovasi',
            'disiplin', 'etika', 'kepemimpinan', 'kolaborasi', 'publik'
        ]

        self.politeness_keywords = [
            'terima kasih', 'mohon maaf', 'permisi', 'tolong', 'harap', 'mohon'
        ]

        # Stopwords for naive language guess
        self.id_stopwords = {
            'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'dengan',
            'untuk', 'pada', 'adalah', 'oleh', 'dalam', 'atau', 'juga', 'tidak',
            'sudah', 'kami', 'kita', 'anda', 'saya', 'akan', 'bukan'
        }
        self.en_stopwords = {
            'the', 'and', 'in', 'on', 'at', 'to', 'for', 'is', 'are', 'a', 'an',
            'of', 'by', 'with', 'this', 'that', 'it', 'or', 'but', 'from'
        }

    def analyze_text(self, text: str) -> Dict:
        if not text or not text.strip():
            return self._empty_result()

        text_clean = text.strip()
        text_lower = text_clean.lower()

        blob = TextBlob(text_lower)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        sentiment_label = self._get_sentiment_label(polarity)

        contains_profanity = self._contains_keywords(text_lower, self.profanity_keywords)
        contains_hate_speech = self._contains_keywords(text_lower, self.hate_speech_keywords)
        contains_political = self._contains_keywords(text_lower, self.political_keywords)

        contains_link = self._contains_link(text_lower)
        caps_ratio = self._caps_ratio(text_clean)
        exclamation_count = text_clean.count('!')

        keywords = self._extract_keywords(text_lower)
        professional_kw_count = self._count_keywords(text_lower, self.professional_keywords)
        politeness_kw_count = self._count_keywords(text_lower, self.politeness_keywords)

        likely_language, id_ratio, en_ratio = self._guess_language(text_lower)
        toxicity_score = self._compute_toxicity(
            polarity=polarity,
            contains_profanity=contains_profanity,
            contains_hate_speech=contains_hate_speech,
            caps_ratio=caps_ratio,
            exclamations=exclamation_count,
        )

        spam_indicator = 1 if (contains_link and exclamation_count >= 3) else 0

        return {
            'sentiment_label': sentiment_label,
            'sentiment_score': polarity,
            'confidence': 1 - subjectivity,
            'contains_profanity': 1 if contains_profanity else 0,
            'contains_hate_speech': 1 if contains_hate_speech else 0,
            'contains_political_content': 1 if contains_political else 0,
            'keywords': keywords,
            # New enrichment fields (backwards-compatible)
            'contains_link': 1 if contains_link else 0,
            'caps_ratio': caps_ratio,
            'exclamation_count': exclamation_count,
            'likely_language': likely_language,
            'id_stopword_ratio': id_ratio,
            'en_stopword_ratio': en_ratio,
            'toxicity_score': toxicity_score,
            'spam_indicator': spam_indicator,
            'professional_keywords_count': professional_kw_count,
            'politeness_keywords_count': politeness_kw_count,
        }

    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        return [self.analyze_text(text) for text in texts]

    def calculate_aggregate_sentiment(self, analyses: List[Dict]) -> Dict:
        if not analyses:
            return {
                'average_sentiment': 0.0,
                'positive_ratio': 0.0,
                'negative_ratio': 0.0,
                'neutral_ratio': 0.0,
                'total_profanity': 0,
                'total_hate_speech': 0,
                'total_political': 0,
                # Enriched aggregates
                'avg_confidence': 0.0,
                'avg_toxicity': 0.0,
                'contains_links_ratio': 0.0,
                'excessive_caps_ratio': 0.0,
                'exclamation_avg': 0.0,
                'language_distribution': {'id': 0, 'en': 0, 'unknown': 0},
                'primary_language': 'unknown',
                'professional_keywords_total': 0,
            }

        sentiments = [a.get('sentiment_score', 0.0) for a in analyses]
        avg_sentiment = sum(sentiments) / max(len(sentiments), 1)

        positive_count = sum(1 for a in analyses if a.get('sentiment_label') == 'positive')
        negative_count = sum(1 for a in analyses if a.get('sentiment_label') == 'negative')
        neutral_count = sum(1 for a in analyses if a.get('sentiment_label') == 'neutral')

        total = max(len(analyses), 1)

        avg_confidence = sum(a.get('confidence', 0.0) for a in analyses) / total
        avg_toxicity = sum(a.get('toxicity_score', 0.0) for a in analyses) / total
        links_ratio = sum(1 for a in analyses if a.get('contains_link', 0) == 1) / total
        caps_ratio_over = sum(1 for a in analyses if a.get('caps_ratio', 0.0) > 0.5) / total
        exclamation_avg = sum(a.get('exclamation_count', 0) for a in analyses) / total

        lang_dist = {'id': 0, 'en': 0, 'unknown': 0}
        for a in analyses:
            lang = a.get('likely_language', 'unknown')
            if lang not in lang_dist:
                lang = 'unknown'
            lang_dist[lang] += 1
        primary_language = max(lang_dist, key=lambda k: lang_dist[k]) if analyses else 'unknown'

        prof_total = sum(a.get('professional_keywords_count', 0) for a in analyses)

        return {
            'average_sentiment': avg_sentiment,
            'positive_ratio': positive_count / total,
            'negative_ratio': negative_count / total,
            'neutral_ratio': neutral_count / total,
            'total_profanity': sum(a.get('contains_profanity', 0) for a in analyses),
            'total_hate_speech': sum(a.get('contains_hate_speech', 0) for a in analyses),
            'total_political': sum(a.get('contains_political_content', 0) for a in analyses),
            # Enriched aggregates
            'avg_confidence': avg_confidence,
            'avg_toxicity': avg_toxicity,
            'contains_links_ratio': links_ratio,
            'excessive_caps_ratio': caps_ratio_over,
            'exclamation_avg': exclamation_avg,
            'language_distribution': lang_dist,
            'primary_language': primary_language,
            'professional_keywords_total': prof_total,
        }

    def _get_sentiment_label(self, polarity: float) -> str:
        if polarity >= self.positive_threshold:
            return 'positive'
        elif polarity <= -self.negative_threshold:
            return 'negative'
        else:
            return 'neutral'

    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        for keyword in keywords:
            if keyword in text:
                return True
        return False

    def _count_keywords(self, text: str, keywords: List[str]) -> int:
        count = 0
        for kw in keywords:
            count += text.count(kw)
        return count

    def _extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        words = re.findall(r'\b\w+\b', text.lower())

        stopwords = {
            'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'dengan',
            'untuk', 'pada', 'adalah', 'oleh', 'dalam', 'atau', 'juga',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to'
        }

        words = [w for w in words if w not in stopwords and len(w) > 3]

        word_freq: Dict[str, int] = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:top_n]]

    def _contains_link(self, text: str) -> bool:
        return re.search(r'(https?://|www\.|\.[a-z]{2,3}/)', text) is not None

    def _caps_ratio(self, text: str) -> float:
        letters = [c for c in text if c.isalpha()]
        if not letters:
            return 0.0
        upper = sum(1 for c in letters if c.isupper())
        return upper / len(letters)

    def _guess_language(self, text: str):
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return 'unknown', 0.0, 0.0
        id_hits = sum(1 for w in words if w in self.id_stopwords)
        en_hits = sum(1 for w in words if w in self.en_stopwords)
        total = max(len(words), 1)
        id_ratio = id_hits / total
        en_ratio = en_hits / total
        if id_ratio > en_ratio + 0.01:
            lang = 'id'
        elif en_ratio > id_ratio + 0.01:
            lang = 'en'
        else:
            lang = 'unknown'
        return lang, id_ratio, en_ratio

    def _compute_toxicity(self, polarity: float, contains_profanity: bool, contains_hate_speech: bool, caps_ratio: float, exclamations: int) -> float:
        score = 0.0
        if contains_hate_speech:
            score += 1.0
        if contains_profanity:
            score += 0.5
        if polarity < -0.5:
            score += 0.2
        if caps_ratio > 0.5:
            score += 0.1
        if exclamations >= 3:
            score += 0.1
        return min(score, 1.0)

    def _empty_result(self) -> Dict:
        return {
            'sentiment_label': 'neutral',
            'sentiment_score': 0.0,
            'confidence': 0.0,
            'contains_profanity': 0,
            'contains_hate_speech': 0,
            'contains_political_content': 0,
            'keywords': [],
            'contains_link': 0,
            'caps_ratio': 0.0,
            'exclamation_count': 0,
            'likely_language': 'unknown',
            'id_stopword_ratio': 0.0,
            'en_stopword_ratio': 0.0,
            'toxicity_score': 0.0,
            'spam_indicator': 0,
            'professional_keywords_count': 0,
            'politeness_keywords_count': 0,
        }
