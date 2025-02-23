from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd


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

def get_db_connection():
    """Connect to the database."""
    conn = sqlite3.connect('college_minor.db')  # Replace with your database file
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def fetch_courses_for_category(category_id):
    """Fetch all courses for a specific category."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * 
        FROM minor_courses
        WHERE category_id = ?
        """,
        (category_id,)
    )
    courses = cursor.fetchall()
    conn.close()
    return courses

def get_minors():
    """Fetch all minors from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM minor")
    minors = [dict(row) for row in cursor.fetchall()]  # Convert rows to dictionaries

    conn.close()
    return minors

def fetch_categories_for_minor(minor_id):
    """Fetch all categories for a specific minor."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM minor_categories WHERE minor_id = ?", (minor_id,))
    categories = [dict(row) for row in cursor.fetchall()]  # Convert rows to dictionaries

    conn.close()
    return categories

def fetch_courses_for_category(category_id):
    """Fetch all courses for a specific category."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM minor_courses WHERE category_id = ?", (category_id,))
    courses = [dict(row) for row in cursor.fetchall()]  # Convert rows to dictionaries

    conn.close()
    return courses

def get_electives_from_db(major):
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()
    query = '''
        SELECT 
            e.class_id, 
            c.name, 
            e.description, 
            e.availability, 
            IFNULL(GROUP_CONCAT(p.prereq_id, ', '), 'None') AS prereq
        FROM elective_class e
        JOIN class c ON c.id = e.class_id
        LEFT JOIN prereqs p ON e.class_id = p.class_id
    '''
    if major:
        query += " WHERE e.program_name = ?"
        params = (major,)

    cursor.execute(query, params)
    electives_list = cursor.fetchall()
    conn.close()

    electives = [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "availability": row[3],
            "minor": 'Yes',
            "prereq": row[4],
            "required": False
        }
        for row in electives_list
    ]
    return electives

######### DATABASE LOGIC END ##########

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/flowchart', methods=['POST'])
def flowchart():
    major = request.form.get('major')
    if major:
        classes = get_degree_requirements(major)
        
        # add logic here to process the major selection
        return render_template('flowchart.html', major=major, classes=classes)
    return "No major selected."

@app.route("/get_electives", methods=["GET"])
def get_electives():
    major = request.args.get("major", "")
    electives = get_electives_from_db(major)
    return jsonify(electives)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_remaining_hours(progress):
    """Calculates the remaining hours for a minor progress dictionary."""
    return progress["total_required_hours"] - progress["completed_hours"]

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

        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file)

            # Ensure the DataFrame has exactly two columns
            if len(df.columns) != 2:
                return jsonify({"error": "The Excel file must have exactly two columns: Course ID and Units."}), 400

            # Convert the DataFrame to a dictionary
            taken_courses = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

            # Fetch all minors
            minors = get_minors()

            # Calculate progress for all minors
            all_progress = []
            for minor in minors:
                minor_cat=fetch_categories_for_minor(minor["id"])
                progress = calculate_minor_progress(minor["id"], minor["name"], minor_cat, taken_courses)
                all_progress.append(progress)

            # Sort all_progress based on remaining hours
            all_progress.sort(key=calculate_remaining_hours)

            # Render the progress data in the template
            return render_template('minor_recomendation.html', all_progress=all_progress)

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
             
# Function to calculate progress for a minor
def normalize_course_id(course_id):
    """
    Normalize a course ID by:
    1. Replacing underscores with spaces.
    2. Removing underscores entirely.
    """
    # Replace underscores with spaces
    with_spaces = course_id.replace("_", " ")
    # Remove underscores entirely
    without_underscores = course_id.replace("_", "")
    return {course_id, with_spaces, without_underscores}

def calculate_minor_progress(minor_id, minor_name, minor_categories, taken_courses):
    progress = {
        "minor_id": minor_id,
        "minor_name": minor_name,
        "total_required_hours": 0,
        "completed_hours": 0,
        "categories": [],
    }

    categories = [cat for cat in minor_categories if cat["minor_id"] == minor_id]

    # ensure same course isn't double counted for different categories
    counted_courses = set()

    for category in categories:
        category_id = category["id"]
        required_hours = category["required_hours"]
        dept = category["dept"]
        min_number = category["min_number"]
        category_name = category["category_name"]

        if category_name == "GREATER_THAN":
            category_name = "Elective Courses"

        category_progress = {
            "category_id": category_id,
            "category_name": category_name,
            "required_hours": required_hours,
            "completed_hours": 0,
            "required_courses": [],
            "choice_courses": [],
            "general_requirement": None,
        }

        if dept and min_number:
            category_progress["general_requirement"] = f"{dept} {min_number}+"
            
            for course_code, credits in taken_courses.items():
                if course_code.startswith(dept):
                    course_number = int(''.join(filter(str.isdigit, course_code)))
                    if course_number >= min_number and course_code not in counted_courses:
                        category_progress["completed_hours"] += credits
                        category_progress["required_courses"].append({
                            "course_name": course_code,
                            "credits": credits,
                        })
                        
        else:
            courses = fetch_courses_for_category(category_id)
            for course in courses:
                if course["course_id"] in taken_courses:
                    category_progress["completed_hours"] += taken_courses[course["course_id"]]
                    if course["required"]:
                        category_progress["required_courses"].append({
                            "course_name": course["course_id"],
                            "credits": taken_courses[course["course_id"]],
                        })
                    else:
                        category_progress["choice_courses"].append({
                            "course_name": course["course_id"],
                            "credits": taken_courses[course["course_id"]],
                        })
                    counted_courses.add(course["course_id"])
                else:
                    category_progress["choice_courses"].append({
                        "course_name": course["course_id"],
                        "credits": course["credits"],
                    })

        category_progress["completed_hours"] = min(category_progress["completed_hours"], required_hours)
        progress["total_required_hours"] += required_hours
        progress["completed_hours"] += category_progress["completed_hours"]
        progress["categories"].append(category_progress)

    return progress

# send required classes for the user's selected major to flowchart.html
def get_degree_requirements(major):
    degree_name = "Bachelor of Science - " + major
    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT *
        FROM required_class
        WHERE program_name = ?
        ORDER BY rec_semester ASC
    ''', (degree_name,))

    required_classes = cursor.fetchall()
    conn.close()
    return required_classes

if __name__ == '__main__':
    app.run(debug=True)