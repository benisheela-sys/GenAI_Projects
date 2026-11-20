from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_bbc_headlines():
    url = "playwright install"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the page and wait for headlines to render
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector('h2[data-testid="card-headline"]', timeout=15000)

        html = page.content()
        browser.close()

    # Parse HTML with BeautifulSoup4
    soup = BeautifulSoup(html, "html.parser")
    headline_tags = soup.select('h2[data-testid="card-headline"]')

    # Deduplicate and collect the top 5 non-empty headlines
    headlines = []
    for tag in headline_tags:
        text = tag.get_text(strip=True)
        if text and text not in headlines:
            headlines.append(text)
        if len(headlines) == 5:
            break

    for i, headline in enumerate(headlines, start=1):
        print(f"{i}. {headline}")

if __name__ == "__main__":
    fetch_bbc_headlines()