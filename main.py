import json
import os
from typing import Dict, List
from grading_logic import (
    calculate_semester_gpa, calculate_cgpa, get_degree_classification,
    calculate_required_wgp, validate_workload, calculate_grade_point
)

# File paths
DATA_FILE = 'student_data.json'

def load_student_data() -> Dict:
    """Load student data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {
        'student_id': '',
        'name': '',
        'academic_history': {
            '100': {'Semester I': [], 'Semester II': []},
            '200': {'Semester I': [], 'Semester II': []},
            '300': {'Semester I': [], 'Semester II': []},
            '400': {'Semester I': [], 'Semester II': []}
        }
    }

def save_student_data(data: Dict) -> None:
    """Save student data to JSON file"""
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def input_course_data() -> List[Dict]:
    """Input course data for a semester"""
    courses = []
    print("\nEnter course details (leave course name blank to finish):")
    
    while True:
        course_name = input("Course name: ").strip()
        if not course_name:
            break
            
        try:
            credit = int(input("Credit hours: "))
            score = float(input("Score (%): "))
            
            grade, grade_point = calculate_grade_point(score)
            print(f"Grade: {grade}, Grade Point: {grade_point}")
            
            courses.append({
                'name': course_name,
                'credit': credit,
                'score': score,
                'grade': grade,
                'grade_point': grade_point
            })
        except ValueError:
            print("Invalid input. Please enter numbers for credit and score.")
    
    return courses

def display_semester_gpa(student_data: Dict) -> None:
    """Display GPA for a specific semester"""
    print("\nAvailable levels and semesters:")
    for level, semesters in student_data['academic_history'].items():
        print(f"Level {level}: {', '.join(semesters.keys())}")
    
    level = input("Enter level (100, 200, etc.): ")
    semester = input("Enter semester (e.g., 'Semester I'): ")
    
    if level in student_data['academic_history'] and semester in student_data['academic_history'][level]:
        courses = student_data['academic_history'][level][semester]
        gpa, wgp = calculate_semester_gpa(courses)
        total_credits = sum(course['credit'] for course in courses)
        
        print(f"\nSemester: {semester}, Level {level}")
        print(f"Total Credits: {total_credits}")
        print(f"Weighted Grade Points (WGP): {wgp}")
        print(f"GPA: {gpa}")
    else:
        print("Invalid level or semester selected.")

def display_cgpa(student_data: Dict) -> None:
    """Display CGPA and degree classification"""
    cgpa = calculate_cgpa(student_data)
    classification = get_degree_classification(cgpa)
    
    print(f"\nCumulative GPA (CGPA): {cgpa}")
    print(f"Degree Classification: {classification}")
    
    # Calculate remaining credits for degree
    total_credits = 0
    completed_credits = 0
    for level in ['100', '200', '300', '400']:
        for semester in student_data['academic_history'][level].values():
            completed_credits += sum(course['credit'] for course in semester)
    
    # Assuming standard 128-credit degree (16 credits/semester × 8 semesters)
    remaining_credits = max(0, 128 - completed_credits)
    
    if remaining_credits > 0:
        print("\nTo achieve a 1st Class degree (CGPA ≥ 3.6), you need:")
        current_wgp = cgpa * completed_credits
        required_wgp = calculate_required_wgp(current_wgp, '1st Class', remaining_credits)
        print(f"- Additional WGP of {required_wgp} across remaining {remaining_credits} credits")
        
        print("\nTo achieve a 2nd Class Upper degree (CGPA ≥ 3.0), you need:")
        required_wgp = calculate_required_wgp(current_wgp, '2nd Class Upper', remaining_credits)
        print(f"- Additional WGP of {required_wgp} across remaining {remaining_credits} credits")

def add_semester_data(student_data: Dict) -> None:
    """Add course data for a semester"""
    print("\nAvailable levels and semesters:")
    for level, semesters in student_data['academic_history'].items():
        print(f"Level {level}: {', '.join(semesters.keys())}")
    
    level = input("Enter level (100, 200, etc.): ")
    semester = input("Enter semester (e.g., 'Semester I'): ")
    
    if level in student_data['academic_history'] and semester in student_data['academic_history'][level]:
        courses = input_course_data()
        total_credits = sum(course['credit'] for course in courses)
        
        if not validate_workload(total_credits):
            print(f"Error: Semester workload must be between 1-24 credits (entered: {total_credits})")
            return
            
        student_data['academic_history'][level][semester] = courses
        save_student_data(student_data)
        print("Semester data saved successfully.")
    else:
        print("Invalid level or semester selected.")

def main_menu() -> None:
    """Display main menu and handle user input"""
    student_data = load_student_data()
    
    if not student_data['student_id']:
        student_data['student_id'] = input("Enter your student ID: ")
        student_data['name'] = input("Enter your name: ")
        save_student_data(student_data)
    
    while True:
        print("\n----------------------------------")
        print("\n*** UNIVERSITY GRADING SYSTEM ***")
        print("\n----------------------------------")
        print("1. ADD/UPDATE SEMESTER DATA")
        print("2. VIEW SEMESTER GPA")
        print("3. VIEW CGPA AND DEGREE CLASSIFICATION")
        print("4. EXIT")
        print("\n----------------------------------")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            add_semester_data(student_data)
        elif choice == '2':
            display_semester_gpa(student_data)
        elif choice == '3':
            display_cgpa(student_data)
        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()