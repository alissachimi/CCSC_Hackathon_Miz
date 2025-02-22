import sqlite3

def create_db():
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS class (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            dept TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prereqs (
            class_id TEXT NOT NULL,
            prereq_id TEXT NOT NULL,
            PRIMARY KEY (class_id, prereq_id),
            FOREIGN KEY (class_id) REFERENCES class(id) ON DELETE CASCADE,
            FOREIGN KEY (prereq_id) REFERENCES class(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS semester (
            semester_id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS availability (
            class_id TEXT NOT NULL,
            semester_id INTEGER NOT NULL,
            PRIMARY KEY (class_id, semester_id),
            FOREIGN KEY (class_id) REFERENCES class(id) ON DELETE CASCADE,
            FOREIGN KEY (semester_id) REFERENCES semester(semester_id) ON DELETE CASCADE
        )
    ''')

    class_data = [
            ("CS1050", "Intro to Computer Science", "CS", "Dr. Jim Ries"),
            ("CS4520", "Operating Systems", "CS", "Dr. Jim Ries"),
            ("CS3200", "Software Engineering I", "CS", "Dr. Abdelnasser Ouda"),
            ("BIO101", "Intro to Biology", "Biology", "Dr. Johnson")
        ]

    cursor.executemany('''
        INSERT OR IGNORE INTO class (id, name, dept, professor)
        VALUES (?, ?, ?, ?)
    ''', class_data)

    prereqs_data = [
        ("CS4520", "CS1050")  # OS requires CS 1050
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO prereqs (class_id, prereq_id)
        VALUES (?, ?)
    ''', prereqs_data)

    semester_data = [
        ("Fall", 2024),
        ("Spring", 2025),
        ("Summer", 2025)
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO semester (term, year)
        VALUES (?, ?)
    ''', semester_data)

    availability_data = [
        ("CS1050", 1),  # CS1050 available in Fall 2024
        ("CS4520", 2),  # CS4520 available in Spring 2025
        ("CS1050", 3)  # CS1050 available in Summer 2025
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO availability (class_id, semester_id)
        VALUES (?, ?)
    ''', availability_data)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    create_db()