import matplotlib.pyplot as plt
import os
import math

total_points = 1000

def get_assignment_name(assignment_id):
    with open("data/assignments.txt", "r") as f:
        lines = f.read().split("\n")
        for i, line in enumerate(lines):
            if line.strip() == str(assignment_id):
                assignment_name = str(lines[i - 1].strip())
                return assignment_name

def get_assignment(name):
    with open("data/assignments.txt", "r") as f:
        lines = f.read().split("\n")
        for i, line in enumerate(lines):
            if line.strip() == name:
                assignment_id = int(lines[i + 1].strip())
                total = int(lines[i + 2].strip())
                return [assignment_id, total]

def get_students():
    students = dict()
    with open("data/students.txt", "r") as f:
        all_students = f.readlines()
        for student in all_students:
            students[student[3:].strip()] = int(student[0:3].strip())
    return students

def get_submissions_for_student(student_id):
    assignments = dict()
    submissions = get_submissions()
    for assignment in submissions:
        if int(assignment[0]) == student_id:
            assignments[assignment[1]] = float(assignment[2])
    return assignments

def get_submissions():
    submissions = list()
    for filename in os.listdir("data/submissions"):
        filepath = os.path.join("data/submissions", filename)
        if os.path.isfile(filepath):
            with open(filepath, "r") as f:
                content = f.read().strip().split("|")
                submissions.append([content[0], content[1], content[2]])
    return submissions

def get_assignment_statistics(assignment):
    min_grade, max_grade, count, total = None, None, 0, 0
    for submission in get_submissions():
        if int(submission[1]) == int(assignment[0]):
            grade = int(submission[2])
            min_grade = grade if (not min_grade or (grade < min_grade)) and grade else min_grade
            max_grade = grade if (not max_grade or (grade > max_grade)) and grade else max_grade
            total += grade
            count += 1
    return [min_grade, max_grade, count, total]

def get_weighted_grade():
    pass

def do_option():
    option = get_option()
    if option == "1":
        name = input("What is the student's name: ")
        student_id = get_students().get(name.strip().title())
        if not student_id:
            print("Student not found")
            return
        count, total = 0, 0
        for assignment_id, grade in get_submissions_for_student(student_id).items():
            assignment_name = get_assignment_name(assignment_id)
            assignment = get_assignment(assignment_name)
            weight = ((grade / 100) * assignment[1]) * 100
            total += weight
            count += 1
        print(f"{int(round(total // 1000))}%")
    elif option == "2":
        name = input("What is the assignment name: ")
        assignment = get_assignment(name.strip().title())
        if not assignment:
            print("Assignment not found")
            return
        stats = get_assignment_statistics(assignment)
        print(f"Min: {int(stats[0])}%")
        print(f"Avg: {int(round(stats[3] // stats[2]))}%")
        print(f"Max: {int(stats[1])}%")
    elif option == "3":
        name = input("What is the assignment name: ")
        assignment = get_assignment(name.strip().title())
        stats = get_assignment_statistics(assignment)
        submission_grades = []
        if not assignment:
            print("Assignment not found")
            return
        for submission in get_submissions():
            if int(submission[1]) == int(assignment[0]):
                submission_grades.append(int(submission[2]))
        plt.hist(submission_grades, bins=range(math.floor(stats[0] / 10) * 10, 101, 5))
        plt.show()
    else:
        print("Invalid selection")

def get_option():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")

    option = input("\nEnter your selection: ")
    return option

def main():
    do_option()


if __name__ == "__main__":
    main()