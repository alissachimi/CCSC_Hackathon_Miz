import sqlite3

def read_database(db_path):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        if not tables:
            print("No tables found in the database.")
            return

        # Iterate through each table and read all data
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")

            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            print("Columns:", column_names)

            # Fetch all rows from the table
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Print all rows
            print("Data:")
            for row in rows:
                print(row)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

# Replace 'your_database.db' with the path to your .db file
read_database('college.db')