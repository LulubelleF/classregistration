# ************************************************************************************************
# CPRG216 - Winter 2024
# Assignment:   Functions, Scoping and Abstraction
#
# Date:         March 2024
# Created By:   Claur, Alessandra
#               Fontelo, Lulubelle
#               Teruel, Bryan Benedict
# ************************************************************************************************
# An educational institution asked you to a develop students registration program. 
# The program allows the following features:
# •	Storing and loading students’ information into/from a file
# •	Adding a new student.
# •	Displaying a list of registered students.
# •	Editing a registered student.
# •	Searching for a registered student.
# •	Deleting a registered student.
# •	Calculating GPA average of the registered students.
# ************************************************************************************************

import os.path

NUM_CHAR = int(60)

# It does not have parameters.
# It displays the welcome message and the menu options.
# It asks the user to select a menu option and returns user’ selection. 
def print_menu():
    print()
    print('*' * 80)
    print(f'{"*** Welcome to Students GPA System! ***":^80}')
    print('*' * 80)
    print("Select from the from the following options")
    print("L - List Students")
    print("A - Add Students")
    print("E - Edit Students")
    print("D - Delete Students")
    print("F - Find a Students")
    print("G - GPA Average")
    print("Q - Quit")

    return input(">>> ")

# •	It receives a list of a student’s information.
# •	It returns a CSV formatted string of the student’s information.
#   o	Example is “John Smith,111,99.0”
def format_student(student_name,student_id,student_gpa):
     return f"{student_name},{student_id},{student_gpa}\n"

# •	It does not have parameters.
# •	It displays the student header which includes Student Name, Student ID, and GPA.
# •	It is used when listing students and finding a student.
def display_std_header():
    print()
    print('=' * 80)
    print(f'{"Student Name":^40}', end="")
    print(f'{"Student ID":^20}', end="")
    print(f'{"Student GPA":^20}')
    print('=' * 80)
    return

# •	It receives a student information.
# •	It displays the report/student header and the student information.
def display_student(name, id, gpa):
    print(f'{name:^40}', end="")
    print(f'{id:^20}', end="")
    print(f'{gpa:^20}')
    return

# •	It receives a list of students’ information.
# •	If the received list is empty, It will display “Students list has no students” error message.
# •	Otherwise, 
#   o	It calls display_std_header() to display the student header.
#   o	It iterates over the students list and display their information.
def list_students(students):
    if len(students) == 0:
        print("Error: Students list has no students")
    else:
        display_std_header()
        for student in students:
            if len(student) >= 3:
                print(f'{student[0]:^40}', end="")
                print(f'{student[1]:^20}', end="")
                print(f'{student[2]:^20}')
    return

# let student ID to accpet numeric values only
def get_student_id():
    while True:
            student_id = input('\nEnter your student ID: ')
            if student_id.isnumeric() and student_id.strip() != "":
                break
            print("Error: Invalid Input. Please enter numeric values.")
    return student_id

# let student name accpet alphabets and white spaces
def get_student_name():
    while True:
        student_name = input("\nEnter the student's name: ")
        if student_name.strip().replace(" ", "").isalpha() and student_name.strip() != "":
            break
        print("Error: Invalid Input. Please enter letters.")
    return student_name.strip().title()

# let student GPA to accept numeric values with decimal
def get_student_gpa():
    while True:
        student_gpa = input("\nEnter the student's GPA: ")
        if student_gpa.replace(".", "").isnumeric() and student_gpa.strip() != "":
            student_gpa = round(float(student_gpa),1)
            break
        print("Error: Invalid Input. Please enter numeric values.")
    return student_gpa


# •	It receives the file name where students information is saved and the list of students.
# •	It asks the user to enter the student id.
# •	It checks whether the student exists or not
#   o	If the student exists, it displays the students already exists.
#   o	If the student does not exist, it will ask the user to enter the student information (name, GPA), 
#       append these information to the student list, and update the students text file. 
def add_student(file_path, students):
    print("Adding a student.....")
    student_id = get_student_id()

    # Check if student exists
    student_exist, _, _, _ = find_student(student_id, students)
    if student_exist >= 0:
        print(f'A student with ID {student_id} already exists.')
    else:
        student_name = get_student_name()
        student_gpa = get_student_gpa()

        # Append new student to the list
        students.append([student_name, student_id, student_gpa])
        
        # Update the students text file
        update_students(file_path, students)

        print(f"The student with id {student_id} is added.")
    return

