import mysql.connector
import matplotlib.pyplot as plt

class StudentReport:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
        self.cursor = None

    def connect_to_database(self):
        self.conn = mysql.connector.connect(**self.db_config)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def fetch_students(self):
        self.cursor.execute("""
            SELECT name, email, mathematics, science, history, english, art, computer_science 
            FROM students_records
        """)
        return self.cursor.fetchall()

    def calculate_report(self, students):
        report_data = []
        total_percentages = 0
        
        for student in students:
            name, email, math, sci, hist, eng, art, cs = student
            grades = [math, sci, hist, eng, art, cs]
            total = sum(map(float, grades))
            percentage = total / 6
            total_percentages += percentage
            report_data.append((name, email, percentage))

        class_average = total_percentages / len(students) if students else 0
        report_data.sort(key=lambda x: x[2], reverse=True)
        return report_data, class_average

    def update_report_table(self, report_data, class_average):
        self.cursor.execute("DELETE FROM report")
        self.conn.commit()

        for data in report_data:
            self.cursor.execute("""
                INSERT INTO report (name, email, percentage, class_average)
                VALUES (%s, %s, %s, %s)
            """, (*data, class_average))
        self.conn.commit()

    def display_top_student(self, report_data):
        
        if report_data:
            top_student = report_data[0]
            print(f"Top Student: {top_student[0]} with {top_student[2]:.2f}%")

    def display_class_average(self, class_average):
        print(f"Class Average: {class_average:.2f}%")

    def plot_top_students(self, report_data):
        top_10_students = report_data[:10]
        names = [student[0] for student in top_10_students]
        percentages = [student[2] for student in top_10_students]

        plt.figure(figsize=(10, 6))
        plt.barh(names, percentages, color='maroon')
        for i, percentage in enumerate(percentages):
            plt.text(percentage + 1, i, f"{percentage:.2f}%", va='center', color='black')

        plt.xlabel('Percentage')
        plt.ylabel('Students')
        plt.title('Top 10 Students by Percentage')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def generate_report(self):
        try:
            self.connect_to_database()
            students = self.fetch_students()
            report_data, class_average = self.calculate_report(students)
            self.update_report_table(report_data, class_average)
            self.display_top_student(report_data)
            self.display_class_average(class_average)
            self.plot_top_students(report_data)
        finally:
            self.close_connection()


# Configuration for the database connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "irutingaboRai1@",
    "database": "students"
}

# Create an instance of the class and generate the report
report = StudentReport(db_config)
report.generate_report()
