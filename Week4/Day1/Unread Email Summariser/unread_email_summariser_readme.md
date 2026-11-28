# Unread Email Summariser (n8n AI Agent Workflow)

An automated AI Agent workflow built in **n8n** that connects to your Gmail account, fetches your latest 5 unread emails, generates a concise one-line summary (20 words maximum) for each using OpenAI, formats each entry with sender and subject details, and emails all five summaries back to you as a single digest message.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Workflow Architecture](#workflow-architecture)
- [Tools & Prerequisites](#tools--prerequisites)
- [Node-by-Node Breakdown](#node-by-node-breakdown)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Example Output](#example-output)
- [Security Notes](#security-notes)

---

## Problem Statement

Unread emails pile up faster than they can be opened. This workflow solves inbox overload on demand by summarizing your 5 most recent unread messages into a single, scannable digest email—built entirely on the n8n visual canvas with no custom code files required.

---

## Workflow Architecture

```text
[Manual Trigger]
       │
       ▼
[Gmail: Get many messages]  (Filter: Unread | Limit: 5)
       │
       ▼
[AI Agent] ◄──── [OpenAI Chat Model (gpt-4o-mini)]
       │
       ▼
[Edit Fields]               (Combines From, Subject, and Summary)
       │
       ▼
[Summarize]                 (Concatenates all 5 lines into 1 text block)
       │
       ▼
[Gmail: Send a message]     (Sends the combined digest to your inbox)
```

---

## Tools & Prerequisites

- **n8n** (n8n Cloud or self-hosted instance)
- **Gmail Account** with **Google Cloud OAuth 2.0** credentials configured (Gmail API enabled)
- **OpenAI API Key** with access to `gpt-4o-mini`

---

## Node-by-Node Breakdown

| Step | Node Name | Type | Purpose |
| :--- | :--- | :--- | :--- |
| 1 | **When clicking ‘Execute workflow’** | Manual Trigger | Runs the workflow on demand. |
| 2 | **Get many messages** | Gmail (`getAll`) | Fetches up to **5** emails filtered by `Read Status: Unread`. |
| 3 | **AI Agent** | LangChain AI Agent | Summarizes each email's `snippet` into **one line (20 words max)** with no greetings or headings. |
| 4 | **OpenAI Chat Model** | LangChain Chat Model | Powers the AI Agent using `gpt-4o-mini`. |
| 5 | **Edit Fields** | Set | Formats each item as `From: <sender> \| Subject: <subject> \| Summary: <output>`. |
| 6 | **Summarize** | Summarize | Concatenates all 5 `formatted_output` items into a single newline-separated block (`concatenated_formatted_output`). |
| 7 | **Send a message** | Gmail (`send`) | Emails the combined digest under the subject `Summary of Your Latest 5 Unread Emails` (with n8n attribution disabled). |

---

## Setup & Installation

### 1. Import the Workflow
1. Open your n8n dashboard and create a new workflow.
2. Click the **⋯** menu in the top-right corner and select **Import from File...**.
3. Upload `Unread Email Summariser.json`.
4. Confirm the workflow is saved as **Unread Email Summariser**.

### 2. Configure Gmail OAuth2 Credentials
1. Open [Google Cloud Console](https://console.cloud.google.com/), create a project, and enable the **Gmail API**.
2. Configure the **OAuth consent screen** (External) and add your Gmail address under **Test users**.
3. Create an **OAuth Client ID** (Web application) and add the **OAuth Redirect URL** provided by n8n.
4. In n8n, open both **Get many messages** and **Send a message**, create/select your **Gmail OAuth2** credential using the Client ID and Client Secret, and sign in with Google.

### 3. Configure OpenAI Credentials
1. Generate an API key from [OpenAI Platform](https://platform.openai.com/api-keys).
2. In n8n, open the **OpenAI Chat Model** node, create a new **OpenAI API** credential, and paste your key.

### 4. Update the Recipient Address
1. Open the **Send a message** Gmail node.
2. Replace the **To** field with your own email address (`your-email@gmail.com`).
3. Save the workflow (`Ctrl + S` / `Cmd + S`).

---

## Usage

1. Open the **Unread Email Summariser** workflow in n8n.
2. Click **Execute workflow** at the bottom of the canvas.
3. Wait a few seconds for all nodes to turn green.
4. Check your Gmail inbox for an email titled **`Summary of Your Latest 5 Unread Emails`**.

---

## Example Output

```text
From: alerts@bank.com | Subject: Debit Alert | Summary: INR 859.00 was debited from your account on 28-11-26.
From: team@service.com | Subject: Welcome! | Summary: Welcome to the platform; use the provided link to start using the API.
From: security@google.com | Subject: Security alert | Summary: You granted account access to a third-party app on November 28.
From: updates@investing.com | Subject: Monthly Updates | Summary: November updates include new stock options, enhanced charts, and market timing features.
From: newsletter@tech.io | Subject: Weekly Digest | Summary: Top AI automation trends and new developer tools released this week.
```

---

## Security Notes

- **API Keys & Tokens:** All credentials (OpenAI API key and Google OAuth tokens) are stored securely inside n8n's encrypted credentials manager—never hardcoded in the workflow JSON.
- **Sharing the JSON:** Before publishing `Unread Email Summariser.json` publicly, consider replacing your personal email address in the **Send a message** node with a placeholder.