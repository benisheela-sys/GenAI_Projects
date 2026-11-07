import pyautogui
import pyperclip
import pandas 
from datetime import datetime
from pathlib import Path
import time

# Give yourself time to switch windows
print("Starting in 5 seconds...")
time.sleep(5)

# Open Chrome
pyautogui.press("win")
time.sleep(1)

pyautogui.write("chrome", interval=0.05)
pyautogui.press("enter")

time.sleep(3)

# Open Google News
pyautogui.write("https://news.google.com", interval=0.02)
pyautogui.press("enter")

time.sleep(5)

print("Select a headline and press Ctrl+C within 10 seconds...")
time.sleep(10)

# Read copied text
headline = pyperclip.paste()

if not headline:
    headline = "No headline copied"

# Current date/time
now = datetime.now()

# Comment
comment = "Interesting news update"

# Create dataframe
data = pd.DataFrame(
    [[
        now.strftime("%Y-%m-%d %H:%M:%S"),
        headline,
        comment
    ]],
    columns=["DateTime", "Headline", "Comment"]
)

# Save Excel
excel_file = f"daily_report_{now.strftime('%Y-%m-%d')}.xlsx"
data.to_excel(excel_file, index=False)

print(f"Saved: {excel_file}")

# Screenshot
screenshot_file = f"excel_screenshot_{now.strftime('%Y-%m-%d')}.png"
pyautogui.screenshot(screenshot_file)

print(f"Screenshot saved: {screenshot_file}")