import sqlite3
import random

def create_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('college_minor.db')
    cursor = conn.cursor()

    # Create MINOR table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MINOR (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            total_hours INTEGER NOT NULL
        )
    ''')

    # Create minor_courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS minor_courses (
            id INTEGER PRIMARY KEY,
            minor_id INTEGER,
            course_id TEXT NOT NULL,
            course_name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            required BOOLEAN NOT NULL,
            FOREIGN KEY (minor_id) REFERENCES MINOR(id)
        )
    ''')

    # Create minor_categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS minor_categories (
            id INTEGER PRIMARY KEY,
            minor_id INTEGER,
            category_name TEXT NOT NULL,
            required_hours INTEGER NOT NULL,
            dept TEXT,
            min_number INTEGER,
            FOREIGN KEY (minor_id) REFERENCES MINOR(id)
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Call the function to create the database and tables
create_db()
