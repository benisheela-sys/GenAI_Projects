Student Data ETL & Segmentation Pipeline (Week3-Day3-StudentETL)

An automated Extract, Transform, Load (ETL) workflow built in n8n that ingests raw student records via a web form, cleans and standardizes the data using OpenAI (gpt-4o-mini) and custom JavaScript, saves a master cleaned CSV to Google Drive, and segments students into separate enrolled and non-enrolled CSV reports based on their fee payment status.

📋 Table of Contents

Workflow Architecture

Data Cleaning & Validation Rules

Generated Output Files

Prerequisites & Credentials

Setup & Installation

Node Breakdown

🔄 Workflow Architecture

[On form submission]
        │
        ▼
[Extract from File] ──► [Basic LLM Chain] ◄── [OpenAI Chat Model (gpt-4o-mini)]
                                │
                                ▼
                           [Aggregate]
                                │
                                ▼
                      [Code in JavaScript]
                                │
                                ▼
                       [Convert to File2]
                                │
                                ▼
                  [Upload file: Student_Clean.csv]
                                │
                                ▼
                         [Download file]
                                │
                                ▼
                      [Extract from File1]
                                │
                                ▼
                     [If: Fee_Paid == "TRUE"]
                        /               \
               (True)  /                 \  (False)
                      ▼                   ▼
            [Convert to File]    [Convert to File1]
                      │                   │
                      ▼                   ▼
           [Upload file1:        [Upload file2:
       Students_Enrolled.csv]  Student_NotEnrolled.csv]
