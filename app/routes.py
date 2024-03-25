from flask import render_template, request, redirect, url_for
from app import app
from app.parse import parseQTI
from werkzeug.utils import secure_filename
import os
import random

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

# Function to retrieve questions from the in-memory list
def retrieve_questions_from_memory():
    return questions

# Function to retrieve a quiz by its ID
def get_quiz_by_id(quiz_id):
    for quiz in quizzes:
        if quiz['id'] == quiz_id:
            return quiz
    return None  # Return None if quiz with the given ID is not found

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
    # Retrieve the list of questions to display in the form for editing
    # Here, you would retrieve the list of questions from wherever they are stored
    # and pass them to the template to display them in a vertical list
    return render_template('edit_quiz.html', questions=questions)

# Quiz Bank route: Displays the list of quizzes in the quiz bank page
@app.route('/quiz_bank')
def quiz_bank():
    # Retrieve the list of quizzes from the in-memory list
    return render_template('quiz_bank.html', quizzes=retrieve_quizzes_from_memory())

# New route for the quiz bank page
@app.route('/create_quiz_bank_page')
def create_quiz_bank_page():
    return render_template('quiz_bank.html')

# New route for editing a quiz
@app.route('/edit_quiz/<int:quiz_id>')
def edit_quiz(quiz_id):
    # Retrieve the quiz with the specified ID from the in-memory list
    # You would need to implement this logic to retrieve the quiz data
    # For now, let's assume the quiz data is retrieved and stored in a variable named 'quiz'
    quiz = get_quiz_by_id(quiz_id)

    # Render the "Edit Quiz" page with the quiz data
    return render_template('edit_quiz.html', quiz=quiz)

# Route to display questions vertically
@app.route('/questions_vertical')
def questions_vertical():
    # Retrieve the list of questions from the in-memory list
    return render_template('questions_vertical.html', questions=retrieve_questions_from_memory())

# Route to randomize question order
@app.route('/randomize_question_order', methods=['POST'])
def randomize_question_order():
    # Retrieve the list of questions from the in-memory list
    all_questions = retrieve_questions_from_memory()
    # Shuffle the list of questions
    random.shuffle(all_questions)
    # Update the list of questions in memory (if needed)
    # Optionally, you may want to store the shuffled order permanently
    return redirect(url_for('create_quiz_page'))
