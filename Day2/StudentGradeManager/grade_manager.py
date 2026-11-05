# grade_manager.py

students = []


def get_grade(mark):
    """Convert a mark into a grade."""
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


def add_student():
    """Add a student after validating input."""

    name = input("Enter student name: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return

    while True:
        mark_input = input("Enter mark (0-100): ").strip()

        try:
            mark = float(mark_input)

            if mark < 0 or mark > 100:
                print("Error: Mark must be between 0 and 100.")
                continue

            students.append({
                "name": name,
                "mark": mark
            })

            print("Student added successfully.")
            break

        except ValueError:
            print("Error: Please enter a valid number.")


def show_results():
    """Display all students and statistics."""

    if not students:
        print("\nNo student records available.\n")
        return

    print("\n" + "=" * 35)
    print(f"{'Name':<15}{'Mark':<10}{'Grade'}")
    print("=" * 35)

    marks = []

    for student in students:
        grade = get_grade(student["mark"])
        marks.append(student["mark"])

        print(
            f"{student['name']:<15}"
            f"{student['mark']:<10.1f}"
            f"{grade}"
        )

    print("=" * 35)

    average = sum(marks) / len(marks)

    print(f"Average Mark : {average:.2f}")
    print(f"Highest Mark : {max(marks):.1f}")
    print(f"Lowest Mark  : {min(marks):.1f}")
    print()


def main():
    while True:
        print("===== GRADE MANAGER =====")
        print("1. Add Student")
        print("2. Show Results")
        print("3. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            show_results()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()