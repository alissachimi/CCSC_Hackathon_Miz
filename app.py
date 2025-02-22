from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, static_folder='static')

########## DATABASE LOGIC ##########

app.config["DATABASE"] = "college.db"

def get_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def get_prerequisites(classID):
    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT pr.prereq_id
        FROM prereq pr
        WHERE pr.class_id = ?
    ''', (classID,))

    # Fetch all the results
    results = cursor.fetchall()
    conn.close()

    # Extract the classIDs from the query result
    prereq_classes = [row[0] for row in results]
    return prereq_classes


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
