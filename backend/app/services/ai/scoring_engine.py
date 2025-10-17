from typing import Dict, List
import numpy as np
from app.models.screening import RecommendationStatus


class ScoringEngine:
    def __init__(self):
        self.weights = {
            'sentiment': 0.30,
            'professionalism': 0.25,
            'digital_ethics': 0.25,
            'social': 0.20
        }
        
        self.risk_thresholds = {
            'profanity_count': 3,
            'hate_speech_count': 1,
            'negative_ratio': 0.5,
            'low_engagement': 0.1
        }

    def calculate_overall_score(
        self,
        sentiment_data: Dict,
        digital_footprints: List[Dict],
        content_analyses: List[Dict]
    ) -> Dict:
        sentiment_score = self._calculate_sentiment_score(sentiment_data)
        professionalism_score = self._calculate_professionalism_score(digital_footprints, content_analyses)
        digital_ethics_score = self._calculate_digital_ethics_score(sentiment_data, content_analyses)
        social_score = self._calculate_social_score(digital_footprints)
        
        overall_score = (
            sentiment_score * self.weights['sentiment'] +
            professionalism_score * self.weights['professionalism'] +
            digital_ethics_score * self.weights['digital_ethics'] +
            social_score * self.weights['social']
        )
        
        risk_flags = self._identify_risk_flags(sentiment_data, content_analyses)
        positive_indicators = self._identify_positive_indicators(sentiment_data, digital_footprints)
        
        recommendation = self._determine_recommendation(overall_score, risk_flags)
        recommendation_reason = self._generate_recommendation_reason(
            overall_score, risk_flags, positive_indicators
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'technical_score': 0.0,
            'social_score': round(social_score, 2),
            'digital_ethics_score': round(digital_ethics_score, 2),
            'professionalism_score': round(professionalism_score, 2),
            'sentiment_score': round(sentiment_score, 2),
            'positive_content_ratio': sentiment_data.get('positive_ratio', 0),
            'negative_content_ratio': sentiment_data.get('negative_ratio', 0),
            'neutral_content_ratio': sentiment_data.get('neutral_ratio', 0),
            'recommendation': recommendation,
            'recommendation_reason': recommendation_reason,
            'risk_flags': risk_flags,
            'positive_indicators': positive_indicators
        }

    def _calculate_sentiment_score(self, sentiment_data: Dict) -> float:
        avg_sentiment = sentiment_data.get('average_sentiment', 0)
        positive_ratio = sentiment_data.get('positive_ratio', 0)
        negative_ratio = sentiment_data.get('negative_ratio', 0)
        
        normalized_sentiment = (avg_sentiment + 1) / 2
        
        score = (normalized_sentiment * 0.6 + positive_ratio * 0.4 - negative_ratio * 0.3)
        
        return max(0, min(100, score * 100))

    def _calculate_professionalism_score(
        self,
        digital_footprints: List[Dict],
        content_analyses: List[Dict]
    ) -> float:
        score = 70.0
        
        for footprint in digital_footprints:
            if footprint.get('platform') == 'linkedin':
                if footprint.get('bio'):
                    score += 10
                if footprint.get('follower_count', 0) > 100:
                    score += 5
        
        profanity_count = sum(1 for c in content_analyses if c.get('contains_profanity', 0) > 0)
        score -= profanity_count * 5
        
        return max(0, min(100, score))

    def _calculate_digital_ethics_score(
        self,
        sentiment_data: Dict,
        content_analyses: List[Dict]
    ) -> float:
        score = 80.0
        
        hate_speech_count = sentiment_data.get('total_hate_speech', 0)
        profanity_count = sentiment_data.get('total_profanity', 0)
        
        score -= hate_speech_count * 20
        score -= profanity_count * 5
        
        negative_ratio = sentiment_data.get('negative_ratio', 0)
        if negative_ratio > 0.3:
            score -= (negative_ratio - 0.3) * 50
        
        return max(0, min(100, score))

    def _calculate_social_score(self, digital_footprints: List[Dict]) -> float:
        if not digital_footprints:
            return 50.0
        
        score = 60.0
        
        active_platforms = len(digital_footprints)
        score += min(active_platforms * 5, 20)
        
        total_followers = sum(fp.get('follower_count', 0) for fp in digital_footprints)
        if total_followers > 1000:
            score += 10
        elif total_followers > 500:
            score += 5
        
        total_posts = sum(fp.get('post_count', 0) for fp in digital_footprints)
        if total_posts > 100:
            score += 10
        elif total_posts > 50:
            score += 5
        
        return min(100, score)

    def _identify_risk_flags(self, sentiment_data: Dict, content_analyses: List[Dict]) -> Dict:
        flags = {}
        
        if sentiment_data.get('total_hate_speech', 0) > 0:
            flags['hate_speech'] = {
                'severity': 'critical',
                'count': sentiment_data['total_hate_speech'],
                'description': 'Konten mengandung ujaran kebencian'
            }
        
        if sentiment_data.get('total_profanity', 0) >= self.risk_thresholds['profanity_count']:
            flags['excessive_profanity'] = {
                'severity': 'high',
                'count': sentiment_data['total_profanity'],
                'description': 'Penggunaan kata kasar berlebihan'
            }
        
        if sentiment_data.get('negative_ratio', 0) >= self.risk_thresholds['negative_ratio']:
            flags['high_negativity'] = {
                'severity': 'medium',
                'ratio': sentiment_data['negative_ratio'],
                'description': 'Konten negatif dominan'
            }
        
        political_content = sentiment_data.get('total_political', 0)
        if political_content > 10:
            flags['political_activity'] = {
                'severity': 'low',
                'count': political_content,
                'description': 'Aktivitas politik terdeteksi (perlu review manual)'
            }
        
        return flags

    def _identify_positive_indicators(
        self,
        sentiment_data: Dict,
        digital_footprints: List[Dict]
    ) -> Dict:
        indicators = {}
        
        if sentiment_data.get('positive_ratio', 0) > 0.6:
            indicators['positive_communication'] = {
                'score': sentiment_data['positive_ratio'],
                'description': 'Komunikasi positif dan konstruktif'
            }
        
        if sentiment_data.get('total_profanity', 0) == 0 and sentiment_data.get('total_hate_speech', 0) == 0:
            indicators['clean_digital_record'] = {
                'description': 'Jejak digital bersih tanpa konten negatif'
            }
        
        professional_platforms = [fp for fp in digital_footprints if fp.get('platform') == 'linkedin']
        if professional_platforms:
            indicators['professional_presence'] = {
                'platforms': len(professional_platforms),
                'description': 'Memiliki kehadiran di platform profesional'
            }
        
        total_engagement = sum(fp.get('follower_count', 0) + fp.get('following_count', 0) 
                              for fp in digital_footprints)
        if total_engagement > 1000:
            indicators['good_social_engagement'] = {
                'score': total_engagement,
                'description': 'Engagement sosial media yang baik'
            }
        
        return indicators

    def _determine_recommendation(self, overall_score: float, risk_flags: Dict) -> str:
        if risk_flags.get('hate_speech'):
            return RecommendationStatus.TIDAK_LAYAK.value
        
        critical_flags = [f for f in risk_flags.values() if f.get('severity') == 'critical']
        if critical_flags:
            return RecommendationStatus.TIDAK_LAYAK.value
        
        high_flags = [f for f in risk_flags.values() if f.get('severity') == 'high']
        if high_flags:
            return RecommendationStatus.DIPERTIMBANGKAN.value
        
        if overall_score >= 75:
            return RecommendationStatus.LAYAK.value
        elif overall_score >= 60:
            return RecommendationStatus.DIPERTIMBANGKAN.value
        else:
            return RecommendationStatus.TIDAK_LAYAK.value

    def _generate_recommendation_reason(
        self,
        overall_score: float,
        risk_flags: Dict,
        positive_indicators: Dict
    ) -> str:
        reasons = []
        
        reasons.append(f"Skor keseluruhan: {overall_score:.1f}/100")
        
        if risk_flags:
            reasons.append(f"Ditemukan {len(risk_flags)} indikator risiko:")
            for flag_name, flag_data in risk_flags.items():
                reasons.append(f"  - {flag_data['description']} (Tingkat: {flag_data['severity']})")
        
        if positive_indicators:
            reasons.append(f"Indikator positif: {len(positive_indicators)}")
            for indicator_name, indicator_data in positive_indicators.items():
                reasons.append(f"  + {indicator_data['description']}")
        
        return "\n".join(reasons)
