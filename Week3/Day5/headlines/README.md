# BBC News Top Headlines Scraper

## About the Project
This project is a lightweight Python web scraper that fetches and prints the top 5 headlines from [BBC News](https://www.bbc.com/news). 

It combines **Playwright** (to render the webpage in a headless Chromium browser and handle dynamically loaded content) with **BeautifulSoup4** (to parse the HTML and extract clean headline text).

---

## Prerequisites
* Python 3.8 or higher
* `pip` (Python package manager)

---

## Execution Steps

### 1. Clone or Save the Project
Save your Python script as `bbc_scraper.py` (make sure `url = "https://www.bbc.com/news"` is set in the script).

### 2. (Optional) Create a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate