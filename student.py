from policy import *
from abc import ABC, abstractmethod

class GradItem:
    def __init__(self, score:float) -> None:
        self.__score = score
    
    @property
    def score(self)->float:
        return self.__score
    
    @score.setter
    def score(self, new_score: float)->None:
        self.__score = new_score
    
    @abstractmethod
    def grade_type(self)->str:
        pass
    
    def __str__(self)->str:
        return f"Score:{self.__score}"
    
    def __repr__(self)->str:
        return str(self)


class Assignment(GradItem):
    def grade_type(self)->str:
        return 'Assignment'

class Test(GradItem):
    def grade_type(self)->str:
        return 'Test'

class FinalExam(GradItem):
    def grade_type(self)->str:
        return 'FinalExam'

class Student:
    def __init__(self, stuid:int,first_name:str, last_name:str) -> None:
        self.__stuid = stuid
        self.__first_name = first_name
        self.__last_name = last_name
        self.__finalscore=0.0
        self.__assignments:list[Assignment]=[]
        self.__tests:list[Test]=[]
        self.__final_exams:list[FinalExam]=[]
    
    @property
    def stuid(self)->float:
        return self.__stuid
    
    @property
    def first_name(self)->str:
        return self.__first_name
    
    @property
    def last_name(self)->str:
        return self.__last_name
    
    @property
    def final_score(self)->float:
        return self.__finalscore

    @final_score.setter
    def final_score(self, score: float)->None:
        self.__finalscore = score
    
    def get_num_assignments(self)->int:
        return len(self.__assignments)
    
    def get_num_tests(self)->int:
        return len(self.__tests)
    
    def add_assignment_score(self, assignment_number:int, score:float)->None:
        while len(self.__assignments) < assignment_number:
            self.__assignments.append(Assignment(0))
        self.__assignments[assignment_number - 1] = Assignment(score)
    
    def add_test(self,test:Test)->None:
        self.__tests.append(test)

    def add_test_score(self, test_number:int, score:float)->None:
        while len(self.__tests) < test_number:
            self.__tests.append(Test(0))  
        self.__tests[test_number - 1] = Test(score)
    
    def add_finals(self,final:FinalExam)->None:
        self.__final_exams.append(final)


    def add_final_exam_score(self, score:float)->None:
        if not self.__final_exams:
            self.__final_exams.append(FinalExam(score))
        else:
            self.__final_exams[0].score = score
    
    def __iter__(self):
        self.index = -1
        return self
    
    def __next__(self):
        self.index += 1
        if self.index < len(self.__assignments):
            return self.__assignments[self.index]
        elif self.index < len(self.__assignments) + len(self.__tests):
            return self.__tests[self.index - len(self.__assignments)]
        elif self.index < len(self.__assignments) + len(self.__tests) + len(self.__final_exams):
            return self.__final_exams[self.index - len(self.__assignments) - len(self.__tests)]
        else:
            raise StopIteration


    def add_grade(self, grade_type:str, score:float)->None:
        if grade_type == 'Assignment':
            self.__assignments.append(Assignment(score))
        elif grade_type == 'Test':
            self.__tests.append(Test(score))
        elif grade_type == 'FinalExam':
            self.__final_exams.append(FinalExam(score))


    def average(self,scores:float):
        total = 0
        count = 0
        for score in scores:
            if score is not None:
                total += score.score 
                count += 1

        if count > 0:
            return total / count
        else:
            return 0
    
    def average_assignment_score(self)->float:
        return self.average(self.__assignments)
    
    def average_test_score(self)->float:
        return self.average(self.__tests)
    
    def final_exam_score(self)->float:
        if self.__final_exams:
            return self.__final_exams[0].score
        else:
            return None
        
    def calculate_final_score(self, policy: GradingPolicy) -> float:
        assignment_avg = self.average(self.__assignments)
        test_avg = self.average(self.__tests)
        final_exam_avg = self.average(self.__final_exams)

        total_weight = policy.get_weight('assignments') + policy.get_weight('tests') + policy.get_weight('final_exam')
        final_score = (
            (assignment_avg * policy.get_weight('assignments') / total_weight) +
            (test_avg * policy.get_weight('tests') / total_weight) +
            (final_exam_avg * policy.get_weight('final_exam') / total_weight)
        ) 

        self.__finalscore = final_score
        return final_score

    def __str__(self) -> str:
        assinmentoutput=''
        testoutput=''
        for assign in self.__assignments:
            assinmentoutput += str(assign) + '\n'
        for test in self.__tests:
            testoutput += str(test) +'\n'
        return f"StudentID: {self.__stuid}\nFirst_Name:{self.__first_name}\nLast_Name:{self.__last_name}\nFinalExams:{self.__final_exams}Tests:{testoutput}Assignments:{assinmentoutput}FinalScore:{self.__finalscore}"
    
    def __repr__(self) -> str:
        return str(self)


def main():
    student1 = Student(1, "abraham", "sened")
    student2 = Student(2, "segen", "hana")

    policy_weights = {'assignments': 50, 'tests': 30, 'final_exam': 20}
    policy = GradingPolicy(weights=policy_weights)

    student1.add_grade('Assignment', 80)
    student1.add_grade('Assignment', 75)
    student1.add_grade('Test', 85)
    student1.add_grade('Test', 88)
    student1.add_grade('FinalExam', 90)
    student2.add_grade('Assignment', 70)
    student2.add_grade('Assignment', 65)
    student2.add_grade('Test', 75)
    student2.add_grade('Test', 78)
    student2.add_grade('FinalExam', 80)

    print(f"{student1.first_name} {student1.last_name}'s final score: {student1.calculate_final_score(policy)}")
    print(f"{student2.first_name} {student2.last_name}'s final score: {student2.calculate_final_score(policy)}")

if __name__ == "__main__":
    main()
