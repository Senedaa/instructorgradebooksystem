import os
import json
from student import Student

class StudentRepo:
    def __init__(self, filename: str) -> None:
        self.__filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    def save_students_to_file(self, students:list[Student])->None:
        with open(self.__filename, "w") as file:
            for student in students:
                student_data = self.student_to_dict(student)
                json.dump(student_data, file)
                file.write('\n')  


    def student_to_dict(self, student:Student):
        grades_list = []
        for grade_item in student:
            grade_data = (grade_item.grade_type(), grade_item.score)
            grades_list.append(grade_data)

        student_data = {
            "stuid": student.stuid,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "grades": grades_list,
            "final_score": student.final_score
        }
        return student_data

    def read_students_from_file(self) -> list[Student]:
        students = []
        try:
            with open(self.__filename, 'r') as file:
                for line in file:
                    item = json.loads(line)
                    student = Student(item['stuid'], item['first_name'], item['last_name'])
                    for grade_type, score in item['grades']:
                        student.add_grade(grade_type, score)
                    student.final_score = item['final_score']
                    students.append(student)
        except FileNotFoundError:
            print("File not found, returning empty list.")
        return students

def main():
    filename = "grades.dat"
    students_to_save = [
        Student(123, "hana", "Berhe"),
        Student(456, "segen", "beyene"),
        Student(789, "sara", "tekle")
    ]

    for student in students_to_save:
        student.add_grade('Assignment', 90)
        student.add_grade('Test', 78)
        student.add_grade('FinalExam', 88)

    student_repo = StudentRepo(filename)
    student_repo.save_students_to_file(students_to_save)
    loaded_students = student_repo.read_students_from_file()

    for student in loaded_students:
        print(student)
        print()

if __name__ == "__main__":
    main()
