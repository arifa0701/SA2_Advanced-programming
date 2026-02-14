"""STUDENT MANAGER"""
import tkinter as tk
from tkinter import ttk, messagebox  # Importing required modules for GUI


# Data Load

def load_data(filename):
    students = []  # List to store student data
    try:
        with open(filename, "r") as file:  # Open file for reading
            n = int(file.readline().strip())  # First line = number of students
            for _ in range(n):
                parts = [p.strip() for p in file.readline().split(",")]  # Split line by comma
                if len(parts) < 6:
                    continue  # Skip if incomplete data
                code = parts[0]
                name = parts[1]
                coursework = list(map(int, parts[2:5]))  # Convert coursework marks to integers
                exam = int(parts[5])  # Convert exam mark to integer
                students.append({
                    "code": code,
                    "name": name,
                    "coursework": coursework,
                    "exam": exam
                })
    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt not found!")  # Show error if file missing
    return students  # Return the list of students

# -----------------------------
# Marks calculation
# -----------------------------
def calculate(student):
    cw_total = sum(student["coursework"])  # Total coursework marks
    total = cw_total + student["exam"]  # Add exam mark
    percent = (total / 160) * 100  # Calculate percentage
    # Determine grade based on percentage
    if percent >= 70:
        grade = "A"
    elif percent >= 60:
        grade = "B"
    elif percent >= 50:
        grade = "C"
    elif percent >= 40:
        grade = "D"
    else:
        grade = "F"
    return cw_total, total, percent, grade  # Return results


# Display Functions

def clear_text():
    text_box.config(state=tk.NORMAL)  # Enable editing
    text_box.delete(1.0, tk.END)  # Clear text box

def display(student):
    cw, total, pct, grade = calculate(student)  # Get student marks and grade
    # Display student information
    text_box.insert(tk.END, f"Name: {student['name']}\n")
    text_box.insert(tk.END, f"Number: {student['code']}\n")
    text_box.insert(tk.END, f"Coursework Total: {cw}\n")
    text_box.insert(tk.END, f"Exam Mark: {student['exam']}\n")
    text_box.insert(tk.END, f"Overall Percentage: {pct:.2f}%\n")
    text_box.insert(tk.END, f"Grade: {grade}\n\n")

def view_all():
    clear_text()  # Clear text box first
    total_pct = 0
    for s in students:  # Loop through all students
        display(s)
        total_pct += calculate(s)[2]  # Add percentage
    avg = total_pct / len(students)  # Calculate average
    text_box.insert(tk.END, f"Total Students: {len(students)}\n")
    text_box.insert(tk.END, f"Average Percentage: {avg:.2f}%\n")
    text_box.config(state=tk.DISABLED)  # Disable editing

def show_highest():
    clear_text()
    if not students:
        return
    top = max(students, key=lambda s: calculate(s)[1])  # Find student with highest total
    text_box.insert(tk.END, "Student with Highest Score:\n\n")
    display(top)
    text_box.config(state=tk.DISABLED)

def show_lowest():
    clear_text()
    if not students:
        return
    low = min(students, key=lambda s: calculate(s)[1])  # Find student with lowest total
    text_box.insert(tk.END, "Student with Lowest Score:\n\n")
    display(low)
    text_box.config(state=tk.DISABLED)

def view_individual():
    name = selected_student.get()  # Get selected student name
    clear_text()
    if not name:
        text_box.insert(tk.END, "Please select a student.")
        text_box.config(state=tk.DISABLED)
        return
    student = next((s for s in students if s["name"] == name), None)  # Find student by name
    if student:
        display(student)
    else:
        text_box.insert(tk.END, "Student not found.")
    text_box.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()  # Create main window
root.title("Student Manager")
root.geometry("800x500")  # Set window size

# Load student data from file
students = load_data("resources/studentMarks.txt")

# Title label
title = tk.Label(root, text="Student Manager", font=("Arial", 18, "bold"), bg="white")
title.pack(pady=10)

# Frame for main buttons
button = tk.Frame(root, bg="white")
button.pack(pady=10)

# Buttons for viewing data
all_button = tk.Button(button, text="View All Student Records", width=20, command=view_all)
highest_button = tk.Button(button, text="Show Highest Score", width=20, command=show_highest)
lowest_button = tk.Button(button, text="Show Lowest Score", width=20, command=show_lowest)

# Positioning buttons
all_button.grid(row=0, column=0, padx=10)
highest_button.grid(row=0, column=1, padx=10)
lowest_button.grid(row=0, column=2, padx=10)


# Individual Record Section
frame_individual = tk.Frame(root, bg="light blue")
frame_individual.pack(pady=10)

l1_select = tk.Label(frame_individual, text="View Individual Student Record:", bg="sky blue", font=("Arial", 12))
l1_select.grid(row=0, column=0, padx=5)

selected_student = tk.StringVar()  # Variable to store selected name
names = [s["name"] for s in students]  # List of student names
dropdown = ttk.Combobox(frame_individual, textvariable=selected_student, values=names, width=25)
dropdown.grid(row=0, column=1, padx=5)

button_view = tk.Button(frame_individual, text="View Record", command=view_individual, width=12)
button_view.grid(row=0, column=2, padx=5)

# Output Box

frame_text = tk.Frame(root, bg="light blue")
frame_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

text_box = tk.Text(frame_text, height=15, font=("Arial", 12))  # Text area for output
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Run the main GUI loop
root.mainloop()


