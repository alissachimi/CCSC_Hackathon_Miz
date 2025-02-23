import sqlite3

def insert_statistics_minor():
    # Connect to SQLite database
    conn = sqlite3.connect('college_minor.db')
    cursor = conn.cursor()

    # Insert the Minor in Statistics into the MINOR table
    cursor.execute("INSERT INTO MINOR (name, total_hours) VALUES (?, ?)", ('Statistics', 15))
    
    # Get the ID of the inserted Statistics Minor
    cursor.execute("SELECT id FROM MINOR WHERE name = ?", ('Statistics',))
    minor_id = cursor.fetchone()[0]

    # Insert categories for the Statistics Minor
    cursor.execute(""" 
        INSERT INTO minor_categories (minor_id, category_name, required_hours, dept, min_number) 
        VALUES (?, ?, ?, ?, ?)
    """, (minor_id, 'Required Courses', 9, 'STAT', None))

    cursor.execute(""" 
        INSERT INTO minor_categories (minor_id, category_name, required_hours, dept, min_number) 
        VALUES (?, ?, ?, ?, ?)
    """, (minor_id, 'GREATER_THAN', 6, 'STAT', 3000))

    # Get category ID for 'Required Courses'
    cursor.execute(""" 
        SELECT id FROM minor_categories WHERE category_name = ? AND minor_id = ? 
    """, ('Required Courses', minor_id))
    required_category_id = cursor.fetchone()[0]

    # Insert required courses
    required_courses = [
        ('STAT 3500', 'Introduction to Probability and Statistics II', 3, 1),
        ('STAT 4710', 'Introduction to Mathematical Statistics', 3, 1),
        ('STAT 4750', 'Introduction to Probability Theory', 3, 1)
    ]

    for course_id, course_name, credits, required in required_courses:
        cursor.execute(""" 
            INSERT INTO minor_courses (minor_id, course_id, category_id, course_name, credits, required) 
            VALUES (?, ?, ?, ?, ?, ?) 
        """, (minor_id, course_id, required_category_id, course_name, credits, required))

    # Commit and close connection
    conn.commit()
    conn.close()

# Run the function to insert the Minor in Statistics
insert_statistics_minor()
