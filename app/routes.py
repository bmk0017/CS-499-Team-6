# Import necessary modules and classes
from flask import render_template, request, redirect, url_for
from app import app
from app import save
from app.parse import ziptoQuizObj
from app.qti_generator import quiztoQTI
import os

# Specify the upload folder for the XML files
UPLOAD_FOLDER = os.path.join(os.getcwd(),'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route: Displays the main page with the list of quizzes
@app.route('/')
def home():
    quiz = save.loadQuiz()[1]
    quiztoQTI(quiz)

    # Retrieve the list of quizzes from the in-memory list
    return render_template('index.html', quizzes = save.loadQuiz())

# Create Quiz route: Handles quiz creation form submission
@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        # Handle form submission logic
        if 'file' in request.files:
            #file = request.files['file']

            file = request.files.get("file") 
            save.saveQuiz(ziptoQuizObj(file))

        else:
            # Handle the case where no file is uploaded
            # Example: Generate a new quiz with default questions
            new_quiz = {
                'id': len(save.loadQuiz()) + 1,  # Assign a unique ID
                'name': request.form.get('quiz_name'),  # Get the quiz name from the form
                'questions': []  # Add default questions or leave it empty
            }

            # Store the created quiz in the in-memory list
            save.saveQuiz(new_quiz)

        return redirect('/')  # Redirect to create_quiz.html

    return render_template('index.html', quizzes = save.loadQuiz())

# New route for creating a quiz page
@app.route('/create_quiz_page')
def create_quiz_page():
    return render_template('create_quiz.html')

@app.route('/edit_quiz')
def edit_quiz():
    return render_template('edit_quiz.html')

# Quiz Bank route: Displays the list of quizzes in the quiz bank page
@app.route('/quiz_bank')
def quiz_bank():
    # Retrieve the list of quizzes from the in-memory list
    return render_template('quiz_bank.html', quizzes = save.loadQuiz())

# New route for the quiz bank page
@app.route('/create_quiz_bank_page')
def create_quiz_bank_page():
    return render_template('quiz_bank.html')

@app.route('/demo_page/<quizID>')
def demo(quizID = ''):
    
    for q in save.loadQuiz():
        if q.id == quizID:
            currentQuiz = q
    return render_template('demo.html', quiz = str(currentQuiz))