# •	The program should check whether the student exists or not before calling this function.
# •	It receives the student ID and the students list.
# •	It iterates over the list of students until finding the student. 
# •	Once, the student is located in the list, it asks the user to enter student name, ID, and GPA 
#   and updates the student record in the list.
# •	After executing this function, the program should update the students text file.
def edit_student(file_name, students):
    student_id = get_student_id()
    student_exist, _, _, _ = find_student(student_id, students)

    if student_exist >= 0:
        # Get the information to update
        new_name = get_student_name()
        new_id = get_student_id()
        new_gpa = get_student_gpa()

        students[student_exist][0] = new_name
        students[student_exist][1] = new_id
        students[student_exist][2] = new_gpa

        # Update the students text file
        update_students(file_name, students)
        print("Student information updated successfully.")
    
    else:
        print(f"No student found with ID {student_id}")

    return

# •	The program should check whether the student exists or not before calling this function.
# •	It receives the student information and the students list.
# •	It deletes the student from the students list. 
# •	After executing this function, the program should update the students text file.
def delete_student(student_id, students):
    student_exist, _, _, _ = find_student(student_id, students)
    if student_exist >= 0:
        students.remove(students[student_exist])
        print(f"Student with ID {student_id} deleted")
    else:
        print(f"No student with ID: {student_id}")   

    return

# •	The program should check whether the student exists or not before calling this function.
# •	It receives the student ID and the students list.
# •	It iterates over the list of students until finding the student and returns the student information. 
# •	After executing this function, the program should display the student information if the student exists.
def find_student(student_id, students):
    student_exist = -1
    student_name = ""
    student_gpa = ""
    for index, student in enumerate(students):
        if student[1] == student_id:
            student_exist = index
            student_name = student[0]
            student_gpa = student[2]
            break

    return student_exist, student_name, student_id, student_gpa

# •	It receives the students list.
# •	It processes the students list to extract the GPA for each student and calculate the GPA average. 
# •	It returns the calculated average rounded to 2 decimal digits.
def calculate_average(students):
    total_gpa = 0.0
    num_students = len(students)

    for student in students:
        total_gpa += float(student[2])
    
    average_gpa = total_gpa / num_students
    return round(average_gpa, 2)

# •	It receives the text file name (i.e., students.txt)
# •	It reads students information and load it into a list.
# •	It returns the students list.
# •	Hint: the student list is a 2 dimensional list (i.e. list of students lists). 
#   Each element in this list is another list which has the information of one student.
def load_students(file_name):
    file = open(file_name, 'r')
    students = []
    
    for line in file.readlines():
        line = line.strip()
        student = line.split(sep=',')
        students.append(student)

    file.close()
    print("Students infomation has been loaded from the file.")

    return students

# •	It receives the text file name (i.e., students.txt) and students list.
# •	It reads students list and format the students information to CSV format.
# •	Finally, it writes the formatted students information into the students text file.
def update_students(file_name, students):
    with open(file_name, 'w') as file:
        for student in students:
            file.write(format_student(student[0], student[1], student[2]))
    return

# •	The program execution starts by executing this function.
# •	It asks the user to enter the students text file.
# •	It will ensure that the entered file exists before reading the file content and load it to the student list.
# •	It displays the program menu.
# •	It checked the user selection and accordingly call the appropriate functions.
def main():
    while True:
        file_name = str(input("\nPlease enter the file name to load students information: ")).strip()
        if file_name != "":
            break
        print("Error: Invalid Input. File name cannot be empty.")

    file_path = '.\\' + file_name
    
    menu = ['L', 'A', 'E', 'D', 'F', 'G', 'Q']

    if (os.path.exists(file_path)):
        students = load_students(file_path)
        
        while True:
            user_choice = print_menu()

            if user_choice.upper() not in menu:
                print("Error: Invalid Input.")
            else:
                match user_choice.upper():
                    case 'L':
                        list_students(students)
                    
                    case 'A':
                        add_student(file_path, students)
                    
                    case 'E':
                        edit_student(file_name, students)  
                    
                    case 'D':
                        student_id_input = get_student_id()
                        delete_student(student_id_input, students)
                        update_students(file_path, students)
                    
                    case 'F':
                        student_id_input = get_student_id()
                        student_exist, student_name, student_id, student_gpa = find_student(student_id_input, students)
                       
                        if student_exist >= 0:
                            display_std_header()
                            display_student(student_name, student_id, student_gpa)
                        else:
                            print(f"No student with ID {student_id_input}")
                    
                    case 'G':
                        if len(students) == 0:
                            print("Error: No students found.")
                        else:
                            gpa_average = calculate_average(students)
                            print(f"GPA average is {gpa_average}")
                    
                    case 'Q':
                        print("Thanks and Good Bye!")
                        input("Please press enter to continue...")
                        break
    else:
        print(f"{file_name} does not exist. - Bye")

if __name__ == "__main__":
    main()
