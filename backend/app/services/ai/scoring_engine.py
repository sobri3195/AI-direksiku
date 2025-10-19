from typing import Dict, List, Tuple
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

        # Tuned thresholds and defaults
        self.risk_thresholds = {
            'profanity_count': 3,
            'hate_speech_count': 1,
            'negative_ratio': 0.5,
            'low_engagement': 0.005,  # engagement rate threshold
            'keyword_spam_ratio': 0.5,
            'link_spam_ratio': 0.3,
            'caps_ratio_flag': 0.2,
        }

        self.professional_keywords = {
            'integritas', 'profesional', 'profesionalisme', 'akuntabilitas',
            'transparansi', 'melayani', 'pelayanan', 'merit', 'inovasi',
            'disiplin', 'etika', 'kepemimpinan', 'kolaborasi', 'publik'
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
        social_score, engagement_insights = self._calculate_social_score(digital_footprints)

        overall_score = (
            sentiment_score * self.weights['sentiment'] +
            professionalism_score * self.weights['professionalism'] +
            digital_ethics_score * self.weights['digital_ethics'] +
            social_score * self.weights['social']
        )

        # Insights and flags
        keyword_stats = self._aggregate_keywords(content_analyses)
        risk_flags = self._identify_risk_flags(sentiment_data, content_analyses, engagement_insights, keyword_stats)
        positive_indicators = self._identify_positive_indicators(sentiment_data, digital_footprints, engagement_insights, keyword_stats)

        recommendation = self._determine_recommendation(overall_score, risk_flags)
        recommendation_reason = self._generate_recommendation_reason(
            overall_score, risk_flags, positive_indicators
        )

        insights = {
            'engagement': engagement_insights,
            'language': {
                'primary': sentiment_data.get('primary_language', 'unknown'),
                'distribution': sentiment_data.get('language_distribution', {})
            },
            'keywords_top': keyword_stats.get('top_keywords', []),
            'avg_confidence': sentiment_data.get('avg_confidence', 0.0),
            'avg_toxicity': sentiment_data.get('avg_toxicity', 0.0),
        }

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
            'positive_indicators': positive_indicators,
            'insights': insights,
        }

    def _calculate_sentiment_score(self, sentiment_data: Dict) -> float:
        avg_sentiment = sentiment_data.get('average_sentiment', 0.0)
        positive_ratio = sentiment_data.get('positive_ratio', 0.0)
        negative_ratio = sentiment_data.get('negative_ratio', 0.0)
        avg_confidence = sentiment_data.get('avg_confidence', 0.0)
        avg_toxicity = sentiment_data.get('avg_toxicity', 0.0)

        normalized_sentiment = (avg_sentiment + 1) / 2

        # Confidence slightly boosts, toxicity slightly penalizes
        score = (
            normalized_sentiment * 0.55 +
            positive_ratio * 0.35 -
            negative_ratio * 0.25 +
            avg_confidence * 0.05 -
            avg_toxicity * 0.10
        )

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

        # Reward presence of professional vocabulary and politeness
        prof_kw_total = sum(c.get('professional_keywords_count', 0) for c in content_analyses)
        polite_kw_total = sum(c.get('politeness_keywords_count', 0) for c in content_analyses)
        score += min(10, (prof_kw_total * 1.0) + (polite_kw_total * 0.5))

        # Penalize spammy behavior
        spam_hits = sum(1 for c in content_analyses if c.get('spam_indicator', 0) == 1)
        score -= min(10, spam_hits * 2)

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

        negative_ratio = sentiment_data.get('negative_ratio', 0.0)
        if negative_ratio > 0.3:
            score -= (negative_ratio - 0.3) * 50

        # Extra ethical penalties/bonuses
        avg_toxicity = sentiment_data.get('avg_toxicity', 0.0)
        if avg_toxicity > 0.6:
            score -= 10
        elif avg_toxicity < 0.1:
            score += 2

        links_ratio = sentiment_data.get('contains_links_ratio', 0.0)
        if links_ratio > 0.5:
            score -= 5

        caps_ratio_over = sentiment_data.get('excessive_caps_ratio', 0.0)
        if caps_ratio_over > 0.3:
            score -= 3

        return max(0, min(100, score))

    def _calculate_social_score(self, digital_footprints: List[Dict]) -> Tuple[float, Dict]:
        if not digital_footprints:
            return 50.0, {
                'active_platforms': 0,
                'total_followers': 0,
                'total_posts': 0,
                'engagement_rate': 0.0,
                'follower_following_ratio': 0.0,
                'total_engagements': 0,
                'total_possible': 0,
            }

        score = 60.0

        active_platforms = len(digital_footprints)
        score += min(active_platforms * 5, 20)

        total_followers = sum(fp.get('follower_count', 0) for fp in digital_footprints)
        total_following = sum(fp.get('following_count', 0) for fp in digital_footprints)
        if total_followers > 1000:
            score += 10
        elif total_followers > 500:
            score += 5

        total_posts = sum(fp.get('post_count', 0) for fp in digital_footprints)
        if total_posts > 100:
            score += 10
        elif total_posts > 50:
            score += 5

        # Compute engagement metrics when possible
        total_engagements = 0
        total_possible = 0
        for fp in digital_footprints:
            followers = fp.get('follower_count', 0)
            posts = fp.get('posts_data', [])
            if isinstance(posts, list) and posts:
                for p in posts:
                    if isinstance(p, dict):
                        likes = p.get('likes', 0)
                        comments = p.get('comments', 0)
                        retweets = p.get('retweets', 0)
                        replies = p.get('replies', 0)
                        shares = p.get('shares', 0)
                        total_engagements += (likes + comments + retweets + replies + shares)
                total_possible += max(followers, 1) * len(posts)

        engagement_rate = (total_engagements / total_possible) if total_possible > 0 else 0.0
        if engagement_rate > 0.05:
            score += 10
        elif engagement_rate > 0.02:
            score += 5
        elif engagement_rate < 0.001 and total_posts > 50:
            score -= 5

        follower_following_ratio = (total_followers / max(total_following, 1)) if total_following else (total_followers or 0)
        if follower_following_ratio < 0.3 and total_posts > 100:
            score -= 5

        insights = {
            'active_platforms': active_platforms,
            'total_followers': total_followers,
            'total_posts': total_posts,
            'engagement_rate': round(engagement_rate, 4),
            'follower_following_ratio': round(follower_following_ratio, 2) if isinstance(follower_following_ratio, float) else follower_following_ratio,
            'total_engagements': total_engagements,
            'total_possible': total_possible,
        }

        return min(100, score), insights

    def _aggregate_keywords(self, content_analyses: List[Dict]) -> Dict:
        freq: Dict[str, int] = {}
        total_keywords = 0
        for c in content_analyses:
            kws = c.get('keywords', []) or []
            for k in kws:
                if not isinstance(k, str):
                    continue
                total_keywords += 1
                freq[k] = freq.get(k, 0) + 1
        top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
        top_ratio = (top[0][1] / total_keywords) if top and total_keywords > 0 else 0.0
        return {
            'freq': freq,
            'total': total_keywords,
            'top_keywords': top,
            'top_ratio': top_ratio,
        }

    def _identify_risk_flags(self, sentiment_data: Dict, content_analyses: List[Dict], engagement_insights: Dict, keyword_stats: Dict) -> Dict:
        flags: Dict[str, Dict] = {}

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

        # New risk flags
        if engagement_insights.get('engagement_rate', 0.0) < self.risk_thresholds['low_engagement'] and engagement_insights.get('total_posts', 0) > 20:
            flags['low_engagement'] = {
                'severity': 'low',
                'rate': engagement_insights.get('engagement_rate', 0.0),
                'description': 'Engagement sosial media rendah'
            }

        if sentiment_data.get('primary_language') and sentiment_data.get('primary_language') != 'id':
            flags['language_mismatch'] = {
                'severity': 'low',
                'primary_language': sentiment_data.get('primary_language'),
                'description': 'Mayoritas konten tidak berbahasa Indonesia'
            }

        if sentiment_data.get('contains_links_ratio', 0.0) > self.risk_thresholds['link_spam_ratio']:
            flags['link_spam'] = {
                'severity': 'low',
                'ratio': sentiment_data.get('contains_links_ratio', 0.0),
                'description': 'Konten banyak mengandung tautan (indikasi promosi/spam)'
            }

        if sentiment_data.get('excessive_caps_ratio', 0.0) > self.risk_thresholds['caps_ratio_flag'] and sentiment_data.get('exclamation_avg', 0.0) > 1.0:
            flags['shouting'] = {
                'severity': 'low',
                'description': 'Gaya komunikasi cenderung berteriak (huruf besar/eksklamasi)'
            }

        if keyword_stats.get('top_ratio', 0.0) > self.risk_thresholds['keyword_spam_ratio'] and keyword_stats.get('total', 0) >= 10:
            flags['keyword_spam'] = {
                'severity': 'low',
                'ratio': keyword_stats.get('top_ratio'),
                'top_keyword': keyword_stats.get('top_keywords', [(None, 0)])[0][0],
                'description': 'Kata kunci yang sama mendominasi (indikasi spam)'
            }

        avg_toxicity = sentiment_data.get('avg_toxicity', 0.0)
        if avg_toxicity > 0.5:
            flags['toxicity_high'] = {
                'severity': 'medium',
                'score': avg_toxicity,
                'description': 'Tingkat toksisitas tinggi'
            }

        return flags

    def _identify_positive_indicators(
        self,
        sentiment_data: Dict,
        digital_footprints: List[Dict],
        engagement_insights: Dict,
        keyword_stats: Dict
    ) -> Dict:
        indicators: Dict[str, Dict] = {}

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

        if engagement_insights.get('engagement_rate', 0.0) > 0.02:
            indicators['engagement_quality'] = {
                'rate': engagement_insights.get('engagement_rate'),
                'description': 'Kualitas engagement yang baik'
            }

        ratio = engagement_insights.get('follower_following_ratio', 1.0) or 0
        if 0.5 <= ratio <= 2.0:
            indicators['balanced_network'] = {
                'ratio': ratio,
                'description': 'Rasio pengikut vs mengikuti yang seimbang'
            }

        if sentiment_data.get('primary_language') == 'id':
            indicators['language_consistency'] = {
                'description': 'Mayoritas konten berbahasa Indonesia'
            }

        if keyword_stats.get('total', 0) >= 20 and keyword_stats.get('top_ratio', 0.0) < 0.4:
            indicators['content_diversity'] = {
                'description': 'Konten beragam tanpa dominasi kata kunci tertentu'
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
        reasons: List[str] = []

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
