from policy import GradingPolicy
import os
import json

class PolicyRepo:
    def __init__(self, filename:str) -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.__filename = os.path.join(script_dir, filename)

    def save_policy_to_file(self, policy:GradingPolicy)->None:
        with open(self.__filename, 'w') as file:
            data = {
                'num_assignments': policy.num_assignments,
                'num_tests': policy.num_tests,
                'num_finals': policy.num_finals,
                'weights': {
                    'assignments': policy.get_weight('assignments'),
                    'tests': policy.get_weight('tests'),
                    'final_exam': policy.get_weight('final_exam')
                }
            }
            json.dump(data, file)


    def read_policy_from_file(self) -> GradingPolicy:
        try:
            with open(self.__filename, 'r') as file:
                data = json.load(file)
                num_assignments = data.get('num_assignments', 0)
                num_tests = data.get('num_tests', 0)
                num_finals = data.get('num_finals', 0)
                weights = data.get('weights', None)

                return GradingPolicy(num_assignments, num_tests, num_finals, weights)
        except FileNotFoundError:
            return GradingPolicy()
        except json.JSONDecodeError:
            print("Error decoding JSON from the policy file.")
            return GradingPolicy()




def main():
    policy_repo = PolicyRepo("policy.dat")
    policy = GradingPolicy()
    policy.setup_grading_policy(
        num_assignments=5,
        num_tests=2,
        num_finals=1,
        assignment_weight=40,
        test_weight=30,
        final_exam_weight=30
    )
    policy_repo.save_policy_to_file(policy)
    print("Grading Policy has been saved to the file.")

    loaded_policy = policy_repo.read_policy_from_file()
    print(loaded_policy)
if __name__ == "__main__":
    main()


