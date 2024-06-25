import tkinter as tk
import sqlite3
import os
from tkinter import messagebox
from first_menu import firstMenu
from change_pass import changePassword
from authentication import hashPassword

def createUser(username, name, password, year_level=None):
    if username.lower() == "admin" or username.lower().startswith('tr'):
        conn = sqlite3.connect('database/faculty.db')
    elif username.lower().startswith('st'):
        conn = sqlite3.connect('database/students.db')

    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))

    #Check if the username already exists
    existing_user = cursor.fetchone()
    conn.close()

    if existing_user:
        print("Error: Username already exists.")
        return "Username already exists.", False

    # Generate salt
    salt = os.urandom(16)
    
    # Hash password with the salt
    hashed_password = hashPassword(password, salt)
    
    if username.lower().startswith('st'):
        conn = sqlite3.connect('database/students.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, name, salt, password, yearLevel) VALUES (?, ?, ?, ?, ?)", (username, name, salt, hashed_password, year_level))
    elif username.lower() == "admin" or username.lower().startswith('tr'):
        conn = sqlite3.connect('database/faculty.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, name, salt, password) VALUES (?, ?, ?, ?)", (username, name, salt, hashed_password))

    conn.commit()
    conn.close()
    print("\nUser successfully added")
    return "User successfully added.", True

def deleteUser(username):
    # Function to delete a user
    if username.lower().startswith('tr'):
        conn = sqlite3.connect('database/faculty.db')
    elif username.lower().startswith('st'):
        conn = sqlite3.connect('database/students.db')

    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()

    conn.close()
    print("\nUser successfully deleted.")

def traverseUsers():
    # Fetch users from both faculty and students databases
    users = []
    conn_faculty = sqlite3.connect('database/faculty.db')
    cursor_faculty = conn_faculty.cursor()
    cursor_faculty.execute("SELECT username, name FROM users")
    users.extend(cursor_faculty.fetchall())
    conn_faculty.close()

    conn_students = sqlite3.connect('database/students.db')
    cursor_students = conn_students.cursor()
    cursor_students.execute("SELECT username, name FROM users")
    users.extend(cursor_students.fetchall())
    conn_students.close()

    return users

def adminMenu():
    # Function to display admin menu
    admin_window = tk.Tk()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("300x300")
    admin_window.configure(bg="lightblue")

    tk.Label(admin_window, text="Admin Menu", bg="lightblue", font=("Arial", 16)).pack(pady=20)

    tk.Button(admin_window, text="Create User", command=createUserGUI).pack(fill='x', padx=50, pady=5)
    tk.Button(admin_window, text="Delete User", command=deleteUserGUI).pack(fill='x', padx=50, pady=5)
    tk.Button(admin_window, text="Traverse Users", command=traverseUsersGUI).pack(fill='x', padx=50, pady=5)
    tk.Button(admin_window, text="Change User Password", command=changeUserPasswordGUI).pack(fill='x', padx=50, pady=5)
    tk.Button(admin_window, text="Logout", command=lambda: [admin_window.destroy(), firstMenu()]).pack(fill='x', padx=50, pady=5)

    admin_window.mainloop()

def createUserGUI():
    # Function to create user using GUI
    cu_window = tk.Toplevel()
    cu_window.title("Create User")
    cu_window.geometry("300x250")

    tk.Label(cu_window, text="Enter new username:").pack()
    username_entry = tk.Entry(cu_window)
    username_entry.pack()
    tk.Label(cu_window, text="Enter user's full name:").pack()
    name_entry = tk.Entry(cu_window)
    name_entry.pack()
    tk.Label(cu_window, text="Enter password:").pack()
    password_entry = tk.Entry(cu_window, show="*")
    password_entry.pack()
    tk.Label(cu_window, text="Enter year level:").pack()
    year_level_entry = tk.Entry(cu_window)
    year_level_entry.pack()

    def submit_action():
        username = username_entry.get().strip()
        name = name_entry.get().strip()
        password = password_entry.get()
        year_level = year_level_entry.get().strip()
        # Check if all mandatory fields are filled
        if not all([username, name, password]):
            messagebox.showerror("Error", "Please fill all required fields.")
            return
        if username.lower().startswith("st") and not year_level:
            messagebox.showerror("Error", "Please fill the year level.")
            return
        # If user is not student or year level is filled for student, proceed with creating user
        message, success = createUser(username, name, password, year_level)
        messagebox.showinfo("Info", message)
        if success:
            cu_window.destroy()

    tk.Button(cu_window, text="Submit", command=submit_action).pack(pady=10)


def deleteUserGUI():
    # Function to delete user using GUI
    du_window = tk.Toplevel()
    du_window.title("Delete User")
    du_window.geometry("300x200")

    tk.Label(du_window, text="Enter username/user ID to delete:").pack()
    username_entry = tk.Entry(du_window)
    username_entry.pack()

    def delete_action():
        username = username_entry.get().strip() 
        if not username:
            messagebox.showerror("Error", "Please enter a username to delete.")
            return
        deleteUser(username)
        messagebox.showinfo("Success", "If the user existed, they have been deleted.")
        du_window.destroy()

    tk.Button(du_window, text="Delete", command=delete_action).pack(pady=10)

def traverseUsersGUI():
    # Function to traverse users using GUI
    tu_window = tk.Toplevel()
    tu_window.title("Traverse Users")
    tu_window.geometry("300x300")

    # Fetch users
    users = traverseUsers()
    if not users:
        tk.Label(tu_window, text="No users found.").pack(pady=10)
        return

    # Display each user's info
    for user in users:
        user_info = f"Username: {user[0]}, Name: {user[1]}"
        tk.Label(tu_window, text=user_info).pack()

    # Add a close button
    tk.Button(tu_window, text="Close", command=tu_window.destroy).pack(pady=10)

def changeUserPasswordGUI():
    # Function to change user's password using GUI
    cp_window = tk.Toplevel()
    cp_window.title("Change User Password")
    cp_window.geometry("300x200")

    tk.Label(cp_window, text="Enter username:").pack()
    username_entry = tk.Entry(cp_window)
    username_entry.pack()
    tk.Label(cp_window, text="Enter new password:").pack()
    password_entry = tk.Entry(cp_window, show="*")
    password_entry.pack()

    def submit_action():
        username = username_entry.get().strip()
        new_password = password_entry.get().strip()
        if not username or not new_password:
            messagebox.showerror("Error", "Please enter both username and new password.")
            return
        changePassword(username, new_password)
        messagebox.showinfo("Success", "Password changed successfully.")
        cp_window.destroy()

    tk.Button(cp_window, text="Submit", command=submit_action).pack(pady=10)
