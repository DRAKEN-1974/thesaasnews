import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.thesaasnews.com/"

class Scraper:
    def __init__(self):
        self.base_url = BASE_URL

    async def fetch_page(self, url, session):
        async with session.get(url) as resp:
            return await resp.text()

    async def scrape_articles(self, max_pages=1):
        articles = []
        async with aiohttp.ClientSession() as session:
            url = self.base_url
            for _ in range(max_pages):
                html = await self.fetch_page(url, session)
                soup = BeautifulSoup(html, "html.parser")
                news_cards = soup.select(".news-card, .news-list .news-card")
                for card in news_cards:
                    headline_tag = card.find("h2")
                    url_tag = card.find("a", href=True)
                    date_tag = card.find("time")
                    category_tag = card.find("span", {"class": "category"})
                    headline = headline_tag.text.strip() if headline_tag else ""
                    url_ = urljoin(self.base_url, url_tag['href']) if url_tag else ""
                    date_ = date_tag['datetime'] if date_tag and date_tag.has_attr('datetime') else (date_tag.text if date_tag else "")
                    category = category_tag.text.strip() if category_tag else "Unknown"
                    articles.append({
                        "headline": headline,
                        "url": url_,
                        "publication_date": date_,
                        "category": category
                    })
                # Pagination (improve this as needed)
                next_btn = soup.find("a", text="Next")
                if next_btn and next_btn['href']:
                    url = urljoin(self.base_url, next_btn['href'])
                else:
                    break
        return articles