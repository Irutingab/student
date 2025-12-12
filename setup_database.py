import mysql.connector

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "irutingaboRai1@"
}

# Connect without specifying database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS students")
print("Database 'students' created successfully")

# Use the database
cursor.execute("USE students")

# Create students_records table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students_records (
        name VARCHAR(100),
        email VARCHAR(100) PRIMARY KEY,
        phone_number VARCHAR(20),
        mathematics DECIMAL(5,2),
        science DECIMAL(5,2),
        history DECIMAL(5,2),
        english DECIMAL(5,2),
        art DECIMAL(5,2),
        computer_science DECIMAL(5,2)
    )
""")
print("Table 'students_records' created successfully")

# Create report table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS report (
        name VARCHAR(100),
        email VARCHAR(100),
        percentage DECIMAL(5,2),
        class_average DECIMAL(5,2)
    )
""")
print("Table 'report' created successfully")

# Insert sample data for demonstration
sample_students = [
    ('Alice Johnson', 'alice@email.com', '1234567890', 95, 92, 88, 90, 85, 94),
    ('Bob Smith', 'bob@email.com', '1234567891', 88, 85, 90, 87, 82, 89),
    ('Charlie Brown', 'charlie@email.com', '1234567892', 92, 89, 91, 93, 88, 90),
    ('Diana Prince', 'diana@email.com', '1234567893', 85, 88, 84, 86, 90, 87),
    ('Eve Davis', 'eve@email.com', '1234567894', 90, 91, 89, 88, 86, 92),
    ('Frank Miller', 'frank@email.com', '1234567895', 78, 80, 82, 79, 75, 81),
    ('Grace Lee', 'grace@email.com', '1234567896', 94, 93, 95, 92, 91, 96),
    ('Henry Wilson', 'henry@email.com', '1234567897', 82, 84, 81, 83, 80, 85),
    ('Ivy Chen', 'ivy@email.com', '1234567898', 89, 87, 88, 90, 85, 88),
    ('Jack Taylor', 'jack@email.com', '1234567899', 91, 90, 92, 89, 87, 93),
    ('Kelly White', 'kelly@email.com', '1234567800', 87, 89, 86, 88, 84, 90),
    ('Leo Martinez', 'leo@email.com', '1234567801', 93, 94, 92, 95, 90, 94),
]

for student in sample_students:
    try:
        cursor.execute("""
            INSERT INTO students_records 
            (name, email, phone_number, mathematics, science, history, english, art, computer_science)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, student)
    except mysql.connector.IntegrityError:
        print(f"Student {student[0]} already exists, skipping...")

conn.commit()
print(f"Inserted sample data for {len(sample_students)} students")

# Verify data
cursor.execute("SELECT COUNT(*) FROM students_records")
count = cursor.fetchone()[0]
print(f"Total students in database: {count}")

conn.close()
print("\nDatabase setup complete!")
