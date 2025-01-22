import mysql.connector
from dbconnection import DataBaseConnection


class StudentReport:
    """Class to handle student report generation and database updates."""

    def __init__(self):
        """Initialize with a database connection."""
        self.db_connection = DataBaseConnection()
        self.conn = self.db_connection.conn
        self.cursor = self.db_connection.cursor

    def fetch_students(self):
        """Retrieve all student records from the database."""
        try:
            self.cursor.execute("""
                SELECT name, email, mathematics, science, history, english, art, computer_science
                FROM students_records
            """)
            students = self.cursor.fetchall()
            return students
        except mysql.connector.Error as err:
            print(f"Error fetching student data: {err}")
            return []

    def calculate_report(self, students):
        """Calculate individual student percentages and the class average."""
        report_data = []
        total_percentages = 0

        for student in students:
            name, email, math, sci, hist, eng, art, cs = student
            grades = [math, sci, hist, eng, art, cs]
            total = sum(map(float, grades))  # Convert grades to float and sum them
            percentage = total / len(grades)  # Calculate percentage
            total_percentages += percentage
            report_data.append((name, email, percentage))

        # Calculate class average
        class_average = total_percentages / len(students) if students else 0

        # Sort report data by percentage in descending order
        report_data.sort(key=lambda x: x[2], reverse=True)

        return report_data, class_average

    def update_report_table(self, report_data, class_average):
        """Update the report table with the latest report data."""
        try:
            # Clear the existing data in the report table
            self.cursor.execute("DELETE FROM report")
            self.conn.commit()

            # Insert new report data
            for data in report_data:
                self.cursor.execute("""
                    INSERT INTO report (name, email, percentage, class_average)
                    VALUES (%s, %s, %s, %s)
                """, (*data, class_average))
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error updating report table: {err}")

    def generate_report(self):
        """Generate the report and display key metrics."""
        students = self.fetch_students()
        if not students:
            print("No student data found.")
            return

        report_data, class_average = self.calculate_report(students)
        self.update_report_table(report_data, class_average)

        # Print the top student and class average
        if report_data:
            top_student = report_data[0]
            print(f"Top Student: {top_student[0]} with {top_student[2]:.2f}%")
        print(f"Class Average: {class_average:.2f}%")

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.db_connection.close()


# Main function to generate the report
if __name__ == "__main__":
    student_report = StudentReport()
    try:
        student_report.generate_report()
    finally:
        student_report.close()
