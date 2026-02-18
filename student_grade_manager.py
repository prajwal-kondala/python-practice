'''
Student Grade Manager

This program:
- Stores student marks
- Calculates averages
- Assigns grades
- Finds the top student


students = {
     'Prajwal': {'math': 95, 'science': 88, 'english': 92},
     'Alice': {'math': 78, 'science': 82, 'english': 85},
     'Bob': {'math': 92, 'science': 79, 'english': 88},
     'Charlie': {'math': 65, 'science': 70, 'english': 72},
     'Diana': {'math': 88, 'science': 91, 'english': 87}
   }

def calculate_average(scores):
    math = scores['math']
    science = scores['science']
    english = scores['english']
    average = round((math + science + english) / 3, 2)
    return average

def assign_grade(average):
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    else:
        return 'D'

def get_top_student(students):
    top_student = max(students, key=lambda x: calculate_average(students[x]))
    return top_student , calculate_average(students[top_student])

def subject_topper(students, subject):
    topper = max(students, key=lambda x: students[x][subject])
    return topper, students[topper][subject]

print("Student Report: ")
print("-"*20)
for student_name, scores in students.items():
    average = calculate_average(scores)
    grade = assign_grade(average)
    print(f"{student_name}: Average = {average}, Grade = {grade}")

top_name, top_avg = get_top_student(students)
print(f"\nTop Student: {top_name} ({top_avg})")
print("\nSubject Toppers: ")

subjects = ['math', 'science', 'english']
for subject in subjects:
    topper_name, topper_score = subject_topper(students, subject)
    print(f"  {subject.capitalize()}: {topper_name} with {topper_score} marks")
print("\n'A' Grade Students :")
found_a_grade = False
for student_name, scores in students.items():
    average = calculate_average(scores)
    grade = assign_grade(average)
    if grade == 'A':
        print(f" {student_name}")
        found_a_grade = True

if not found_a_grade:
    print("No students achieved an 'A' grade.")
