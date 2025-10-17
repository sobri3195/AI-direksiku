import pytest
from app.services.ai.sentiment_analyzer import SentimentAnalyzer
from app.services.ai.scoring_engine import ScoringEngine


def test_sentiment_analyzer():
    analyzer = SentimentAnalyzer()
    
    positive_text = "Saya sangat senang dan bangga bisa melayani masyarakat dengan baik"
    result = analyzer.analyze_text(positive_text)
    
    assert result['sentiment_label'] in ['positive', 'neutral', 'negative']
    assert 'sentiment_score' in result
    assert 'confidence' in result
    assert 'contains_profanity' in result


def test_sentiment_analyzer_profanity():
    analyzer = SentimentAnalyzer()
    
    profane_text = "Ini adalah teks yang mengandung kata anjing"
    result = analyzer.analyze_text(profane_text)
    
    assert result['contains_profanity'] == 1


def test_sentiment_batch_analysis():
    analyzer = SentimentAnalyzer()
    
    texts = [
        "Hari ini sangat menyenangkan",
        "Saya kecewa dengan pelayanan",
        "Bekerja dengan profesional"
    ]
    
    results = analyzer.analyze_batch(texts)
    assert len(results) == 3
    assert all('sentiment_label' in r for r in results)


def test_aggregate_sentiment():
    analyzer = SentimentAnalyzer()
    
    analyses = [
        {'sentiment_label': 'positive', 'sentiment_score': 0.8, 'contains_profanity': 0, 'contains_hate_speech': 0, 'contains_political_content': 0},
        {'sentiment_label': 'negative', 'sentiment_score': -0.5, 'contains_profanity': 0, 'contains_hate_speech': 0, 'contains_political_content': 0},
        {'sentiment_label': 'neutral', 'sentiment_score': 0.1, 'contains_profanity': 0, 'contains_hate_speech': 0, 'contains_political_content': 0},
    ]
    
    aggregate = analyzer.calculate_aggregate_sentiment(analyses)
    
    assert 'average_sentiment' in aggregate
    assert 'positive_ratio' in aggregate
    assert 'negative_ratio' in aggregate
    assert aggregate['positive_ratio'] > 0


def test_scoring_engine():
    engine = ScoringEngine()
    
    sentiment_data = {
        'average_sentiment': 0.5,
        'positive_ratio': 0.7,
        'negative_ratio': 0.1,
        'neutral_ratio': 0.2,
        'total_profanity': 0,
        'total_hate_speech': 0,
        'total_political': 2
    }
    
    digital_footprints = [
        {'platform': 'linkedin', 'follower_count': 500, 'post_count': 50, 'bio': 'Professional'},
        {'platform': 'twitter', 'follower_count': 300, 'post_count': 100}
    ]
    
    content_analyses = [
        {'contains_profanity': 0, 'contains_hate_speech': 0},
        {'contains_profanity': 0, 'contains_hate_speech': 0}
    ]
    
    result = engine.calculate_overall_score(sentiment_data, digital_footprints, content_analyses)
    
    assert 'overall_score' in result
    assert 0 <= result['overall_score'] <= 100
    assert 'recommendation' in result
    assert result['recommendation'] in ['layak', 'dipertimbangkan', 'tidak_layak']


def test_scoring_with_risk_flags():
    engine = ScoringEngine()
    
    sentiment_data = {
        'average_sentiment': -0.3,
        'positive_ratio': 0.2,
        'negative_ratio': 0.6,
        'neutral_ratio': 0.2,
        'total_profanity': 5,
        'total_hate_speech': 1,
        'total_political': 0
    }
    
    digital_footprints = []
    content_analyses = []
    
    result = engine.calculate_overall_score(sentiment_data, digital_footprints, content_analyses)
    
    assert result['recommendation'] == 'tidak_layak'
    assert len(result['risk_flags']) > 0
