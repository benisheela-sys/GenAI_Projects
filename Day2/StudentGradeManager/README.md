# Student Grade Manager

A simple Python terminal application to manage student marks and grades.

## Features

- Add multiple students
- Calculate grades (A–E)
- Show results in a formatted table
- Display average, highest, and lowest marks
- Handles invalid input safely

## Grading Scale

| Marks | Grade |
|--------|--------|
| 90–100 | A |
| 80–89 | B |
| 70–79 | C |
| 60–69 | D |
| Below 60 | E |

## Run

```bash
python grade_manager.py
```

## Project Files

```text
grade_manager.py
README.md
.gitignore
.gitattributes
```

=====Result========

===== GRADE MANAGER =====
1. Add Student
2. Show Results
3. Quit
Choose an option: 1
Enter student name: Anto
Enter mark (0-100): 89
Student added successfully.
===== GRADE MANAGER =====
1. Add Student
2. Show Results
3. Quit
Choose an option: 1
Enter student name: Raji
Enter mark (0-100): 90
Student added successfully.
===== GRADE MANAGER =====
1. Add Student
2. Show Results
3. Quit
Choose an option: 2

===================================
Name           Mark      Grade
===================================
Anto           89.0      B
Raji           90.0      A
===================================
Average Mark : 89.50
Highest Mark : 90.0
Lowest Mark  : 89.0

===== GRADE MANAGER =====
1. Add Student
2. Show Results
3. Quit
Choose an option: 3
Goodbye!

## Author

Benisheela

