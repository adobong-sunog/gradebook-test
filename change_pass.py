import sqlite3
import os
from authentication import hashPassword

def changePassword(username, new_pass):
    # Generate salt
    salt = os.urandom(16)
    
    # Hash password with the salt
    hashed_password = hashPassword(new_pass, salt)
    
    if username.lower() == "admin" or username.lower().startswith('tr'):
        conn = sqlite3.connect('database/faculty.db')
        cursor = conn.cursor()
    elif username.lower().startswith('st'):
        conn = sqlite3.connect('database/students.db')
        cursor = conn.cursor()

    cursor.execute("UPDATE users SET salt=?, password=? WHERE username=?", (salt, hashed_password, username))
    conn.commit()
    conn.close()
    print("\nPassword changed successfully.")