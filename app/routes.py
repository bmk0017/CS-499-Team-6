# Import necessary modules and classes
from flask import render_template, request, redirect, url_for
from app import app
from app import save
from app import docGen
from app.parse import ziptoQuizObj
from werkzeug.utils import secure_filename
import os

# Specify the upload folder for the XML files
UPLOAD_FOLDER = os.path.join(os.getcwd(),'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route: Displays the main page with the list of quizzes
@app.route('/')
def home():
    # filepaths = [r'C:\Users\matth\Desktop\Team 6 Project Extra Files\team-6-quiz-export-0.zip', 
    #              r'C:\Users\matth\Desktop\Team 6 Project Extra Files\team-6-quiz-export-1.zip',
    #              r'C:\Users\matth\Desktop\Team 6 Project Extra Files\team-6-quiz-export-2.zip',
    #              r'C:\Users\matth\Desktop\Team 6 Project Extra Files\team-6-quiz-export-3.zip',
    #              r'C:\Users\matth\Desktop\Team 6 Project Extra Files\team-6-quiz-export-4.zip', 
    #              r'C:\Users\matth\Desktop\Team 6 Project Extra Files\robert-k-preston-playground-quiz-export-3-4-24.zip']
    # save.saveQuiz(ziptoQuizObj(filepaths[5]))

    for q in save.loadQuiz():
        print(q)

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

            # if file.filename != '':
            #     # Save the uploaded file to the specified folder
            #     filename = secure_filename(file.filename)
            #     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #     file.save(file_path)

            #     # Now, you can pass the file_path to the parseQTI function
            #     save.saveQuiz(ziptoQuizObj(file_path))
            #     print(ziptoQuizObj(file_path))

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

@app.route('/export/<quizID>')
def export(quizID = ''):

    for q in save.loadQuiz():
        if q.id == quizID:
            docGen.Quiz_to_Doc(q, False)    #Generate Exam
            docGen.Quiz_to_Doc(q, True)     #Generate Exam Key
    
    return redirect('/')
            

