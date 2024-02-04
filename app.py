from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data for storing quizzes and questions
quizzes = []
questions = []

# Home route: Displays the main page with the list of quizzes
@app.route('/')
def home():
    return render_template('index.html', quizzes=quizzes)

# Create Quiz route: Handles quiz creation form submission
@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        quiz_title = request.form['quiz_title']
        quiz_questions = []
        for i in range(1, 6):  # Assuming 5 questions for simplicity
            question_text = request.form.get(f'question_{i}_text')
            if question_text:
                options = [
                    request.form.get(f'question_{i}_option_{j}')
                    for j in range(1, 5)  # Assuming 4 options per question
                ]
                correct_option = request.form.get(f'question_{i}_correct_option')

                question_data = {
                    'text': question_text,
                    'options': options,
                    'correct_option': correct_option
                }
                questions.append(question_data)
                quiz_questions.append(len(questions) - 1)  # Store the index of the question

        quizzes.append({'title': quiz_title, 'questions': quiz_questions})

        return redirect(url_for('home'))

    return render_template('create_quiz.html')

# Question Bank route: Placeholder for the question bank page
@app.route('/question_bank')
def question_bank():
    # Placeholder for the question bank page
    return "Question Bank Page"

# Quiz Bank route: Displays the list of quizzes in the quiz bank page
@app.route('/quiz_bank')
def quiz_bank():
    return render_template('quiz_bank.html', quizzes=quizzes)

if __name__ == '__main__':
    app.run(debug=True)
