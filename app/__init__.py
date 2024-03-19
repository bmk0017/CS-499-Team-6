from flask import Flask
from app.saveData import Save

app = Flask(__name__)
save = Save('savedQuizzes.pickle')

from app import routes