import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from first_menu import firstMenu
from upload_file import browseFile
from delete_grades import deleteGrades
from profile_window import change_password

def teacherMenu(username):
    def exit_application():
        root.destroy()

    def open_profile_menu(event):
        profile_menu.post(label_profile_icon.winfo_rootx(), label_profile_icon.winfo_rooty() + label_profile_icon.winfo_height())

    def displayUploadWindow():
        browseFile(root, result_label, username)

    def displayDeleteWindow():
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Grades")
        delete_window.geometry("300x150")
        delete_window.resizable(False, False)

        def confirm_delete():
            subject_code = subject_code_entry.get().strip()
            student_id = student_id_entry.get().strip()
            if not subject_code or not student_id:
                messagebox.showerror("Error", "Please fill in both Subject Code and Student ID.")
                return
            deleteGrades(subject_code, student_id, username)
            delete_window.destroy()

        subject_code_label = tk.Label(delete_window, text="Subject Code:", font=("Arial", 12, "bold"))
        subject_code_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        subject_code_entry = tk.Entry(delete_window, font=("Arial", 12))
        subject_code_entry.grid(row=0, column=1, padx=10, pady=5)

        student_id_label = tk.Label(delete_window, text="Student ID:", font=("Arial", 12, "bold"))
        student_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        student_id_entry = tk.Entry(delete_window, font=("Arial", 12))
        student_id_entry.grid(row=1, column=1, padx=10, pady=5)

        confirm_button = tk.Button(delete_window, text="Confirm Delete", font=("Arial", 12), command=confirm_delete)
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def display_students(subject):
        # Fetch students enrolled in the subject where the teacher is the instructor
        conn = sqlite3.connect('database/records.db')
        cursor = conn.cursor()
        cursor.execute("SELECT studentID FROM grades_table WHERE subjectCode=? AND teacher=?", (subject, username))
        student_ids = [row[0] for row in cursor.fetchall()]
        conn.close()

        if student_ids:
            students = []
            # Fetch names of students using student IDs
            conn = sqlite3.connect('database/students.db')
            cursor = conn.cursor()
            for student_id in student_ids:
                cursor.execute("SELECT name FROM users WHERE username=?", (student_id,))
                name = cursor.fetchone()[0]
                students.append(name)
            conn.close()
            messagebox.showinfo("Students Enrolled", "\n".join(students))
        else:
            messagebox.showinfo("No Students", "No students are enrolled in this subject.")

    root = tk.Tk()
    root.title("GradeBook Groove")
    root.geometry('1280x720')
    root.configure(bg='#AED6E8')

    # Load the profile icon
    profile_image = Image.open("images/profile.png")
    profile_image = profile_image.resize((50, 50), Image.LANCZOS)
    profile_icon = ImageTk.PhotoImage(profile_image)

    label_profile_icon = tk.Label(root, image=profile_icon, bg='#AED6E8')
    label_profile_icon.image = profile_icon
    label_profile_icon.place(x=1230, y=10, anchor='ne')
    label_profile_icon.bind("<Button-1>", open_profile_menu)

    # Create the profile menu
    profile_menu = tk.Menu(root, tearoff=0)
    profile_menu.add_command(label="Logout", command=lambda: logout(root))

    # Get name from the database
    def get_name(username):
        conn = sqlite3.connect('database/faculty.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        name = row[0] if row else ""
        conn.close()
        return name

    # Profile Icon and UserName
    name = get_name(username)
    label_username = tk.Label(root, text=name, font=("Arial", 12, 'bold'), bg='#AED6E8')
    label_username.place(x=1150, y=30, anchor='ne')

    # Separator for Top section
    separator_top = tk.Frame(root, bg='black', height=2, width=1280)
    separator_top.place(x=0, y=80, anchor='nw')

    # Navigation
    label_navigation = tk.Label(root, text="NAVIGATION", font=("Arial", 18, "bold"), bg='#AED6E8')
    label_navigation.place(x=10, y=100, anchor='nw')

    # Separator for Bottom section
    separator_bottom = tk.Frame(root, bg='black', height=2, width=1280)
    separator_bottom.place(x=0, y=150, anchor='nw')

    # Upload File Button
    button_upload_file = tk.Button(root, text="UPLOAD FILE", font=("Arial", 14, "bold"), bg='#AED6E8', relief="flat", command=displayUploadWindow)
    button_upload_file.place(x=20, y=190, anchor='nw')

    # Delete Grades
    button_delete_grades = tk.Button(root, text="DELETE GRADES", font=("Arial", 14, "bold"), bg='#AED6E8', relief="flat", command=displayDeleteWindow)
    button_delete_grades.place(x=20, y=230, anchor='nw')

    # Change Password
    button_change_password = tk.Button(root, text="CHANGE PASSWORD", font=("Arial", 14, "bold"), bg='#AED6E8', relief="flat", command=lambda: change_password(root, username))
    button_change_password.place(x=20, y=270, anchor='nw')

    # Logout
    button_logout = tk.Button(root, text="LOGOUT", font=("Arial", 14, "bold"), bg='#AED6E8', relief="flat", command=lambda: logout(root))
    button_logout.place(x=20, y=310, anchor='nw')

    # Separator for Bottom section
    separator_bottom = tk.Frame(root, bg='black', height=2, width=1280)
    separator_bottom.place(x=0, y=360, anchor='nw')

    label_subs_handled = tk.Label(root, text="SUBJECTS HANDLED", font=("Arial", 18, "bold"), bg='#AED6E8')
    label_subs_handled.place(x=10, y=380, anchor='nw')

    # Fetch subjects handled by the teacher
    conn = sqlite3.connect('database/records.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT subjectCode FROM grades_table WHERE teacher=?", (username,))
    subjects = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Display buttons for each subject
    for i, subject in enumerate(subjects):
        button_subject = tk.Button(root, text=subject, font=("Arial", 14, "bold"), bg='#AED6E8', relief="flat", command=lambda subj=subject: display_students(subj))
        button_subject.place(x=20, y=430 + i*40, anchor="nw")

    def logout(window):
        window.destroy()
        firstMenu()

    # Result label
    result_label = tk.Label(root, text="", bg="lightblue")
    result_label.place(x=470, y=310, anchor='nw')

    root.protocol("WM_DELETE_WINDOW", exit_application)
    root.mainloop()
