# 📚 Student Grade Manager

A simple Streamlit application to manage student marks and grades.

## Features

- Add any number of students
- Validate marks between 0 and 100
- Automatically calculate grades
- Display all students in a table
- Show:
  - Class Average
  - Highest Mark
  - Lowest Mark
- Automatically clear the form after submission

## Grade Criteria

| Mark Range | Grade |
| ---------- | ----- |
| 90 - 100 | A+ |
| 80 - 89 | A |
| 70 - 79 | B |
| 60 - 69 | C |
| 50 - 59 | D |
| Below 50 | F |

## Requirements

- Python 3.8+
- Streamlit
- Pandas

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd student-grade-manager
```

Install dependencies:

```bash
pip install streamlit pandas
```

## Run the Application

```bash
streamlit run grade_app.py
```

The application will open in your browser automatically.

## Project Structure

```text
student-grade-manager/
│
├── grade_app.py
├── README.md
└── requirements.txt
```

## Sample Output

| Name | Mark | Grade |
|------|------|-------|
| Anto | 95 | A+ |
| John | 82 | A |
| Mary | 68 | C |

### Statistics

- Class Average: 81.67
- Highest Mark: 95
- Lowest Mark: 68

## Author

Beni
