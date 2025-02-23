
import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

# create programs table
cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS programs (
            program_type TEXT NOT NULL,
            name TEXT NOT NULL,
            PRIMARY KEY (program_type)
        )
    ''')

#  create required_class table
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS required_class (
        class_id TEXT NOT NULL,
        program_name TEXT NOT NULL,
        rec_semester INTEGER,
        PRIMARY KEY (class_id),
        FOREIGN KEY (class_id) REFERENCES class(id) ON DELETE CASCADE
    )
''')

#  create elective_class table
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS elective_class (
        class_id TEXT NOT NULL,
        program_name TEXT NOT NULL,
        rec_semester INTEGER,
        level INTEGER,
        PRIMARY KEY (class_id),
        FOREIGN KEY (class_id) REFERENCES class(id) ON DELETE CASCADE,
        FOREIGN KEY (program_type) REFERENCES programs(program_type) ON DELETE CASCADE
    )
''')

cursor.execute(''' 
    ALTER TABLE elective_class
    ADD description TEXT
''')

# create gen_eds table
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS gen_eds (
        class_id TEXT NOT NULL,
        math_basic INTEGER,
        english_basic INTEGER,
                
        gov INTEGER,
        american_history INTEGER,
                
        writing_intensive INTEGER,
                
        humanities INTEGER,
        fine_arts INTEGER,
                
        bio_sci INTEGER,
        physical_sci INTEGER,
        
        behavioral_sci INTEGER,
        social_sci INTEGER,
        
        PRIMARY KEY (class_id)
        FOREIGN KEY (class_id) REFERENCES class(id) ON DELETE CASCADE
    )
''')

conn.commit()
conn.close()   
print("Database updated successfully!")

