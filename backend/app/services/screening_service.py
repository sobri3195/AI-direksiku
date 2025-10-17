from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.models.screening import ScreeningResult, DigitalFootprint, SentimentAnalysis
from app.services.scraping.social_media_scraper import SocialMediaScraper
from app.services.ai.sentiment_analyzer import SentimentAnalyzer
from app.services.ai.scoring_engine import ScoringEngine
from datetime import datetime


class ScreeningService:
    def __init__(self, db: Session):
        self.db = db
        self.scraper = SocialMediaScraper()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.scoring_engine = ScoringEngine()

    def conduct_screening(self, candidate_id: int) -> ScreeningResult:
        candidate = self.db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            raise ValueError(f"Candidate with id {candidate_id} not found")
        
        footprints_data = self.scraper.scrape_candidate_profiles(
            linkedin_url=candidate.linkedin_url,
            twitter_username=candidate.twitter_username,
            facebook_url=candidate.facebook_url,
            instagram_username=candidate.instagram_username
        )
        
        digital_footprints = []
        for footprint_data in footprints_data:
            footprint = DigitalFootprint(
                candidate_id=candidate_id,
                platform=footprint_data.get('platform'),
                profile_url=footprint_data.get('profile_url'),
                username=footprint_data.get('username'),
                display_name=footprint_data.get('display_name'),
                bio=footprint_data.get('bio'),
                follower_count=footprint_data.get('follower_count'),
                following_count=footprint_data.get('following_count'),
                post_count=footprint_data.get('post_count'),
                profile_data=footprint_data.get('profile_data'),
                posts_data=footprint_data.get('posts_data'),
                scraped_at=footprint_data.get('scraped_at', datetime.utcnow()),
                scraping_status=footprint_data.get('scraping_status', 'completed'),
                scraping_error=footprint_data.get('scraping_error')
            )
            self.db.add(footprint)
            digital_footprints.append(footprint_data)
        
        self.db.commit()
        
        posts_text = self.scraper.extract_posts_text(footprints_data)
        
        content_analyses = self.sentiment_analyzer.analyze_batch(posts_text)
        
        sentiment_data = self.sentiment_analyzer.calculate_aggregate_sentiment(content_analyses)
        
        scoring_result = self.scoring_engine.calculate_overall_score(
            sentiment_data=sentiment_data,
            digital_footprints=digital_footprints,
            content_analyses=content_analyses
        )
        
        screening_result = ScreeningResult(
            candidate_id=candidate_id,
            overall_score=scoring_result['overall_score'],
            technical_score=scoring_result['technical_score'],
            social_score=scoring_result['social_score'],
            digital_ethics_score=scoring_result['digital_ethics_score'],
            professionalism_score=scoring_result['professionalism_score'],
            sentiment_score=scoring_result['sentiment_score'],
            positive_content_ratio=scoring_result['positive_content_ratio'],
            negative_content_ratio=scoring_result['negative_content_ratio'],
            neutral_content_ratio=scoring_result['neutral_content_ratio'],
            recommendation=scoring_result['recommendation'],
            recommendation_reason=scoring_result['recommendation_reason'],
            risk_flags=scoring_result['risk_flags'],
            positive_indicators=scoring_result['positive_indicators'],
            ai_analysis_summary=self._generate_summary(scoring_result),
            detailed_report=self._generate_detailed_report(
                candidate, footprints_data, sentiment_data, scoring_result
            ),
            analyzed_at=datetime.utcnow()
        )
        
        self.db.add(screening_result)
        self.db.commit()
        self.db.refresh(screening_result)
        
        for i, (text, analysis) in enumerate(zip(posts_text, content_analyses)):
            platform = self._determine_platform_for_text(text, footprints_data)
            sentiment_record = SentimentAnalysis(
                screening_result_id=screening_result.id,
                platform=platform,
                content_type='post',
                content_text=text[:1000],
                sentiment_label=analysis['sentiment_label'],
                sentiment_score=analysis['sentiment_score'],
                confidence=analysis['confidence'],
                contains_profanity=analysis['contains_profanity'],
                contains_hate_speech=analysis['contains_hate_speech'],
                contains_political_content=analysis['contains_political_content'],
                keywords=analysis.get('keywords', []),
                analyzed_at=datetime.utcnow()
            )
            self.db.add(sentiment_record)
        
        self.db.commit()
        
        candidate.status = f"screened_{scoring_result['recommendation']}"
        self.db.commit()
        
        return screening_result

    def _generate_summary(self, scoring_result: Dict) -> str:
        recommendation = scoring_result['recommendation']
        overall_score = scoring_result['overall_score']
        
        summary_parts = [
            f"Hasil Analisis AI-DiReksi:",
            f"Skor Keseluruhan: {overall_score:.1f}/100",
            f"Rekomendasi: {recommendation.upper()}",
            "",
            "Rincian Skor:",
            f"- Etika Digital: {scoring_result['digital_ethics_score']:.1f}/100",
            f"- Profesionalisme: {scoring_result['professionalism_score']:.1f}/100",
            f"- Sentimen: {scoring_result['sentiment_score']:.1f}/100",
            f"- Sosial: {scoring_result['social_score']:.1f}/100",
            "",
        ]
        
        if scoring_result['risk_flags']:
            summary_parts.append(f"Peringatan: {len(scoring_result['risk_flags'])} indikator risiko terdeteksi")
        
        if scoring_result['positive_indicators']:
            summary_parts.append(f"Indikator Positif: {len(scoring_result['positive_indicators'])} aspek positif teridentifikasi")
        
        return "\n".join(summary_parts)

    def _generate_detailed_report(
        self,
        candidate: Candidate,
        footprints: List[Dict],
        sentiment_data: Dict,
        scoring_result: Dict
    ) -> Dict:
        return {
            'candidate_info': {
                'name': candidate.full_name,
                'email': candidate.email,
                'position': candidate.applied_position,
                'application_date': candidate.application_date.isoformat() if candidate.application_date else None
            },
            'digital_presence': {
                'platforms_analyzed': len(footprints),
                'platforms': [f['platform'] for f in footprints],
                'total_followers': sum(f.get('follower_count', 0) for f in footprints),
                'total_posts_analyzed': sum(f.get('post_count', 0) for f in footprints)
            },
            'sentiment_analysis': {
                'average_sentiment': sentiment_data.get('average_sentiment', 0),
                'positive_ratio': sentiment_data.get('positive_ratio', 0),
                'negative_ratio': sentiment_data.get('negative_ratio', 0),
                'neutral_ratio': sentiment_data.get('neutral_ratio', 0),
                'concerns': {
                    'profanity': sentiment_data.get('total_profanity', 0),
                    'hate_speech': sentiment_data.get('total_hate_speech', 0),
                    'political_content': sentiment_data.get('total_political', 0)
                }
            },
            'scores': {
                'overall': scoring_result['overall_score'],
                'breakdown': {
                    'digital_ethics': scoring_result['digital_ethics_score'],
                    'professionalism': scoring_result['professionalism_score'],
                    'sentiment': scoring_result['sentiment_score'],
                    'social': scoring_result['social_score']
                }
            },
            'recommendation': {
                'status': scoring_result['recommendation'],
                'confidence': 'high' if scoring_result['overall_score'] > 80 or scoring_result['overall_score'] < 40 else 'medium',
                'reason': scoring_result['recommendation_reason']
            },
            'risk_assessment': scoring_result['risk_flags'],
            'positive_factors': scoring_result['positive_indicators'],
            'generated_at': datetime.utcnow().isoformat()
        }

    def _determine_platform_for_text(self, text: str, footprints: List[Dict]) -> str:
        for footprint in footprints:
            if footprint.get('bio') == text:
                return footprint.get('platform', 'unknown')
            
            posts_data = footprint.get('posts_data', [])
            if isinstance(posts_data, list):
                for post in posts_data:
                    if isinstance(post, dict) and post.get('text') == text:
                        return footprint.get('platform', 'unknown')
        
        return 'unknown'
