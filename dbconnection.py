import mysql.connector
import os
from dotenv import load_dotenv #to load environment variables from .env file

# Load DB credentials)
load_dotenv()

class DataBaseConnection:
    _instance = None #ensures only one database connection is created(singleton pattern)
    #Ensures that only one instance of DataBaseConnection exists.
    def __new__(cls):
        """Create a single instance of the database connection"""
        if not cls._instance:
            cls._instance = super(DataBaseConnection, cls).__new__(cls)
            cls._instance.connect()
        return cls._instance

    def connect(self):
        """Establish a database connection from the .env file"""
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            self.cursor = self.conn.cursor()
            print("Database connection established successfully.")
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            self.conn = None
            self.cursor = None

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Database connection closed.")
