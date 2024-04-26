from student import *
from policy import *
from studentrepo import StudentRepo
from policyrepo import PolicyRepo

class Gradebook:
    def __init__(self):
        self.__students:list[Student]= []
        self.__grading_policy=GradingPolicy()
    
    @property
    def grading_policy(self):
        return self.__grading_policy
    
    def check_grading_policy(self)->bool:
        return self.__grading_policy.check_weight()
    
    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        if self.index >= len(self.__students)-1:
            raise StopIteration
        self.index += 1
        return self.__students[self.index]
    
    def setup_new_semester(self, num_assignments: int, num_tests: int, num_final_exams: int, assignment_weight: float, test_weight: float, final_exam_weight: float)->bool:
        if assignment_weight + test_weight + final_exam_weight != 100:
            return True

        with open("Grades.dat", "w") as file:
            file.close() 
        with open("policy.dat", "w") as file:
            file.close()
        try:
            self.__grading_policy.setup_grading_policy(num_assignments, num_tests, num_final_exams, assignment_weight, test_weight, final_exam_weight)
            self.save_policy_to_policydb()
        except ValueError as e:
            raise ValueError("Error setting up policy") from e
            return True
        return False

    def add_student(self, student_id:int, first_name:str, last_name:str)->bool:
        found = False
        self.get_student_from_studentdb()
        for student in self.__students:
            if student.stuid == student_id:
                found= True
                break
        else:
            student = Student(student_id, first_name, last_name) 
            self.__students.append(student)
            self.save_student_to_studentdb()
        return found

    def record_assignment_score(self, assignment_number:int, scores:float)->None:
        for student in self.__students:
            if student.stuid in scores:
                score = scores[student.stuid]
                student.add_assignment_score(assignment_number, score)
        self.save_student_to_studentdb() 

    def record_test_score(self, test_number:int, scores:float)->None:
        for student in self.__students:
            if student.stuid in scores:
                score = scores[student.stuid]
                student.add_test_score(test_number, score)
        self.save_student_to_studentdb()
    
    def record_final_exam_score(self, scores:float)->None:
        for student in self.__students:
            if student.stuid in scores:
                score = scores[student.stuid]
                student.add_final_exam_score(score)  
        self.save_student_to_studentdb()

    def change_student_grade(self, student_id:int, grade_type:str, identifier:int, new_score:float)->tuple:
        for student in self.__students:
            if student.stuid == student_id:
                if grade_type == 'P':
                    if identifier <= student.get_num_assignments():
                        student.add_assignment_score(identifier, new_score)
                        self.save_student_to_studentdb()
                        return True, "Grade updated successfully."
                    else:
                        return False, "Invalid assignment number."
                elif grade_type == 'T':
                    if identifier <= student.get_num_tests():
                        student.add_test_score(identifier, new_score)
                        self.save_student_to_studentdb()
                        return True, "Grade updated successfully."
                    else:
                        return False, "Invalid test number."
                elif grade_type == 'F':
                    student.add_final_exam_score(new_score)
                    self.save_student_to_studentdb()
                    return True, "Final exam grade updated successfully."
                else:
                    return False, "Invalid grade type entered."
        return False, f"No student found with the ID: {student_id}"

    def calculate_final_scores(self):
        for student in self.__students:
            assignment_weight = self.__grading_policy.get_weight('assignments')
            test_weight = self.__grading_policy.get_weight('tests')
            final_exam_weight = self.__grading_policy.get_weight('final_exam')

            max_assignment_score = assignment_weight / self.__grading_policy.num_assignments
            max_test_score = test_weight / self.__grading_policy.num_tests
            max_final_exam_score = final_exam_weight

            assignment_score = student.average_assignment_score()
            if assignment_score is None:
                assignment_score = 0.0

            test_score = student.average_test_score()
            if test_score is None:
                test_score = 0.0

            assignment_avg = assignment_score
            test_avg = test_score

            final_exam_score = student.final_exam_score()
            if final_exam_score is None:
                final_exam_score = 0.0

            final_score = (
                (assignment_avg / max_assignment_score) * assignment_weight +
                (test_avg / max_test_score) * test_weight +
                (final_exam_score / max_final_exam_score) * final_exam_weight
            )
            student.final_score = final_score
        self.save_student_to_studentdb()


    def order_students_by_name(self)->list[Student]:
        n = len(self.__students)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.__students[j].last_name > self.__students[j + 1].last_name:
                    self.__students[j], self.__students[j + 1] = self.__students[j + 1], self.__students[j]
        return self.__students

    def order_students_by_id(self)->list[Student]:
        n = len(self.__students)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.__students[j].stuid < self.__students[min_idx].stuid:
                    min_idx = j
            self.__students[i], self.__students[min_idx] = self.__students[min_idx], self.__students[i]
        return self.__students


    def __str__(self) -> str:
        output =''
        for student in self.__students:
            output += str(student) +'\n'
        return f'Grading_Polic:{self.__grading_policy}\nStudents:{output}'
    
    def __repr__(self):
        return str(self)

    def get_student_from_studentdb(self):
        repos = StudentRepo("grades.dat")
        try:
            self.__students = repos.read_students_from_file()
            if not self.__students:
                raise ValueError("Student data is empty or corrupted.")
        except (FileNotFoundError, ValueError) as e:
            self.__students = []
    
    
    def get_policy_from_policydb(self):
        repos = PolicyRepo("policy.dat")
        try:
            self.__grading_policy = repos.read_policy_from_file()
            if self.__grading_policy is None:
                raise ValueError("Policy file is empty or corrupted.")
                self.__grading_policy = None
        except FileNotFoundError:
            self.__grading_policy = None 

    def save_student_to_studentdb(self):
        repos = StudentRepo("grades.dat")
        repos.save_students_to_file(self.__students)
    
    def save_policy_to_policydb(self):
        repos = PolicyRepo("policy.dat")
        repos.save_policy_to_file(self.__grading_policy)


# def main():
#     gradebook = Gradebook()
#     gradebook.setup_new_semester(num_assignments=3, num_tests=2, num_final_exams=1, assignment_weight=40, test_weight=30, final_exam_weight=30)
#     gradebook.add_student(1, "Abraham", "atiet")
#     gradebook.add_student(2, "luna", "gebre")
#     gradebook.record_assignment_score(1, {1: 85, 2: 78})
#     gradebook.record_test_score(1, {1: 90, 2: 85})
#     gradebook.record_final_exam_score({1: 85, 2: 90})
#     gradebook.calculate_final_scores()
#     print("Grading Policy:")
#     print(gradebook.grading_policy)
#     print("\nStudents:")
#     print(gradebook)
#     result, message = gradebook.change_student_grade(1, 'P', 1, 90)
#     print(message)
#     print("Grading Policy Check:", gradebook.check_grading_policy())
#     print("Ordered Students by Name:")
#     for student in gradebook.order_students_by_name():
#         print(student)
#     print("Ordered Students by ID:")
#     for student in gradebook.order_students_by_id():
#         print(student)

# if __name__ == "__main__":
#     main()
