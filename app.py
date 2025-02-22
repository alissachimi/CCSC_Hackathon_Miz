from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import os

# Sample data for minors
minors = [
    {
        "id": 1,
        "name": "Computer Science",
    },
    {
        "id": 2,
        "name": "Mathematics",
    },
    {
        "id": 3,
        "name": "Psychology",
    },
]

# Sample data for minor_category
minor_categories = [
    # Computer Science categories
    {
        "id": 1,
        "minor_id": 1,
        "category_name": "Required Courses",
        "required_hours": 6,
        "dept": None,
        "min_number": None,
    },
    {
        "id": 2,
        "minor_id": 1,
        "category_name": "Electives (Pick 2)",
        "required_hours": 6,
        "dept": None,
        "min_number": None,
    },

    # Mathematics categories
    {
        "id": 3,
        "minor_id": 2,
        "category_name": "GREATER_THAN",
        "required_hours": 6,
        "dept": "MATH",
        "min_number": 3000,
    },

    # Psychology categories
    {
        "id": 4,
        "minor_id": 3,
        "category_name": "Required Courses",
        "required_hours": 6,
        "dept": None,
        "min_number": None,
    },
    {
        "id": 5,
        "minor_id": 3,
        "category_name": "Electives (Pick 2)",
        "required_hours": 6,
        "dept": None,
        "min_number": None,
    },
]

# Sample data for minor_courses
minor_courses = [
    # Computer Science courses
    {"id": 1, "minor_category_id": 1, "course_id": "CS1050", "course_name": "Algorithm Design and Programming I", "credits": 3, "is_required": True},
    {"id": 2, "minor_category_id": 1, "course_id": "CS2050", "course_name": "Algorithm Design and Programming II", "credits": 3, "is_required": True},
    {"id": 3, "minor_category_id": 2, "course_id": "CS2830", "course_name": "Network Fundamentals", "credits": 3, "is_required": False},
    {"id": 4, "minor_category_id": 2, "course_id": "CS3330", "course_name": "Object-Oriented Programming", "credits": 3, "is_required": False},
    {"id": 5, "minor_category_id": 2, "course_id": "CS3380", "course_name": "Database Applications", "credits": 3, "is_required": False},

    # Mathematics courses
    {"id": 6, "minor_category_id": 3, "course_id": "MATH3000", "course_name": "Advanced Calculus", "credits": 3, "is_required": False},
    {"id": 7, "minor_category_id": 3, "course_id": "MATH4100", "course_name": "Linear Algebra", "credits": 3, "is_required": False},
    {"id": 8, "minor_category_id": 3, "course_id": "MATH4200", "course_name": "Differential Equations", "credits": 3, "is_required": False},

    # Psychology courses
    {"id": 9, "minor_category_id": 4, "course_id": "PSYCH1000", "course_name": "General Psychology", "credits": 3, "is_required": True},
    {"id": 10, "minor_category_id": 4, "course_id": "PSYCH2410", "course_name": "Research Methods in Psychology", "credits": 3, "is_required": True},
    {"id": 11, "minor_category_id": 5, "course_id": "PSYCH2210", "course_name": "Developmental Psychology", "credits": 3, "is_required": False},
    {"id": 12, "minor_category_id": 5, "course_id": "PSYCH3310", "course_name": "Abnormal Psychology", "credits": 3, "is_required": False},
    {"id": 13, "minor_category_id": 5, "course_id": "PSYCH4320", "course_name": "Cognitive Psychology", "credits": 3, "is_required": False},
]

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
        return render_template('minor_recomendation.html', all_progress=None)

    if request.method == 'POST':
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

            # Calculate progress for all minors
            all_progress = []
            for minor in minors:
                progress = calculate_minor_progress(minor["id"], minor_categories, minor_courses, course_dict)
                progress["minor_name"] = minor["name"]
                all_progress.append(progress)

            # Render the progress data in the template
            return render_template('minor_recomendation.html', all_progress=all_progress)

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
# Function to calculate progress for a minor
def calculate_minor_progress(minor_id, minor_categories, minor_courses, taken_courses):
    progress = {
        "minor_id": minor_id,
        "total_required_hours": 0,
        "completed_hours": 0,
        "categories": [],
    }

    # Get all categories for the minor
    categories = [cat for cat in minor_categories if cat["minor_id"] == minor_id]

    for category in categories:
        category_id = category["id"]
        required_hours = category["required_hours"]
        dept = category["dept"]
        min_number = category["min_number"]

        # Initialize completed hours for this category
        category_completed_hours = 0

        # Get all courses for the category
        courses = [course for course in minor_courses if course["minor_category_id"] == category_id]

        # Check if the category is a general requirement (e.g., "GREATER_THAN")
        if dept and min_number:
            # Filter taken courses that match the department and minimum number
            for course_code, credits in taken_courses.items():
                if course_code.startswith(dept):
                    course_number = int(''.join(filter(str.isdigit, course_code)))
                    if course_number >= min_number:
                        category_completed_hours += credits
        else:
            # Specific course requirements
            for course in courses:
                if course["course_id"] in taken_courses:
                    category_completed_hours += taken_courses[course["course_id"]]

        # Cap completed hours at the required hours
        category_completed_hours = min(category_completed_hours, required_hours)

        # Update progress
        progress["total_required_hours"] += required_hours
        progress["completed_hours"] += category_completed_hours
        progress["categories"].append({
            "category_id": category_id,
            "category_name": category["category_name"],
            "required_hours": required_hours,
            "completed_hours": category_completed_hours,
        })

    return progress


if __name__ == '__main__':
    app.run(debug=True)