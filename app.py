from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, static_folder='static')

########## DATABASE LOGIC ##########

app.config["DATABASE"] = "college.db"

def get_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

# Get any prerequisite ids for a given class
def get_prereq_ids(classID):
    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    # Query to get all the prerequisite class IDs for a given class
    cursor.execute('''
        SELECT pr.prereq_id
        FROM prereq pr
        WHERE pr.class_id = ?
    ''', (classID,))

    prereq_classes = cursor.fetchall()
    prereq_class_ids = [row[0] for row in prereq_classes]
    conn.close()
    return prereq_class_ids


# Get all the class details given a list of classIDs
def get_class_details(class_ids):

    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    placeholders = ', '.join('?' for _ in class_ids)
    cursor.execute(f'''
        SELECT class_id, class_name, class_description
        FROM class
        WHERE class_id IN ({placeholders})
    ''', tuple(class_ids))

    class_details = cursor.fetchall()
    conn.close()
    return class_details



######### DATABASE LOGIC END ##########
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/flowchart', methods=['POST'])
def submit():
    major = request.form.get('major')
    if major:
        # add logic here to process the major selection
        return render_template('flowchart.html', major=major)
    return "No major selected."

if __name__ == '__main__':
    app.run(debug=True)
