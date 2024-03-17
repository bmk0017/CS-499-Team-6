from app.question import *
from app.quiz import *
from app.parse import ziptoQuizObj
import pickle

def saveQuiz(quizInfo):

    with open('savefile', 'w') as f:
        pickle.dump(quizInfo, f)

def loadQuiz():

    with open('savefile') as f:
        quizInfo = pickle.load(f)

    return quizInfo