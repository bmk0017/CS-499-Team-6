from app.question import *
from app.quiz import *
import pickle
import os

class Save:
    def __init__(self, file = 'savefile.pickle'):
        self.saveFile = os.getcwd() +'\\'+ file

    def saveQuiz(self, quizInfo):

        with open(self.saveFile, 'ab') as f:
            #Check if it is a quiz so that we can accept single quiz objects and lists
            if isinstance(quizInfo, Quiz):
                quizInfo = [quizInfo]
            
            for q in quizInfo:
                pickle.dump(q, f)

    def loadQuiz(self):
        try:
            with open(self.saveFile, 'rb') as f:
                quizList = []
                while True:
                    try:
                        quiz = pickle.load(f)
                    except EOFError:
                        break
                    quizList.append(quiz)
                f.seek(0)

            return quizList
        except FileNotFoundError:
            return []