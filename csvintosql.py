import mysql.connector
import pandas as pd
from dbconnection import DataBaseConnection

class StudentDatabaseManagement:
    def __init__(self):
        # Use the singleton pattern to get the single instance of the database connection
        self.db_connection = DataBaseConnection()
        self.conn = self.db_connection.conn
        self.cursor = self.db_connection.cursor

    def read_csv(self, csv_file):
        try:
            data = pd.read_csv(csv_file)
            print("CSV Columns:", data.columns)
            return data
        except FileNotFoundError:
            print(f"Error: File {csv_file} not found.")
            return None
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return None

    def add_data_to_database(self, data):
        if self.conn is None or self.cursor is None:
            print("Database connection is not established.")
            return
        
        try:
            for _, row in data.iterrows():
                self.cursor.execute("""
                    INSERT INTO students_records (Name, Email, Phone_Number, Mathematics, Science, History, English, Art, Computer_Science)
                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s)
                """, (
                    row['Name'],
                    row['Email'],
                    row['Phone_Number'],
                    row['Mathematics'],
                    row['Science'],
            
            
                    row['History'],
                    row['English'],
                    row['Art'],
                    row['Computer_Science']
                ))
            self.conn.commit()
            print("Data imported successfully!")
        except KeyError as e:
            print(f"Error: Missing column in CSV: {e}")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    def import_csv_to_database(self, csv_file):
        data = self.read_csv(csv_file)
        if data is not None:
            self.add_data_to_database(data)
            
if __name__ == "__main__":
    db_manager = StudentDatabaseManagement()
    csv_file_path = "./student_records.csv"
    db_manager.import_csv_to_database(csv_file_path)
