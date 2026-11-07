from playwright.sync_api import sync_playwright, TimeoutError
from datetime import datetime

print("Starting the Playwright automation script...")
print(f"Script started at: {datetime.now()}")

# Live Cricket Score Bot
# Chromium --> Cricbuzz --> Extract the score --> Screen shot --> Final text file

with sync_playwright() as p:
    
    print("Launching the Chromium browser...")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    try:
        print("Navigating to the Cricbuzz website...")

        page.goto(
            "https://www.cricbuzz.com/live-cricket-scores/170687/sl-vs-pak-1st-t20i-sri-lanka-tour-of-pakistan-2026",
            wait_until="domcontentloaded"
        )

        print("Waiting for the cricket score to appear...")

        # Wait for the score element instead of using fixed sleep
        page.locator(
            "div.bg-white.flex.justify-between.items-center.px-4.py-2"
        ).wait_for(state="visible", timeout=20000)

        print("Taking the Cricbuzz screenshot...")
        page.screenshot(path="score.png", full_page=True)

        print("Extracting the cricket score...")

        score = page.locator(
            "div.bg-white.flex.justify-between.items-center.px-4.py-2"
        ).inner_text()

        print(f"Cricket Score Report:\n{score}")

        print("Saving the cricket score to a text file...")

        with open("cricket_score.txt", "w", encoding="utf-8") as file:
            file.write(f"Cricbuzz Score Report - {datetime.now()}\n")
            file.write("----------------------------------------\n")
            file.write(score)

        print("Cricket score saved successfully!")
        print("Screenshot saved as score.png")

    except TimeoutError:
        print("No cricket score found.")
        print("The match may not be available or the page timed out.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Closing the browser...")
        browser.close

print(f"Script completed at: {datetime.now()}")