import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

programs = [
    ("Major", "Bachelor of Science - Computer Science"),
    ("Major", "Bachelor of Science - Information Technology"),
    ("Major", "Bachelor of Science - Mechanical Engineering")
]

cursor.executemany('''
        INSERT OR IGNORE INTO programs (program_type, name)
        VALUES (?, ?)
    ''', programs)

requirements = [
    ("CMP_SC1050", "Bachelor of Science - Computer Science", 1),
    ("MATH1500", "Bachelor of Science - Computer Science", 1)
    ("CMP_SC2050", "Bachelor of Science - Computer Science", 2),
    ("CMP_SC2270", "Bachelor of Science - Computer Science", 2),
    ("MATH1700", "Bachelor of Science - Computer Science", 2),
    ("CMP_SC3050", "Bachelor of Science - Computer Science", 3),
    ("MATH2300", "Bachelor of Science - Computer Science", 3),
    ("CMP_SC3330", "Bachelor of Science - Computer Science", 4),
    ("CMP_SC3280", "Bachelor of Science - Computer Science", 5),
    ("CMP_SC3380", "Bachelor of Science - Computer Science", 5),
    ("CMP_SC4050", "Bachelor of Science - Computer Science", 6),
    ("CMP_SC4320", "Bachelor of Science - Computer Science", 6),
    ("CMP_SC4520", "Bachelor of Science - Computer Science", 7),
    ("CMP_SC4970W", "Bachelor of Science - Computer Science", 7),
    ("CMP_SC4850", "Bachelor of Science - Computer Science", 8),
    ("CMP_SC4980", "Bachelor of Science - Computer Science", 8)
]

cursor.executemany('''
        INSERT OR IGNORE INTO required_class (class_id, program_type, rec_semester)
        VALUES (?, ?, ?)
    ''', requirements)

conn.commit()
conn.close()
print("Database updated successfully!")