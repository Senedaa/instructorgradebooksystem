from student import Student
from policy import GradingPolicy
from gradebook import Gradebook

class GradeBookApp:
    def __init__(self) -> None:
        self.__gradebook = Gradebook()
        self.__gradebook.get_policy_from_policydb()
        self.__gradebook.get_student_from_studentdb()
        self.setup_completed = False
    
    def show_menu(self):
        print("===== MENU ====")
        print("(S) Set up new semester")
        print("(A) Add a student")
        print("(P) Record programming assignment")
        print("(T) Record test grades for all students")
        print("(F) Record Final exam score for all students")
        print("(C) Change a grade")
        print("(G) Calculate final score")
        print("(O) Output the grade data")
        print("(Q) Quit")

    def process_command(self, command:str) -> bool:
        cont = True 
        if command == 's':
            proceed = True
            if self.setup_completed :
                print("Setup for the current semester has already been completed.")
                response = input("Do you want to reset the setup? (yes/no): ").strip().lower()
                if response != 'yes':
                    proceed = False

            if proceed:
                print("Please enter the following info \n")
                num_assignments = num_tests = num_final_exams = assignment_weight = test_weight = final_exam_weight = None
                try:
                    num_assignments = int(input("Enter the number of programming assignments (0-6): "))
                    num_tests = int(input("Enter the number of tests (0-4): "))
                    num_final_exams = int(input("Enter the number of final exams (0-1): "))
                    assignment_weight = float(input("Enter the weight of programming assignments (0-100): "))
                    test_weight = float(input("Enter the weight of tests (0-100): "))
                    final_exam_weight = float(input("Enter the weight of final exams (0-100): "))
                    if not (0 <= num_assignments <= 6 and 0 <= num_tests <= 4 and 0 <= num_final_exams <= 1):
                        raise ValueError("Input values must be within specified ranges.")
                    
                except ValueError as e:
                    print("Error:", e)
                    return True
                ans = self.__gradebook.setup_new_semester(num_assignments, num_tests, num_final_exams, assignment_weight, test_weight, final_exam_weight)
                if ans:
                    print("Error: The weights must add up to 100.")
                    return True
                else:
                    print("New semester setup completed.")
                    self.setup_completed = True
                return True
        elif command == 'a':
            if self.__gradebook.check_grading_policy() == False:
                print("Error: Please set up the semester first.")
                return True
            else:
                try:
                    student_id = int(input("Enter the student's ID (1 - 9999): "))
                    if not (1 <= student_id <= 9999):
                        raise ValueError("Student ID must be in the range 1 - 9999.")
                    last_name = input("Enter the student's last name (max 20 characters): ")
                    first_name = input("Enter the student's first name (max 20 characters): ")
                    if len(last_name) > 20 or len(first_name) > 20:
                        raise ValueError("Name must be at most 20 characters long.")
                    found = self.__gradebook.add_student(student_id, first_name, last_name)
                    if found:
                        raise ValueError("Student ID already exists.")
                    else:
                        print("Student added successfully.")
                        return True
                except ValueError as e:
                    print("Error:", e)
        elif command == 'p':
            if self.__gradebook.check_grading_policy() == False:
                print("Semester setup is not complete. Please set up the semester first.")
                return True
            assignment_weight = self.__gradebook.grading_policy.get_weight('assignments')

            try:
                assignment_number = int(input("Enter the assignment number to record scores for: "))
                max_assignment_score = assignment_weight / self.__gradebook.grading_policy.num_assignments
            except ValueError:
                print("Invalid input. Please enter a valid integer for the assignment number.")
                return True

            scores = {}
            for student in self.__gradebook:
                try:
                    score = float(input(f"Enter score for {student.first_name} {student.last_name} (ID: {student.stuid}), maximum score is {max_assignment_score}: "))
                    if score < 0 or score > max_assignment_score:
                        raise ValueError(f"Score must be between 0 and {max_assignment_score}.")
                    scores[student.stuid] = score
                except ValueError as e:
                    print(f"Invalid score entered for {student.first_name} {student.last_name}: {e}")
                    continue

            self.__gradebook.record_assignment_score(assignment_number, scores)
            print("Scores recorded successfully.")


        elif command == 't':
            if self.__gradebook.check_grading_policy() == False:
                print("Semester setup is not complete. Please set up the semester first.")
                return True

            try:
                test_number = int(input("Enter the test number to record scores for: "))
                max_tests = self.__gradebook.grading_policy.num_tests
                if test_number < 1 or test_number > max_tests:
                    print(f"Invalid test number. Please enter a number between 1 and {max_tests}.")
                    return True
                
                test_weight = self.__gradebook.grading_policy.get_weight('tests')
                max_test_score = test_weight / max_tests

            except ValueError:
                print("Invalid input. Please enter a valid integer for the test number.")
                return True

            scores = {}
            for student in self.__gradebook:
                try:
                    score = float(input(f"Enter score for {student.first_name} {student.last_name} (ID: {student.stuid}), maximum score is {max_test_score}: "))
                    if score < 0 or score > max_test_score:
                        raise ValueError(f"Score must be between 0 and {max_test_score}.")
                    scores[student.stuid] = score
                except ValueError as e:
                    print(f"Invalid score entered for {student.first_name} {student.last_name}: {e}")
                    continue

            self.__gradebook.record_test_score(test_number, scores)
            print("Test scores recorded successfully.")
            return True

        elif command == 'f':
            if self.__gradebook.check_grading_policy() == False:
                print("Semester setup is not complete. Please set up the semester first.")
                return True
            final_exam_weight = self.__gradebook.grading_policy.get_weight('final_exam')
            max_final_exam_score = final_exam_weight

            print("Recording scores for the Final Exam:")
            for student in self.__gradebook:
                try:
                    score = float(input(f"Enter final exam score for {student.first_name} {student.last_name} (ID: {student.stuid}), maximum score is {max_final_exam_score}: "))
                    if score < 0 or score > max_final_exam_score:
                        raise ValueError(f"Score must be between 0 and {max_final_exam_score}.")
                    student.add_final_exam_score(score)
                except ValueError as e:
                    print(f"Invalid score entered for {student.first_name} {student.last_name}: {e}")
                    continue

            self.__gradebook.save_student_to_studentdb()
            print("Final exam scores recorded successfully.")
            return True

        elif command == 'c':
            if self.__gradebook.check_grading_policy() == False:
                print("The grading policy is not set up. Please set up the grading policy first.")
                return True

            try:
                student_id = int(input("Enter the student ID for which the grade needs to be changed: "))
                grade_type = input("Enter the type of grade to change (P for programming assignment, T for test, F for final exam): ").upper()
                if grade_type not in ['P', 'T', 'F']:
                    print("Invalid grade type entered. Please enter 'P', 'T', or 'F'.")
                    return True

                new_score = float(input("Enter the new score: "))

                if grade_type == 'P':
                    max_score = self.__gradebook.grading_policy.get_weight('assignments') / self.__gradebook.grading_policy.num_assignments
                elif grade_type == 'T':
                    max_score = self.__gradebook.grading_policy.get_weight('tests') / self.__gradebook.grading_policy.num_tests
                else:
                    max_score = self.__gradebook.grading_policy.get_weight('final_exam')

                if not 0 <= new_score <= max_score:
                    raise ValueError(f"New score must be between 0 and {max_score}.")

                identifier = None
                if grade_type in ['P', 'T']:
                    identifier = int(input(f"Enter the {grade_type.lower()} number: "))

                success, message = self.__gradebook.change_student_grade(student_id, grade_type, identifier, new_score)
                print(message)
            except ValueError as e:
                print(f"Invalid input: {e}")

            return True

        elif command == 'g':
            if self.__gradebook.check_grading_policy() == False:
                print("The grading policy is not set up. Please set up the grading policy first.")
                return True
            
            self.__gradebook.calculate_final_scores()
            print("Final scores calculated and updated for all students.")
            return True
            
        elif command == 'o':
            if not self.__gradebook.check_grading_policy():
                print("The grading policy is not set up. Please set up the grading policy first.")
                return True

            sort_option = input("Choose sorting method: Enter 'N' for name or 'I' for ID: ").upper()

            if sort_option == 'N':
                print("--------Sorting by Name--------")
                students = self.__gradebook.order_students_by_name()
                for student in students:
                    print(f'{student}\n')
            elif sort_option == 'I':
                print("-------Sorting By ID--------")
                students = self.__gradebook.order_students_by_id()
                for student in students:
                    print(f'{student}\n')
            else:
                print("Invalid option. Please enter 'N' for name or 'I' for ID.")
                return True

            return True

        elif command == 'q':
            print("Quitting ... 😊")
            cont = False
        else:
            print("Enter Valid Choices from Options")
        return cont

def main():
    app = GradeBookApp()

    cont = True
    while cont:
        app.show_menu()
        command = input("Enter your choice: ").lower()
        cont = app.process_command(command)

if __name__ == "__main__":
    main()
