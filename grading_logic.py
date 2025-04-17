import json
from typing import Dict, List, Tuple, Union

# Grade mapping
GRADE_MAPPING = {
    'A': (80, 100, 4.00),
    'A-': (75, 79, 3.85),
    'B+': (70, 74, 3.50),
    'B': (65, 69, 3.00),
    'C+': (60, 64, 2.50),
    'C': (55, 59, 2.00),
    'D': (50, 54, 1.50),
    'E': (45, 49, 1.00),
    'F': (0, 44, 0),
    'X': (0, 0, 0),
    'Z': (None, None, None),
    'I': (None, None, None),
    'Y': (None, None, None),
    'S': (None, None, None),
    'M': (None, None, None)
}

# Degree classification
DEGREE_CLASSIFICATION = {
    '1st Class': (3.6, 4.0),
    '2nd Class Upper': (3.0, 3.59),
    '2nd Class Lower': (2.5, 2.99),
    '3rd Class': (2.0, 2.49),
    'Pass': (1.5, 1.99),
    'Fail': (0, 1.49)
}

def calculate_grade_point(score: float) -> Tuple[str, float]:
    """Calculate grade and grade point based on score"""
    for grade, (min_score, max_score, point) in GRADE_MAPPING.items():
        if min_score is not None and max_score is not None:
            if min_score <= score <= max_score:
                return grade, point
    return 'F', 0.0

def calculate_semester_gpa(courses: List[Dict]) -> Tuple[float, float]:
    """Calculate semester GPA and total WGP"""
    total_credits = 0
    total_wgp = 0
    
    for course in courses:
        credit = course['credit']
        score = course['score']
        _, grade_point = calculate_grade_point(score)
        wgp = credit * grade_point
        
        total_credits += credit
        total_wgp += wgp
    
    if total_credits == 0:
        return 0.0, 0.0
    
    gpa = total_wgp / total_credits
    return round(gpa, 2), total_wgp

def calculate_cgpa(student_data: Dict) -> float:
    """Calculate cumulative GPA across all semesters"""
    total_wgp = 0
    total_credits = 0
    
    for level, semesters in student_data['academic_history'].items():
        for semester, courses in semesters.items():
            _, semester_wgp = calculate_semester_gpa(courses)
            semester_credits = sum(course['credit'] for course in courses)
            
            total_wgp += semester_wgp
            total_credits += semester_credits
    
    if total_credits == 0:
        return 0.0
    
    cgpa = total_wgp / total_credits
    return round(cgpa, 2)

def get_degree_classification(cgpa: float) -> str:
    """Determine degree classification based on CGPA"""
    for classification, (min_gpa, max_gpa) in DEGREE_CLASSIFICATION.items():
        if min_gpa <= cgpa <= max_gpa:
            return classification
    return 'Unknown'

def calculate_required_wgp(current_wgp: float, target_class: str, remaining_credits: int) -> float:
    """Calculate required WGP to achieve target degree classification"""
    target_min = DEGREE_CLASSIFICATION.get(target_class, (0, 0))[0]
    if target_min == 0:
        return 0.0
    
    required_total_wgp = target_min * (current_wgp / 3.0 + remaining_credits)
    required_additional_wgp = max(0, required_total_wgp - current_wgp)
    return round(required_additional_wgp, 2)

def validate_workload(credits: int) -> bool:
    """Validate semester workload (1-24 credits)"""
    return 1 <= credits <= 24