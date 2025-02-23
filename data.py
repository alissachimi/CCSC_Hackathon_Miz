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
    ("MATH1500", "Bachelor of Science - Computer Science", 1),
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
    ("CMP_SC4980", "Bachelor of Science - Computer Science", 8),

    ("ENGINR1000", "Bachelor of Science - Information Technology", 1),
    ("INFOTC1040", "Bachelor of Science - Information Technology", 1),
    ("ENGINR1050", "Bachelor of Science - Information Technology", 2),
    ("INFOTC2040", "Bachelor of Science - Information Technology", 2),
    ("INFOTC1610", "Bachelor of Science - Information Technology", 2),
    ("INFOTC2810", "Bachelor of Science - Information Technology", 3),
    ("INFOTC2830", "Bachelor of Science - Information Technology", 4),
    ("INFOTC2910", "Bachelor of Science - Information Technology", 4),
    ("INFOTC3380", "Bachelor of Science - Information Technology", 5),
    ("INFOTC3530", "Bachelor of Science - Information Technology", 5),
    ("INFOTC3650W", "Bachelor of Science - Information Technology", 5),
    ("INFOTC4320", "Bachelor of Science - Information Technology", 6),
    ("INFOTC4970W", "Bachelor of Science - Information Technology", 8),

    ("CHEM1401", "Bachelor of Science - Mechanical Engineering", 1),
    ("MATH1500", "Bachelor of Science - Mechanical Engineering", 1),
    ("ENGINR1000", "Bachelor of Science - Mechanical Engineering", 1),
    ("PHYSCS2750", "Bachelor of Science - Mechanical Engineering", 2),
    ("MATH1700", "Bachelor of Science - Mechanical Engineering", 2),
    ("ENGINR1050", "Bachelor of Science - Mechanical Engineering", 2),
    ("MAE1100", "Bachelor of Science - Mechanical Engineering", 2),
    ("PHYSCS2760", "Bachelor of Science - Mechanical Engineering", 3),
    ("ENGINR1200", "Bachelor of Science - Mechanical Engineering", 3),
    ("ENGINR2100", "Bachelor of Science - Mechanical Engineering", 3),
    ("MATH2300", "Bachelor of Science - Mechanical Engineering", 3),
    ("MAE2510", "Bachelor of Science - Mechanical Engineering", 3),
    ("MAE2300", "Bachelor of Science - Mechanical Engineering", 3),
    ("STAT4710", "Bachelor of Science - Mechanical Engineering", 4),
    ("MATH4100", "Bachelor of Science - Mechanical Engineering", 4),
    ("ENGINR2200", "Bachelor of Science - Mechanical Engineering", 4),
    ("MAE2100", "Bachelor of Science - Mechanical Engineering", 4),
    ("MAE2600", "Bachelor of Science - Mechanical Engineering", 4),
    ("MAE2200W", "Bachelor of Science - Mechanical Engineering", 5),
    ("MAE3100", "Bachelor of Science - Mechanical Engineering", 5),
    ("MAE3400", "Bachelor of Science - Mechanical Engineering", 5),
    ("MAE3500", "Bachelor of Science - Mechanical Engineering", 5),
    ("MAE3800", "Bachelor of Science - Mechanical Engineering", 5),
    ("MAE3600", "Bachelor of Science - Mechanical Engineering", 6),
    ("MAE3910", "Bachelor of Science - Mechanical Engineering", 6),
    ("MAE4300", "Bachelor of Science - Mechanical Engineering", 6),
    ("MAE4825", "Bachelor of Science - Mechanical Engineering", 6),
    ("MAE4834", "Bachelor of Science - Mechanical Engineering", 7),
    ("ISE2710", "Bachelor of Science - Mechanical Engineering", 7),
    ("MAE4980W", "Bachelor of Science - Mechanical Engineering", 8),
]

cursor.executemany('''
        INSERT OR IGNORE INTO required_class (class_id, program_name, rec_semester)
        VALUES (?, ?, ?)
    ''', requirements)

conn.commit()
conn.close()
print("Database updated successfully!")