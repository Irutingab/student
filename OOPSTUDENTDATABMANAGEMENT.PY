import mysql.connector
import csv
from dbconnection import DataBaseConnection

class StudentDatabaseManagement:
    def __init__(self):
        # Use the singleton pattern to get the single instance of the database connection
        self.db_connection = DataBaseConnection()
        self.conn = self.db_connection.conn
        self.cursor = self.db_connection.cursor

    def check_for_duplicate_email(self, email):
        """ Helper method to check if email already exists in the database """
        self.cursor.execute("SELECT * FROM students_records WHERE email = %s", (email,))
        return self.cursor.fetchone()

    def save_failed_email(self, email):
        """ Save failed email to CSV """
        with open('failedstudents.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email])
        print(f"Duplicate email {email} saved to 'failedstudents.csv'.")

    def add_new_student(self):
        """ Add a new student record to the database """
        print("Enter the details of the new student:")
        name = input("Enter the student's name: ")
        email = input("Enter the student's email: ")

        # Check for duplicate email
        if self.check_for_duplicate_email(email):
            print("Error: This email already exists!")
            self.save_failed_email(email)
        else:
            phone_number = input("Enter the student's phone number: ")
            grades = {
                "mathematics": input("Enter the grade for Mathematics: "),
                "science": input("Enter the grade for Science: "),
                "history": input("Enter the grade for History: "),
                "english": input("Enter the grade for English: "),
                "art": input("Enter the grade for Art: "),
                "computer_science": input("Enter the grade for Computer Science: "),
            }

            # Insert student record
            self.cursor.execute("""
                INSERT INTO students_records (name, email, phone_number, mathematics, science, history, english, art, computer_science) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, phone_number, grades["mathematics"], grades["science"], grades["history"], 
                grades["english"], grades["art"], grades["computer_science"]))
            self.conn.commit()
            print("New student added successfully!")

    def update_student_info(self):
        """ Update student information based on email """
        email_to_update = input("Enter the student's email to update: ")

        # Check if student exists
        self.cursor.execute("SELECT * FROM students_records WHERE email = %s", (email_to_update,))
        student = self.cursor.fetchone()
        if not student:
            print("Error: No student found with this email.")
            return

        print(f"Student found: {student}")
        print("What would you like to update?")
        print("1. Update name")
        print("2. Update grades")
        print("3. Update email")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            new_name = input(f"Enter the new name (current: {student[0]}): ")
            self.cursor.execute("UPDATE students_records SET name = %s WHERE email = %s", (new_name, email_to_update))
            self.conn.commit()
            print("Name updated successfully!")
        elif choice == '2':
            grades = {
                "mathematics": input(f"Enter new grade for Mathematics (current: {student[3]}): ") or student[3],
                "science": input(f"Enter new grade for Science (current: {student[4]}): ") or student[4],
                "history": input(f"Enter new grade for History (current: {student[5]}): ") or student[5],
                "english": input(f"Enter new grade for English (current: {student[6]}): ") or student[6],
                "art": input(f"Enter new grade for Art (current: {student[7]}): ") or student[7],
                "computer_science": input(f"Enter new grade for Computer Science (current: {student[8]}): ") or student[8],
            }
            self.cursor.execute("""
                UPDATE students_records 
                SET mathematics = %s, science = %s, history = %s, english = %s, art = %s, computer_science = %s
                WHERE email = %s
            """, (grades["mathematics"], grades["science"], grades["history"], grades["english"], 
                grades["art"], grades["computer_science"], email_to_update))
            self.conn.commit()
            print("Grades updated successfully!")
        elif choice == '3':
            new_email = input(f"Enter the new email (current: {student[2]}): ")
            if self.check_for_duplicate_email(new_email):
                print("Error: This email already exists!")
                self.save_failed_email(new_email)
            else:
                self.cursor.execute("UPDATE students_records SET email = %s WHERE email = %s", (new_email, email_to_update))
                self.conn.commit()
                print("Email updated successfully!")
        else:
            print("Invalid choice! Please try again.")

    def delete_student_info(self):
        """ Delete student record based on email """
        email_to_delete = input("Enter the student's email to delete: ")

        # Check if student exists
        self.cursor.execute("SELECT * FROM students_records WHERE email = %s", (email_to_delete,))
        student = self.cursor.fetchone()
        if not student:
            print("Error: No student found with this email.")
            return

        confirm = input(f"Are you sure you want to delete the record for {student[0]} (y/n)? ")
        if confirm.lower() == 'y':
            self.cursor.execute("DELETE FROM students_records WHERE email = %s", (email_to_delete,))
            self.conn.commit()
            print("Student record deleted successfully.")
        else:
            print("Deletion canceled.")

    def main(self):
        """ Main menu for database management """
        while True:
            print("\nStudent Database Management")
            print("1. Add New Student")
            print("2. Update Student Information")
            print("3. Delete Student Information")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_new_student()
            elif choice == '2':
                self.update_student_info()
            elif choice == '3':
                self.delete_student_info()
            elif choice == '4':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    db_manager = StudentDatabaseManagement()
db_manager.main()
