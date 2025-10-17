from textblob import TextBlob
from typing import Dict, List, Tuple
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
        
        self.profanity_keywords = [
            'anjing', 'babi', 'tai', 'bangsat', 'bajingan', 'kampret',
            'tolol', 'goblok', 'bodoh', 'idiot', 'kontol', 'memek'
        ]
        
        self.hate_speech_keywords = [
            'bunuh', 'mati', 'hancurkan', 'bakar', 'habisi',
            'kafir', 'komunis', 'antek', 'pribumi', 'aseng'
        ]
        
        self.political_keywords = [
            'pemerintah', 'presiden', 'menteri', 'dpr', 'partai',
            'pemilu', 'pilkada', 'politik', 'oposisi', 'koalisi'
        ]

    def analyze_text(self, text: str) -> Dict:
        if not text or not text.strip():
            return self._empty_result()
        
        text = text.lower().strip()
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        sentiment_label = self._get_sentiment_label(polarity)
        
        contains_profanity = self._contains_keywords(text, self.profanity_keywords)
        contains_hate_speech = self._contains_keywords(text, self.hate_speech_keywords)
        contains_political = self._contains_keywords(text, self.political_keywords)
        
        keywords = self._extract_keywords(text)
        
        return {
            'sentiment_label': sentiment_label,
            'sentiment_score': polarity,
            'confidence': 1 - subjectivity,
            'contains_profanity': 1 if contains_profanity else 0,
            'contains_hate_speech': 1 if contains_hate_speech else 0,
            'contains_political_content': 1 if contains_political else 0,
            'keywords': keywords
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
                'total_political': 0
            }
        
        sentiments = [a['sentiment_score'] for a in analyses]
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        positive_count = sum(1 for a in analyses if a['sentiment_label'] == 'positive')
        negative_count = sum(1 for a in analyses if a['sentiment_label'] == 'negative')
        neutral_count = sum(1 for a in analyses if a['sentiment_label'] == 'neutral')
        
        total = len(analyses)
        
        return {
            'average_sentiment': avg_sentiment,
            'positive_ratio': positive_count / total,
            'negative_ratio': negative_count / total,
            'neutral_ratio': neutral_count / total,
            'total_profanity': sum(a['contains_profanity'] for a in analyses),
            'total_hate_speech': sum(a['contains_hate_speech'] for a in analyses),
            'total_political': sum(a['contains_political_content'] for a in analyses)
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

    def _extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        words = re.findall(r'\b\w+\b', text.lower())
        
        stopwords = {'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'dengan', 
                     'untuk', 'pada', 'adalah', 'oleh', 'dalam', 'atau', 'juga',
                     'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to'}
        
        words = [w for w in words if w not in stopwords and len(w) > 3]
        
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]]

    def _empty_result(self) -> Dict:
        return {
            'sentiment_label': 'neutral',
            'sentiment_score': 0.0,
            'confidence': 0.0,
            'contains_profanity': 0,
            'contains_hate_speech': 0,
            'contains_political_content': 0,
            'keywords': []
        }
