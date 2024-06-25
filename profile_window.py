import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from change_pass import changePassword

def change_password(parent, username):
    def open_change_password_window():
        window = tk.Toplevel(parent)
        window.title("Change Password")
        window.geometry("300x200")

        label_new_password = tk.Label(window, text="New Password:", font=("Arial", 12, 'bold'), bg='#AED6E8')
        label_new_password.pack(pady=5)

        entry_new_password = tk.Entry(window, show="*")
        entry_new_password.pack(pady=5)

        label_confirm_password = tk.Label(window, text="Confirm Password:", font=("Arial", 12, 'bold'), bg='#AED6E8')
        label_confirm_password.pack(pady=5)

        entry_confirm_password = tk.Entry(window, show="*")
        entry_confirm_password.pack(pady=5)

        def submit_action():
            # Get inputs from entry fields
            new_password = entry_new_password.get().strip()
            confirm_password = entry_confirm_password.get().strip()

            # Validate inputs
            if not new_password or not confirm_password:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match. Please try again.")
                return

            # Call the changePassword function from change_pass.py
            changePassword(username, new_password)

            window.destroy()

        tk.Button(window, text="Submit", command=submit_action).pack(pady=10)

    open_change_password_window()

def edit_profile_window(parent, username):
    window = tk.Toplevel(parent)
    window.title("Edit Profile")
    window.geometry("400x400")

    button_change_password = ttk.Button(window, text="Change Password", command=lambda: change_password(parent, username))
    button_change_password.grid(row=4, column=0, padx=10, pady=10, sticky='w')

    # Profile Picture Label
    profile_image = Image.open("images/profile.png")
    profile_image = profile_image.resize((100, 100), Image.LANCZOS)
    photo = ImageTk.PhotoImage(profile_image)
    label_profile_picture = tk.Label(window, image=photo)
    label_profile_picture.image = photo
    label_profile_picture.grid(row=4, column=1, padx=10, pady=10)

    window.mainloop()
