from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    
def main():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)

        # Create page
        page = browser.new_page()

        # Navigate to website
        page.goto("https://google.com")

        # Print page title
        print("Title:", page.title())

        # Take screenshot
        page.screenshot(path="google.png")

        # Close browser
        browser.close()

if __name__ == "__main__":
    main()