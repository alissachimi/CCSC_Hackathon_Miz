from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import os


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
def flowchart():
    major = request.form.get('major')
    if major:
        # add logic here to process the major selection
        return render_template('flowchart.html', major=major)
    return "No major selected."

# Allowed file extensions
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/minor_recomendation', methods=['POST', 'GET'])
def minor_recomendation():
    if request.method == 'GET':
        return render_template('minor_recomendation.html')
    if request.method=='POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Check if the file has an allowed extension
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only .xlsx and .xls files are allowed."}), 400

        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file)

            # Ensure the DataFrame has exactly two columns
            if len(df.columns) != 2:
                return jsonify({"error": "The Excel file must have exactly two columns: Course ID and Units."}), 400

            # Convert the DataFrame to a dictionary
            course_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

            return jsonify({"message": "File processed successfully", "data": course_dict}), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
