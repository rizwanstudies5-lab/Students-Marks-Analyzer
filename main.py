"""
Student Marks Analyzer
----------------------
A simple menu-driven program that reads student marks from a CSV file
and performs basic data analysis: descriptive statistics, grade
distribution, top performers, student search, charts, and a text report.

Only basic Python is used (functions, loops, lists, dictionaries, files).
"""

import csv
import os

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

DATA_FILE = "students.csv"
REPORT_FILE = "report.txt"
CHART_FILE = "charts.png"
PASS_MARK = 50
GRADES = ["A", "B", "C", "D", "F"]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_students(filename):
    """Read the CSV file and return (subjects, students).

    Each student is a dictionary:
        {"name": str, "marks": {subject: float}, "average": float}
    Rows with missing or invalid marks are skipped with a warning.
    """
    students = []
    subjects = []

    if not os.path.exists(filename):
        print(f"Error: '{filename}' not found.")
        return subjects, students

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        subjects = [col for col in reader.fieldnames if col != "name"]

        for line_number, row in enumerate(reader, start=2):
            try:
                marks = {}
                for subject in subjects:
                    value = float(row[subject])
                    if value < 0 or value > 100:
                        raise ValueError("mark out of range")
                    marks[subject] = value
                name = row["name"].strip()
                if name == "":
                    raise ValueError("missing name")
            except (ValueError, TypeError, KeyError, AttributeError):
                print(f"Warning: skipped invalid data on line {line_number}.")
                continue

            average = calculate_mean(list(marks.values()))
            students.append({"name": name, "marks": marks, "average": average})

    return subjects, students


# ---------------------------------------------------------------------------
# Statistics functions
# ---------------------------------------------------------------------------
def calculate_mean(values):
    """Return the average of a list of numbers."""
    return sum(values) / len(values)


def calculate_median(values):
    """Return the middle value of a list of numbers."""
    ordered = sorted(values)
    count = len(ordered)
    middle = count // 2
    if count % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def calculate_mode(values):
    """Return the most frequent value, or None if every value is unique."""
    frequency = {}
    for value in values:
        frequency[value] = frequency.get(value, 0) + 1

    highest = max(frequency.values())
    if highest == 1:
        return None

    modes = [value for value, count in frequency.items() if count == highest]
    return min(modes)


def calculate_std_dev(values):
    """Return the population standard deviation."""
    mean = calculate_mean(values)
    squared_diffs = [(value - mean) ** 2 for value in values]
    return (sum(squared_diffs) / len(values)) ** 0.5


def get_grade(average):
    """Convert an average mark to a letter grade."""
    if average >= 85:
        return "A"
    if average >= 70:
        return "B"
    if average >= 60:
        return "C"
    if average >= PASS_MARK:
        return "D"
    return "F"


def grade_distribution(students):
    """Return a dictionary with the number of students per grade."""
    counts = {grade: 0 for grade in GRADES}
    for student in students:
        counts[get_grade(student["average"])] += 1
    return counts


# ---------------------------------------------------------------------------
# Report builders (each returns a list of text lines)
# ---------------------------------------------------------------------------
def format_stats_block(title, values):
    """Build the statistics lines for one list of marks."""
    mode = calculate_mode(values)
    mode_text = "No mode" if mode is None else f"{mode:g}"
    return [
        f"{title}",
        f"  Mean               : {calculate_mean(values):.2f}",
        f"  Median             : {calculate_median(values):.2f}",
        f"  Mode               : {mode_text}",
        f"  Standard deviation : {calculate_std_dev(values):.2f}",
        f"  Highest            : {max(values):g}",
        f"  Lowest             : {min(values):g}",
        "",
    ]


def all_students_lines(subjects, students):
    """Table of all students with their average and grade."""
    header = f"{'Name':<18}"
    for subject in subjects:
        header += f"{subject[:12]:>13}"
    header += f"{'Average':>10}{'Grade':>7}"

    lines = [header, "-" * len(header)]
    for student in students:
        row = f"{student['name']:<18}"
        for subject in subjects:
            row += f"{student['marks'][subject]:>13g}"
        row += f"{student['average']:>10.2f}{get_grade(student['average']):>7}"
        lines.append(row)
    lines.append("")
    return lines


def subject_stats_lines(subjects, students):
    """Statistics for every subject."""
    lines = ["=== SUBJECT STATISTICS ===", ""]
    for subject in subjects:
        marks = [student["marks"][subject] for student in students]
        lines += format_stats_block(subject, marks)
    return lines


def overall_stats_lines(students):
    """Statistics for the students' overall averages."""
    averages = [student["average"] for student in students]
    lines = ["=== OVERALL CLASS STATISTICS ===", ""]
    lines.append(f"Total students: {len(students)}")
    lines += format_stats_block("Student averages", averages)

    passed = len([a for a in averages if a >= PASS_MARK])
    pass_rate = passed / len(students) * 100
    lines.append(f"Passed (average >= {PASS_MARK}): {passed} of {len(students)} ({pass_rate:.1f}%)")
    lines.append("")
    return lines


