# GradeBookApp

GradeBookApp is a comprehensive grade management system that allows educators to set up new semesters, add students, record grades, and calculate final scores. This application provides a user-friendly interface to manage grading policies, student records, and grade calculations efficiently.

## Features

- **Set up new semesters**: Configure the number of assignments, tests, and final exams along with their respective weights.
- **Add students**: Add new students to the gradebook.
- **Record grades**: Record scores for assignments, tests, and final exams.
- **Change grades**: Update scores for assignments, tests, and final exams.
- **Calculate final scores**: Compute the final grades based on recorded scores and grading policies.
- **Output grade data**: Display sorted student records by name or ID.
- **Persistent data storage**: Save and load grading policies and student records from files.

## Installation

To install and run GradeBookApp, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/GradeBookApp.git
    cd GradeBookApp
    ```

3. **Run the application**:
    ```bash
    python gradebook_app.py
    ```

## Usage

### Menu Options

- **(S) Set up new semester**: Configure the number of assignments, tests, final exams, and their respective weights. Ensure the total weight adds up to 100%.
- **(A) Add a student**: Add a new student by providing a unique student ID, first name, and last name.
- **(P) Record programming assignment**: Enter scores for a specific programming assignment for all students.
- **(T) Record test grades for all students**: Enter scores for a specific test for all students.
- **(F) Record Final exam score for all students**: Enter final exam scores for all students.
- **(C) Change a grade**: Update the score of a specific assignment, test, or final exam for a student.
- **(G) Calculate final score**: Calculate and update the final scores for all students based on recorded grades and grading policy.
- **(O) Output the grade data**: Display student records sorted by name or ID.
- **(Q) Quit**: Exit the application.

### Example Workflow

1. **Set up new semester**:
    - Select 'S' from the menu.
    - Enter the number of assignments, tests, and final exams.
    - Enter their respective weights ensuring the total weight is 100%.

2. **Add a student**:
    - Select 'A' from the menu.
    - Enter the student's ID, first name, and last name.

3. **Record grades**:
    - Select 'P', 'T', or 'F' from the menu based on the type of grade you want to record.
    - Enter the assignment number or test number if prompted.
    - Enter the scores for each student.

4. **Change a grade**:
    - Select 'C' from the menu.
    - Enter the student ID, grade type (P/T/F), and the new score.

5. **Calculate final scores**:
    - Select 'G' from the menu.
    - The application will calculate and update the final scores for all students.

6. **Output the grade data**:
    - Select 'O' from the menu.
    - Choose the sorting method (by name or ID).
    - The application will display the sorted student records.

7. **Quit**:
    - Select 'Q' from the menu to exit the application.

## File Structure

- **gradebook_app.py**: Main application file containing the `GradeBookApp` class and the `main` function to run the application.
- **gradebook.py**: Contains the `Gradebook` class which manages students and grading policies.
- **student.py**: Defines the `Student` class to manage individual student records.
- **policy.py**: Defines the `GradingPolicy` class to manage grading policies.
- **studentrepo.py**: Handles reading and writing student records to and from files.
- **policyrepo.py**: Handles reading and writing grading policies to and from files.



