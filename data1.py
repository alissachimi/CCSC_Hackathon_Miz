import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("UPDATE elective_class SET availability = ROUND(availability, 2)")

conn.commit()
conn.close()
