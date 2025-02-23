import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute('''
    UPDATE elective_class
    SET availability = (
        SELECT class.fall
        FROM class
        WHERE class.id = elective_class.class_id
    )
    WHERE EXISTS (
        SELECT 1
        FROM class
        WHERE class.id = elective_class.class_id
    )
''')

# Another query to set availability to 0.50 where it is -1
cursor.execute('''
    UPDATE elective_class 
    SET availability = 0.50
    WHERE availability = -1
''')

conn.commit()
conn.close()
