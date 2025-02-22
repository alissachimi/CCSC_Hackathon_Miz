from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static')

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
