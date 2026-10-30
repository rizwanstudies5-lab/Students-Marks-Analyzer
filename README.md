# Student Marks Analyzer

A simple, menu-driven Python program that analyzes student marks stored in a CSV file.
Built for a Programming Fundamentals / Foundations in Data Science course using only basic Python
(functions, loops, lists, dictionaries, and file handling). No classes or OOP.

## Features

- Load student data from a CSV file with input validation
- Descriptive statistics per subject: mean, median, mode, standard deviation, highest, lowest
- Overall class statistics and pass rate
- Letter grade assignment and grade distribution
- Top students ranking
- List of students below the pass mark
- Search a student by name
- Charts (subject averages and grade distribution) using matplotlib
- Save a full text report

## Requirements

- Python 3.8 or newer
- matplotlib (optional, only needed for charts)

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

Choose an option from the menu by entering its number.

## Data Format

`students.csv` must have a `name` column followed by one column per subject (marks from 0 to 100):

```csv
name,Programming,Mathematics,Statistics,English
Ali Khan,85,78,82,74
```

You can add subjects or students freely. Rows with invalid marks are skipped with a warning.

## Grading Scale

| Average | Grade |
|---------|-------|
| 85+     | A     |
| 70-84   | B     |
| 60-69   | C     |
| 50-59   | D     |
| Below 50| F     |

## Project Structure

```
student-marks-analyzer/
├── main.py
├── students.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Concepts Demonstrated

- Functions and modular code
- Lists, dictionaries, and sorting
- File handling and CSV reading
- Error handling with try/except
- Descriptive statistics implemented manually
- Data visualization
