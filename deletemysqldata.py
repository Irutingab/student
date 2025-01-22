import mysql.connector
import pandas as pd
from dbconnection import DataBaseConnection

class TruncateDatabase:
    def __init__(self):
        # Use the singleton pattern to get the single instance of the database connection
        self.db_connection = DataBaseConnection()
        self.conn = self.db_connection.conn
        self.cursor = self.db_connection.cursor

    def truncate_database(self):
        if not self.cursor:
            print("No active database connection.")
            return
        try:
            self.cursor.execute("TRUNCATE TABLE report") 
            self.conn.commit()
            print("Table truncated successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

if __name__ == "__main__":
    db_manager = TruncateDatabase()
db_manager.truncate_database()