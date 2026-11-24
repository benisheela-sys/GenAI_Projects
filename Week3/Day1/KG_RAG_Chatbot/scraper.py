import json
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress SSL warnings if tn.gov.in has intermediate certificate issues
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.tn.gov.in/"
LIST_URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    )
}


def fetch_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=20, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_schemes(limit: int = 25) -> list[dict]:
    """Scrapes scheme links from the department list page and fetches their details."""
    print(f"Fetching scheme list from: {LIST_URL}")
    soup = fetch_soup(LIST_URL)

    scheme_links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        title = a_tag.get_text(strip=True)
        # Filter for scheme detail links
        if ("scheme_details" in href or "scheme" in href.lower()) and title:
            full_url = urljoin(BASE_URL, href)
            if full_url != LIST_URL and full_url not in [s["url"] for s in scheme_links]:
                scheme_links.append({"title": title, "url": full_url})

    print(f"Found {len(scheme_links)} scheme links. Scraping up to {limit}...")
    schemes = []

    for idx, item in enumerate(scheme_links[:limit], start=1):
        try:
            print(f"[{idx}/{min(len(scheme_links), limit)}] Scraping: {item['title']}")
            detail_soup = fetch_soup(item["url"])

            # Remove scripts, styles, and navigation noise
            for tag in detail_soup(["script", "style", "nav", "header", "footer"]):
                tag.decompose()

            # Extract structured text from main content or tables
            content_blocks = []
            for row in detail_soup.find_all("tr"):
                cells = [c.get_text(" ", strip=True) for c in row.find_all(["th", "td"])]
                cells = [c for c in cells if c]
                if cells:
                    content_blocks.append(" : ".join(cells))

            if not content_blocks:
                content_blocks = [detail_soup.get_text("\n", strip=True)]

            raw_text = "\n".join(content_blocks)
            schemes.append(
                {
                    "title": item["title"],
                    "url": item["url"],
                    "content": f"Scheme Name: {item['title']}\nURL: {item['url']}\nDetails:\n{raw_text}",
                }
            )
            time.sleep(0.5)  # Polite delay
        except Exception as e:
            print(f"Failed to scrape {item['url']}: {e}")

    with open("schemes_data.json", "w", encoding="utf-8") as f:
        json.dump(schemes, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(schemes)} schemes to schemes_data.json")
    return schemes


if __name__ == "__main__":
    scrape_schemes(limit=25)