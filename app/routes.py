# Import necessary modules and classes
from flask import render_template, request, redirect, url_for
from app import app
from app.parse import parseQTI
from werkzeug.utils import secure_filename
import os

# Sample data for storing quizzes and questions (using an in-memory list as an example)
quizzes = []
questions = []


# Specify the upload folder for the XML files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to store a quiz in the in-memory list
def store_quiz_in_memory(quiz):
    quizzes.append(quiz)

# Function to retrieve quizzes from the in-memory list
def retrieve_quizzes_from_memory():
    return quizzes

# Home route: Displays the main page with the list of quizzes
@app.route('/')
def home():
    # Retrieve the list of quizzes from the in-memory list
    return render_template('index.html', quizzes=retrieve_quizzes_from_memory())

# Create Quiz route: Handles quiz creation form submission
@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        # Handle form submission logic
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Save the uploaded file to the specified folder
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Now, you can pass the file_path to the parseQTI function
                parseQTI(file_path)

        else:
            # Handle the case where no file is uploaded
            # Example: Generate a new quiz with default questions
            new_quiz = {
                'id': len(quizzes) + 1,  # Assign a unique ID
                'name': request.form.get('quiz_name'),  # Get the quiz name from the form
                'questions': []  # Add default questions or leave it empty
            }

            # Store the created quiz in the in-memory list
            store_quiz_in_memory(new_quiz)

        return redirect(url_for('create_quiz_page'))  # Redirect to create_quiz.html

    return render_template('create_quiz.html')

# New route for creating a quiz page
@app.route('/create_quiz_page')
def create_quiz_page():
    return render_template('create_quiz.html')

# Quiz Bank route: Displays the list of quizzes in the quiz bank page
@app.route('/quiz_bank')
def quiz_bank():
    # Retrieve the list of quizzes from the in-memory list
    return render_template('quiz_bank.html', quizzes=retrieve_quizzes_from_memory())

# New route for the quiz bank page
@app.route('/create_quiz_bank_page')
def create_quiz_bank_page():
    return render_template('quiz_bank.html')
