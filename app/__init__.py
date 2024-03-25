from flask import Flask
from app.saveData import Save
from app.QuizDocGenerator import QuizDocGenerator

app = Flask(__name__)
save = Save('savedQuizzes.pickle')
docGen = QuizDocGenerator()

from app import routes