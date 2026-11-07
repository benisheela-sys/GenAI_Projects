import pyautogui
import pyperclip
import pandas as pd
import subprocess
import time
import os
import re

from datetime import datetime

print("Starting the Playwright daily Gold rate report automation script...")
print(f"Script started at: {datetime.now()}")

# =====================================
# Step 1 - Open Chrome
# =====================================

print("Opening Chrome...")

pyautogui.press("win")
time.sleep(1)

pyautogui.write("chrome", interval=0.05)
pyautogui.press("enter")

time.sleep(4)

# =====================================
# Step 2 - Open Website
# =====================================

url = "https://www.livechennai.com/gold_silverrate.asp"

pyautogui.write(url, interval=0.02)
pyautogui.press("enter")

print("Loading website...")
time.sleep(8)

# =====================================
# Step 3 - Copy Page Contents
# =====================================

pyautogui.hotkey("ctrl", "a")
time.sleep(2)

pyautogui.hotkey("ctrl", "c")
time.sleep(3)

clipboard_text = pyperclip.paste()

print("Web page copied to clipboard")

# Optional - Save clipboard text for debugging
with open("clipboard_content.txt", "w", encoding="utf-8") as f:
    f.write(clipboard_text)

# =====================================
# Step 4 - Extract Gold Rate
# =====================================

today_rate = "Not Found"
yesterday_rate = "Not Found"

# Example text:
# Today's 22K Rate
# ₹13,160
# Yesterday Rate
# ₹13,140

today_match = re.search(
    r"Today's\s*22K\s*Rate\s*₹?\s*([\d,]+)",
    clipboard_text,
    re.IGNORECASE
)

yesterday_match = re.search(
    r"Yesterday\s*Rate\s*₹?\s*([\d,]+)",
    clipboard_text,
    re.IGNORECASE
)

if today_match:
    today_rate = today_match.group(1)

if yesterday_match:
    yesterday_rate = yesterday_match.group(1)

print("Today's Rate :", today_rate)
print("Yesterday Rate :", yesterday_rate)

# =====================================
# Step 5 - Create Row
# =====================================

now = datetime.now()

comment = "Today's Chennai gold rate update"

new_row = {
    "DateTime": now.strftime("%Y-%m-%d %H:%M:%S"),
    "Today_22K_Rate": today_rate,
    "Yesterday_Rate": yesterday_rate,
    "Comment": comment
}

# =====================================
# Step 6 - Save Excel
# =====================================

excel_file = (
    f"daily_report_{now.strftime('%Y-%m-%d')}.xlsx"
)

try:

    if os.path.exists(excel_file):

        existing_df = pd.read_excel(excel_file)

        updated_df = pd.concat(
            [existing_df, pd.DataFrame([new_row])],
            ignore_index=True
        )

    else:

        updated_df = pd.DataFrame([new_row])

    updated_df.to_excel(
        excel_file,
        index=False
    )

    print(f"Excel Saved : {excel_file}")

except PermissionError:

    print(
        "Close the Excel file and run again."
    )
    raise SystemExit()



# =====================================
# Step 7 - Open Excel
# =====================================

subprocess.Popen(
    ["start", excel_file],
    shell=True
)

print("Opening Excel...")
time.sleep(8)

# =====================================
# Step 8 - Screenshot
# =====================================

screenshot_file = (
    f"excel_report_{now.strftime('%Y-%m-%d_%H-%M-%S')}.png"
)

pyautogui.screenshot(screenshot_file)

print(f"Screenshot Saved : {screenshot_file}")

print("Process Completed Successfully")

print(f"Script completed at: {datetime.now()}")