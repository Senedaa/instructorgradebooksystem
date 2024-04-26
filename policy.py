class GradingPolicy:
    def __init__(self, num_assignments: int = 0, num_tests: int = 0, num_finals: int = 0, weights: dict[str, float] = None) -> None:
        self.__num_assignments = num_assignments
        self.__num_tests = num_tests
        self.__num_finals = num_finals
        if weights is None:
            self.__weights= {}
        else:
            self.__weights = weights

    @property
    def num_assignments(self)->int:
        return self.__num_assignments

    @property
    def num_tests(self)->int:
        return self.__num_tests

    @property
    def num_finals(self)->int:
        return self.__num_finals

    def setup_grading_policy(self, num_assignments: int, num_tests: int, num_finals: int, assignment_weight: float, test_weight: float, final_exam_weight: float)->None:
        if (assignment_weight + test_weight + final_exam_weight) != 100:
            raise ValueError("The total weight of all components must sum to 100%.")
        self.__num_assignments = num_assignments
        self.__num_tests = num_tests
        self.__num_finals = num_finals
        self.__weights['assignments'] = assignment_weight
        self.__weights['tests'] = test_weight
        self.__weights['final_exam'] = final_exam_weight

    def get_weight(self, component: str)->float:
        return self.__weights.get(component, 0)
    
    def check_weight(self)->bool:
        return bool(self.__weights)

        
    def __str__(self) -> str:
        if not self.__weights:
            return (f"Grading Policy (Uninitialized Weights):\n"
                    f" - Number of Assignments: {self.num_assignments}\n"
                    f" - Number of Tests: {self.num_tests}\n"
                    f" - Number of Finals: {self.num_finals}\n")
        else:
            return (f"Grading Policy:\n"
                    f" - Number of Assignments: {self.num_assignments}, Weight: {self.__weights.get('assignments', 0)}%\n"
                    f" - Number of Tests: {self.num_tests}, Weight: {self.__weights.get('tests', 0)}%\n"
                    f" - Number of Finals: {self.num_finals}, Weight: {self.__weights.get('final_exam', 0)}%")


    def __repr__(self):
        return str(self)

def main():
    policy = GradingPolicy(num_assignments=3, num_tests=2, num_finals=1)
    print("Initial Grading Policy:")
    print(policy)

    policy.setup_grading_policy(num_assignments=5, num_tests=2, num_finals=1, assignment_weight=40, test_weight=30, final_exam_weight=30)
    print("\nUpdated Grading Policy:")
    print(policy)

    print("\nSpecific Component Weights:")
    print(f"Weight for Assignments: {policy.get_weight('assignments')}%")
    print(f"Weight for Tests: {policy.get_weight('tests')}%")
    print(f"Weight for Final Exams: {policy.get_weight('final_exam')}%")

if __name__ == "__main__":
    main()