def grade_lines(students):
    """Grade distribution with a simple text bar chart."""
    counts = grade_distribution(students)
    lines = ["=== GRADE DISTRIBUTION ===", ""]
    for grade in GRADES:
        percent = counts[grade] / len(students) * 100
        lines.append(f"  {grade} : {'#' * counts[grade]:<15} {counts[grade]:>2} ({percent:.1f}%)")
    lines.append("")
    return lines


def top_students_lines(students, count):
    """Ranking of the top students by average."""
    ranked = sorted(students, key=lambda s: s["average"], reverse=True)
    lines = [f"=== TOP {count} STUDENTS ===", ""]
    for position, student in enumerate(ranked[:count], start=1):
        lines.append(f"  {position}. {student['name']:<18} {student['average']:.2f}  ({get_grade(student['average'])})")
    lines.append("")
    return lines


def weak_students_lines(students):
    """Students whose average is below the pass mark."""
    weak = [s for s in students if s["average"] < PASS_MARK]
    lines = [f"=== STUDENTS BELOW PASS MARK ({PASS_MARK}) ===", ""]
    if not weak:
        lines.append("  None. All students passed.")
    for student in sorted(weak, key=lambda s: s["average"]):
        lines.append(f"  {student['name']:<18} {student['average']:.2f}")
    lines.append("")
    return lines


def build_full_report(subjects, students):
    """Combine every section into one report."""
    lines = ["STUDENT MARKS ANALYSIS REPORT", "=" * 30, ""]
    lines += all_students_lines(subjects, students)
    lines += subject_stats_lines(subjects, students)
    lines += overall_stats_lines(students)
    lines += grade_lines(students)
    lines += top_students_lines(students, 5)
    lines += weak_students_lines(students)
    return lines


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------
def print_lines(lines):
    """Print a list of text lines."""
    print()
    for line in lines:
        print(line)


def search_student(students, subjects):
    """Find students by (partial) name and show their marks."""
    query = input("Enter student name (or part of it): ").strip().lower()
    if query == "":
        print("Nothing entered.")
        return

    found = [s for s in students if query in s["name"].lower()]
    if not found:
        print("No student found.")
        return

    for student in found:
        print(f"\nName: {student['name']}")
        for subject in subjects:
            print(f"  {subject:<14}: {student['marks'][subject]:g}")
        print(f"  Average       : {student['average']:.2f}")
        print(f"  Grade         : {get_grade(student['average'])}")


def ask_top_count(total):
    """Ask how many top students to show."""
    text = input("How many top students to show? [default 5]: ").strip()
    if text == "":
        return min(5, total)
    if text.isdigit() and int(text) > 0:
        return min(int(text), total)
    print("Invalid number. Showing top 5.")
    return min(5, total)


def show_charts(subjects, students):
    """Draw a bar chart of subject averages and the grade distribution."""
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib is not installed. Run: pip install matplotlib")
        return

    subject_averages = []
    for subject in subjects:
        marks = [student["marks"][subject] for student in students]
        subject_averages.append(calculate_mean(marks))

    counts = grade_distribution(students)

    figure, (left, right) = plt.subplots(1, 2, figsize=(11, 4.5))

    left.bar(subjects, subject_averages, color="steelblue")
    left.set_title("Average Marks per Subject")
    left.set_ylabel("Average mark")
    left.set_ylim(0, 100)

    right.bar(GRADES, [counts[g] for g in GRADES], color="seagreen")
    right.set_title("Grade Distribution")
    right.set_xlabel("Grade")
    right.set_ylabel("Number of students")

    figure.tight_layout()
    figure.savefig(CHART_FILE)
    print(f"Chart saved as '{CHART_FILE}'.")
    plt.show()


def save_report(subjects, students):
    """Write the full report to a text file."""
    lines = build_full_report(subjects, students)
    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    print(f"Report saved as '{REPORT_FILE}'.")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------
def show_menu():
    """Print the main menu."""
    print("\n" + "=" * 40)
    print("      STUDENT MARKS ANALYZER")
    print("=" * 40)
    print("1. View all students")
    print("2. Subject statistics")
    print("3. Overall class statistics")
    print("4. Grade distribution")
    print("5. Top students")
    print("6. Students below pass mark")
    print("7. Search a student")
    print("8. Show charts")
    print("9. Save full report to file")
    print("0. Exit")


def main():
    """Load the data and run the menu loop."""
    subjects, students = load_students(DATA_FILE)
    if not students:
        print("No valid student data to analyze. Exiting.")
        return

    print(f"Loaded {len(students)} students and {len(subjects)} subjects.")

    while True:
        show_menu()
        choice = input("Choose an option (0-9): ").strip()

        if choice == "1":
            print_lines(all_students_lines(subjects, students))
        elif choice == "2":
            print_lines(subject_stats_lines(subjects, students))
        elif choice == "3":
            print_lines(overall_stats_lines(students))
        elif choice == "4":
            print_lines(grade_lines(students))
        elif choice == "5":
            count = ask_top_count(len(students))
            print_lines(top_students_lines(students, count))
        elif choice == "6":
            print_lines(weak_students_lines(students))
        elif choice == "7":
            search_student(students, subjects)
        elif choice == "8":
            show_charts(subjects, students)
        elif choice == "9":
            save_report(subjects, students)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 9.")


if __name__ == "__main__":
    main()
