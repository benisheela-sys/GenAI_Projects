
The program should perform the following tasks:

1. Launch Google Chrome automatically.
2. Navigate to the Live Chennai Gold Rate webpage: https://www.livechennai.com/gold_silverrate.asp
3. Read the gold rate information that has been copied to the clipboard. The text will be in a format similar to:
Today's 22K Rate
₹13,160
Yesterday Rate
₹13,140

4. Extract the relevant gold rate values from the clipboard data.
5. Create an Excel report and store the extracted information.
6. If the Excel file already exists, append the new data as a new row instead of overwriting the existing records.
7. Each row should contain:
- Current date and time
- Today's 22K gold rate
- Yesterday's gold rate
- A short comment (for example: "Today's Chennai gold rate update")
8. Save the Excel file using today's date in the filename, such as: daily_report_2026-11-07.xlsx
9. Open the saved Excel file automatically.
10. Capture a screenshot of the final Excel report and save it as an image file.
11. Display a success message after the entire process is completed.
The solution should use Python libraries such as:

- PyAutoGUI
- Pyperclip
- Pandas
- OpenPyXL
The program should also include basic error handling for scenarios such as:

- Excel file already being open
- Empty clipboard data
- Missing gold rate information
- File save errors
