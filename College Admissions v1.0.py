import csv

def convert_row_type(row):
    for i in range(len(row) - 1):
            row[i] = float(row[i])
    return row

def calculate_score(sat, gpa, interest, quality, state):
    gpa_score = 0.40 * (gpa * 2)
    sat_score = (sat // 160) * 0.30
    quality_score = quality * 0.20
    interest_score = interest * 0.05
    state_score = state * 0.05
    return gpa_score + sat_score + quality_score + interest_score + state_score

def is_outlier(sat, gpa, interest_score):
    gpa_difference = (gpa * 2) - (sat / 160)
    return interest_score == 0 or gpa_difference >= 2

def get_score(student):
    return float(student[1])

def encode_in_out(state):
    return 1 if state == "in" else 0

def gpa_checker(semesters):
    sorted_semesters = sorted(semesters)
    convert_row_type(sorted_semesters)
    return (sorted_semesters[1] - sorted_semesters[0]) > 20

def grade_improvement(grades):
    convert_row_type(grades)
    for i in range(len(grades) - 1):
        if grades[i] > grades[i + 1]:
            return False
    return True

def students_score(in_file, out_file):
    with open(in_file, 'r') as file:
        lines = file.readlines()

    student_scores = []

    for line in lines:
        student_scores = [(line.rsplit(' ', 1)[0], float(line.rsplit(' ', 1)[1].strip())) for line in lines]
        sorted_scores = sorted(student_scores, key=get_score, reverse=True)

    with open(out_file, 'w') as file:
        for name, score in sorted_scores:
            file.write(f'{name} {score}\n')

#Main Method
def main():

    with open('admissions_test1.csv', newline="") as file:
    # with open('admissions_test2.csv', newline="") as file:

        csvreader = csv.reader(file, delimiter=',')

        headers1 = [0, 1, 2, 3, 8]
        headers2 = [4, 5, 6, 7]

        list1, list2 = [], []
        names = []

        for line in csvreader:
            names.append(line.pop(0))
            headers1.append([line[h] for h in headers1])
            headers2.append([line[h] for h in headers2])

        for row in list1:
            row[4] = encode_in_out(row[4])

        outliers = open("outliers.txt", "w")
        chosen_student = open("unsorted_chosen_students.txt", "w")
        improved = open("chosen_improved.txt", "w")
        extra_unsorted = open("unsorted_extra_improved_chosen.txt", "w")

        for i in range(2, len(list1) - 1):
            float_rows = convert_row_type(list1[i])
            student_score = calculate_score(*float_rows)

            # writes to a file
            def write_if(condition, file):
                if condition:
                    file.write(f"{names[i]}{student_score}\n")

            # Problem 1
            write_if(student_score >= 6.0, chosen_student)

            # Problem 2
            is_outlier_condition = is_outlier(float_rows[0], float_rows[1], float_rows[2])
            write_if(is_outlier_condition and student_score >= 5.0, outliers)

            # Problem 3
            write_if(student_score >= 6.0 or (is_outlier_condition and student_score >= 5.0), improved)

           # Problem 4
            gpa_improvement = gpa_checker(list2[i])
            grade_improvement_check = grade_improvement(list2[i])
            write_if(student_score >= 6.0 or (student_score >= 5.0 and (is_outlier_condition or gpa_improvement or grade_improvement_check)), extra_unsorted)

        outliers.close()
        chosen_student.close()
        improved.close()
        extra_unsorted.close()

        students_score("unsorted_chosen_students.txt", "chosen_students.txt")
        students_score("unsorted_extra_improved_chosen.txt", "extra_improved_chosen.txt")

