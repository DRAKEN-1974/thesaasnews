from datetime import datetime
from urllib.parse import urljoin
import re

class DataProcessor:
    def __init__(self, base_url):
        self.base_url = base_url

    def clean_article(self, article):
        headline = re.sub('<[^<]+?>', '', article['headline']).strip()
        url = article['url']
        if not url.startswith('http'):
            url = urljoin(self.base_url, url)
        try:
            pub_date = datetime.fromisoformat(article['publication_date'])
        except Exception:
            pub_date = datetime.now()
        category = article['category'].strip()
        return {
            "headline": headline,
            "url": url,
            "publication_date": pub_date,
            "category": category
        }

    def process_articles(self, articles):
        processed = [self.clean_article(a) for a in articles]
        return processed

    def compute_statistics(self, articles):
        stats = {}
        for a in articles:
            cat = a['category']
            stats[cat] = stats.get(cat, 0) + 1
        return [{"category": k, "count": v} for k, v in stats.items()]