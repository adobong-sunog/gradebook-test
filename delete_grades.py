import sqlite3

def deleteGrades(subj_code, student_id, teacher_id):
    try:
        # Connect to database
        connection = sqlite3.connect('database/records.db')
        cursor = connection.cursor()

        # Check if the provided teacher ID matches the teacher associated with the subject code
        cursor.execute("SELECT teacher FROM grades_table WHERE subjectCode=?", (subj_code,))
        subject_teacher = cursor.fetchone()

        if subject_teacher is None:
            raise ValueError("\nSubject code not found.")
        elif subject_teacher[0] != teacher_id:
            raise PermissionError("\nYou do not have permission to delete grades for this subject.")

        # Delete grades only for the specific student and teacher
        cursor.execute("DELETE FROM grades_table WHERE subjectCode=? AND studentID=? AND teacher=?", (subj_code, student_id, teacher_id))

        # Confirm changes and close connection
        connection.commit()
        connection.close()
        print("Grades deleted successfully.")
    except Exception as e:
        print("Error deleting grades:", str(e))
