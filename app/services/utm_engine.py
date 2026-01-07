from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

class UTMEngine:
    @staticmethod
    def inject_utms(html: str, campaign: str, user_type: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', href=True):
            url_parts = list(urlparse(a['href']))
            query = dict(parse_qsl(url_parts[4]))
            query.update({
                "utm_source": "bulk_engine",
                "utm_medium": "email",
                "utm_campaign": campaign,
                "utm_term": user_type
            })
            url_parts[4] = urlencode(query)
            a['href'] = urlunparse(url_parts)
        return str(soup)