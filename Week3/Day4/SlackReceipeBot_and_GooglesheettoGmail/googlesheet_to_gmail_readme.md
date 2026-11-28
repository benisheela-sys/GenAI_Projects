# GoogleSheet_to_Gmail — Student Welcome Email Automation (n8n)

An end-to-end **n8n** workflow (`GoogleSheet_to_Gmail.json`) that reads student enrollment data from Google Sheets, validates email addresses and required fields, filters out duplicate entries, sends a branded HTML welcome email via Gmail, and updates the spreadsheet with the delivery status (`Yes` or `No`).

---

## Features

* **Automated Sheet Ingestion:** Pulls student records from the `Student_information` spreadsheet (`Info` tab).
* **Duplicate Prevention:** Tracks every processed email address (including previously sent rows) in a JavaScript `Set` so duplicate entries are caught and marked `No`.
* **Data Validation:** Validates `Emailid` formatting with a regular expression and checks that `Name` and `Course` are populated before sending.
* **Re-run Safe (Idempotent):** Skips rows already marked `Email Sent = Yes` so re-running the workflow will never send duplicate welcome emails.
* **Branded HTML Emails:** Formats each message with a clean HTML layout, student enrollment callout box, and sign-off from **Admin - Social Eagle** (with n8n attribution disabled).
* **Automatic Status Tracking:** Matches rows by `row_number` to update only the `Email Sent` column (`Yes` for valid/sent rows, `No` for invalid or duplicate rows).

---

## Prerequisites

* An **n8n** instance (n8n Cloud or self-hosted)
* **Google Sheets OAuth2** credentials configured in n8n
* **Gmail OAuth2** credentials configured in n8n

---

## Google Sheet Setup

Create a Google Sheet named **`Student_information`** with a sheet tab named **`Info`**. Row 1 must contain these exact column headers:

| Name | Course | Status | Emailid | Email Sent |
| :--- | :--- | :--- | :--- | :--- |
| Benisheela | AI automation | In Progress | beni.sheela@gmail.com | |
| Stephan | Agentic AI | In Progress | stephan.rpm@gmail.com | |
| Beni | MCP | In Progress | beni.sheela | |
| Anto Jerone | n8n Automation | In Progress | anto.jerone@gmail.com | |
| Benisheela | AI automation | In Progress | beni.sheela@gmail.com | |

> Leave the **`Email Sent`** column blank for new students who have not yet received an email.

---

## Quick Start (Import Workflow)

1. Open your n8n workspace and create a **New Workflow**.
2. Click the **`...`** menu in the top-right corner and select **Import from File...**.
3. Upload **`GoogleSheet_to_Gmail.json`**.
4. Re-link your credentials and spreadsheet:
   * Open **`Get row(s) in sheet`**, **`Update row in sheet`**, and **`Update row in sheet1`** to select your **Google Sheets account** credential and point them to your **`Student_information`** document (`Info` tab).
   * Open **`Send a message`** and select your **Gmail account** credential.
5. Click **Save**.

---

## Workflow Architecture

```text
[When clicking ‘Execute workflow’]
                │
                ▼
     [Get row(s) in sheet]       ──► Reads all rows from Student_information (Info)
                │
                ▼
      [Code in JavaScript]       ──► Skips "Yes" rows, validates Emailid/Name/Course,
                │                    flags duplicates, and builds the HTML email
                ▼
              [If]               ──► Checks: {{ $json.isValid }} is true
        ┌───────┴───────┐
      True            False
        │               │
        ▼               ▼
 [Send a message]  [Update row in sheet1] ──► Sets Email Sent = "No"
        │
        ▼
 [Update row in sheet]           ──► Sets Email Sent = "Yes"
```

---

## Node-by-Node Breakdown

| # | Node Name | Type | Purpose & Key Settings |
| :-: | :--- | :--- | :--- |
| 1 | **When clicking ‘Execute workflow’** | Manual Trigger | Starts the workflow on demand. *(Can be replaced with a Schedule Trigger for automated runs.)* |
| 2 | **Get row(s) in sheet** | Google Sheets (`v4.7`) | Reads all rows from `Student_information` → `Info`. |
| 3 | **Code in JavaScript** | Code (`v2`) | Runs once for all items. Skips rows where `Email Sent` is `yes`, checks for invalid/missing emails, duplicate emails, and missing `Name`/`Course`, and generates the HTML email payload (`to`, `subject`, `body`, `isValid`, `row_number`). |
| 4 | **If** | If (`v2.4`) | Strict boolean check on `={{ $json.isValid }}`. Routes valid items to **Send a message** and invalid/duplicate items to **Update row in sheet1**. |
| 5 | **Send a message** | Gmail (`v2.2`) | Sends the HTML email using `={{ $json.to }}`, `={{ $json.subject }}`, and `={{ $json.body }}`. `appendAttribution` is set to `false` and `onError` is set to `continueRegularOutput`. |
| 6 | **Update row in sheet** | Google Sheets (`v4.7`) | Matches on `row_number` (`={{ $('If').item.json.row_number }}`) and updates `Email Sent` to **`Yes`**. |
| 7 | **Update row in sheet1** | Google Sheets (`v4.7`) | Matches on `row_number` (`={{ $('If').item.json.row_number }}`) and updates `Email Sent` to **`No`**. |

---

## Testing & Verification

1. Clear the **`Email Sent`** column in your Google Sheet for the rows you want to test.
2. Include a mix of valid rows, an invalid email (e.g., `beni.sheela`), and a duplicate email address.
3. Click **Execute workflow** in n8n.
4. **Expected Results:**
   * Valid, unique students receive the formatted HTML welcome email and update to **`Yes`**.
   * Invalid and duplicate rows are not emailed and update to **`No`**.
   * Executing the workflow a second time skips all **`Yes`** rows automatically (if no new rows remain, **Code in JavaScript** returns no output and stops cleanly).

---

## Notes & Troubleshooting

* **Gmail Error Routing (Optional Improvement):** In the current export, **Send a message** uses `On Error: Continue` (`continueRegularOutput`). If Gmail rejects a syntactically valid address at send time, switching **On Error** to **`Continue (using error output)`** and connecting the error output to **`Update row in sheet1`** will ensure failed sends are marked **`No`** instead of **`Yes`**.
* **Case-Sensitive Node Names:** The update nodes reference `{{ $('If').item.json.row_number }}`. If you rename the **`If`** node, update that expression in both Google Sheets update nodes to match.
* **No Output from Code Node:** If **Code in JavaScript** displays *"No output data returned"*, every row in your sheet is already marked **`Yes`**. Add new rows or clear the `Email Sent` column to run again.

#Final Output

| Name | Course | Status | Emailid | Email Sent |
| :--- | :--- | :--- | :--- | :--- |
| Benisheela | AI automation | In Progress | beni.sheela@gmail.com |Yes |
| Stephan | Agentic AI | In Progress | stephan.rpm@gmail.com | Yes|
| Beni | MCP | In Progress | beni.sheela | No|
| Anto Jerone | n8n Automation | In Progress | anto.jerone@gmail.com |Yes |
| Benisheela | AI automation | In Progress | beni.sheela@gmail.com |No |