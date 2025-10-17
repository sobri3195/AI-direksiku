from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
from app.core.config import settings


class SocialMediaScraper:
    def __init__(self):
        self.timeout = settings.SCRAPING_TIMEOUT
        self.max_pages = settings.MAX_SCRAPING_PAGES
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_candidate_profiles(
        self,
        linkedin_url: Optional[str] = None,
        twitter_username: Optional[str] = None,
        facebook_url: Optional[str] = None,
        instagram_username: Optional[str] = None
    ) -> List[Dict]:
        results = []
        
        if linkedin_url:
            linkedin_data = self._scrape_linkedin_mock(linkedin_url)
            if linkedin_data:
                results.append(linkedin_data)
        
        if twitter_username:
            twitter_data = self._scrape_twitter_mock(twitter_username)
            if twitter_data:
                results.append(twitter_data)
        
        if facebook_url:
            facebook_data = self._scrape_facebook_mock(facebook_url)
            if facebook_data:
                results.append(facebook_data)
        
        if instagram_username:
            instagram_data = self._scrape_instagram_mock(instagram_username)
            if instagram_data:
                results.append(instagram_data)
        
        return results

    def _scrape_linkedin_mock(self, url: str) -> Optional[Dict]:
        try:
            username = url.split('/')[-1] if '/' in url else url
            
            return {
                'platform': 'linkedin',
                'profile_url': url,
                'username': username,
                'display_name': f'Professional {username.title()}',
                'bio': 'Experienced professional with expertise in public administration and digital transformation. Committed to excellence and integrity in public service.',
                'follower_count': 450,
                'following_count': 320,
                'post_count': 78,
                'profile_data': {
                    'experience': [
                        {
                            'title': 'Senior Administrator',
                            'company': 'Government Agency',
                            'duration': '2020-Present'
                        }
                    ],
                    'education': [
                        {
                            'degree': 'Master in Public Administration',
                            'institution': 'University of Indonesia',
                            'year': 2019
                        }
                    ],
                    'skills': ['Public Policy', 'Digital Government', 'Leadership', 'Data Analysis']
                },
                'posts_data': [
                    {
                        'text': 'Excited to contribute to digital transformation in public sector. Innovation and integrity are key.',
                        'date': '2024-01-15',
                        'likes': 45,
                        'comments': 8
                    },
                    {
                        'text': 'Attended workshop on e-government solutions. Great insights on improving public service delivery.',
                        'date': '2024-01-10',
                        'likes': 32,
                        'comments': 5
                    },
                    {
                        'text': 'Proud to be part of civil service modernization efforts. Together we build better governance.',
                        'date': '2024-01-05',
                        'likes': 67,
                        'comments': 12
                    }
                ],
                'scraped_at': datetime.utcnow(),
                'scraping_status': 'completed'
            }
        except Exception as e:
            return {
                'platform': 'linkedin',
                'profile_url': url,
                'scraped_at': datetime.utcnow(),
                'scraping_status': 'error',
                'scraping_error': str(e)
            }

    def _scrape_twitter_mock(self, username: str) -> Optional[Dict]:
        try:
            username = username.replace('@', '')
            
            return {
                'platform': 'twitter',
                'profile_url': f'https://twitter.com/{username}',
                'username': username,
                'display_name': f'@{username}',
                'bio': 'Public servant | Digital enthusiast | Building better Indonesia 🇮🇩',
                'follower_count': 1250,
                'following_count': 380,
                'post_count': 234,
                'profile_data': {
                    'verified': False,
                    'location': 'Jakarta, Indonesia',
                    'joined_date': '2020-03-15'
                },
                'posts_data': [
                    {
                        'text': 'Pagi yang produktif! Semangat untuk melayani masyarakat dengan sepenuh hati.',
                        'date': '2024-01-16',
                        'likes': 23,
                        'retweets': 5,
                        'replies': 3
                    },
                    {
                        'text': 'Inovasi digital adalah kunci meningkatkan kualitas pelayanan publik. Mari kita dukung transformasi ini!',
                        'date': '2024-01-14',
                        'likes': 45,
                        'retweets': 12,
                        'replies': 7
                    },
                    {
                        'text': 'Terima kasih atas kepercayaan dan dukungannya. Akan terus bekerja dengan integritas.',
                        'date': '2024-01-12',
                        'likes': 67,
                        'retweets': 8,
                        'replies': 15
                    },
                    {
                        'text': 'Senang bisa berdiskusi dengan rekan-rekan tentang reformasi birokrasi. Banyak ide menarik!',
                        'date': '2024-01-10',
                        'likes': 34,
                        'retweets': 6,
                        'replies': 9
                    }
                ],
                'scraped_at': datetime.utcnow(),
                'scraping_status': 'completed'
            }
        except Exception as e:
            return {
                'platform': 'twitter',
                'username': username,
                'scraped_at': datetime.utcnow(),
                'scraping_status': 'error',
                'scraping_error': str(e)
            }

    def _scrape_facebook_mock(self, url: str) -> Optional[Dict]:
        try:
            username = url.split('/')[-1] if '/' in url else url
            
            return {
                'platform': 'facebook',
                'profile_url': url,
                'username': username,
                'display_name': username.replace('.', ' ').title(),
                'bio': 'ASN | Pelayan Publik | Indonesia',
                'follower_count': 890,
                'following_count': 450,
                'post_count': 156,
                'profile_data': {
                    'location': 'Jakarta',
                    'work': 'Government Institution',
                    'education': 'State University'
                },
                'posts_data': [
                    {
                        'text': 'Alhamdulillah, program pelayanan digital kami mendapat apresiasi positif dari masyarakat. Terima kasih atas dukungannya!',
                        'date': '2024-01-15',
                        'likes': 56,
                        'comments': 12,
                        'shares': 4
                    },
                    {
                        'text': 'Kebersamaan dengan keluarga di akhir pekan. Family time yang berkualitas.',
                        'date': '2024-01-13',
                        'likes': 89,
                        'comments': 23,
                        'shares': 0
                    },
                    {
                        'text': 'Workshop hari ini sangat bermanfaat. Belajar banyak tentang inovasi pelayanan publik.',
                        'date': '2024-01-11',
                        'likes': 45,
                        'comments': 8,
                        'shares': 3
                    }
                ],
                'scraped_at': datetime.utcnow(),
                'scraping_status': 'completed'
            }
        except Exception as e:
            return {
                'platform': 'facebook',
                'profile_url': url,
                'scraped_at': datetime.utcnow(),
                'scraping_status': 'error',
                'scraping_error': str(e)
            }

    def _scrape_instagram_mock(self, username: str) -> Optional[Dict]:
        try:
            username = username.replace('@', '')
            
            return {
                'platform': 'instagram',
                'profile_url': f'https://instagram.com/{username}',
                'username': username,
                'display_name': username,
                'bio': '🇮🇩 Public Servant | 📚 Lifelong Learner | 💼 Professional',
                'follower_count': 2340,
                'following_count': 567,
                'post_count': 189,
                'profile_data': {
                    'verified': False,
                    'private': False,
                    'posts': 189
                },
                'posts_data': [
                    {
                        'text': 'Pagi yang indah untuk memulai hari dengan semangat baru! #PublicService #Indonesia',
                        'date': '2024-01-16',
                        'likes': 234,
                        'comments': 18
                    },
                    {
                        'text': 'Bersyukur bisa berkontribusi untuk negeri. Setiap hari adalah kesempatan untuk berbuat baik. #ASN #Integritas',
                        'date': '2024-01-14',
                        'likes': 345,
                        'comments': 28
                    },
                    {
                        'text': 'Weekend with family 👨‍👩‍👧‍👦 #FamilyTime #Blessed',
                        'date': '2024-01-13',
                        'likes': 456,
                        'comments': 34
                    }
                ],
                'scraped_at': datetime.utcnow(),
                'scraping_status': 'completed'
            }
        except Exception as e:
            return {
                'platform': 'instagram',
                'username': username,
                'scraped_at': datetime.utcnow(),
                'scraping_status': 'error',
                'scraping_error': str(e)
            }

    def extract_posts_text(self, footprints: List[Dict]) -> List[str]:
        all_texts = []
        
        for footprint in footprints:
            posts_data = footprint.get('posts_data', [])
            if isinstance(posts_data, list):
                for post in posts_data:
                    if isinstance(post, dict) and 'text' in post:
                        all_texts.append(post['text'])
            
            bio = footprint.get('bio')
            if bio:
                all_texts.append(bio)
        
        return all_texts
