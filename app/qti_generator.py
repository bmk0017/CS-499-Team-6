from app.question import *
from app.quiz import *
import xml.etree.ElementTree as ET

#---------------------------------------WORK IN PROGRESS--------------------------------------------

def quiztoQTI(quiz):
    ...

def createQTI(quiz : Quiz):
    root = ET.Element('questestinterop')

def resprocessing(node, question : Question):

    if question.question_type not in ['matching_question', 'numerical_question']:
        answer_feedback_processing(node, question)

    if question.question_type in ["multiple_choice_question", "true_false_question"]:
        multiple_choice_processing(node, question)
    elif question.question_type is "multiple_answers_question":
        multiple_answer_processing(node, question)
    elif question.question_type is "short_answer_question":
        short_answer_processing(node, question)
    elif question.question_type is "essay_question":
        essay_processing(node, question)
    elif question.question_type is "matching_question":
        matching_processing(node, question)
    elif question.question_type in ["multiple_dropdowns_question", "fill_in_multiple_blanks_question"]:
        multiple_dropdowns_processing(node, question)
    elif question.question_type is "calculated_question":
        calculated_processing(node, question)
    elif question.question_type is "numerical_question":
        numerical_processing(node, question)





def answer_feedback_processing(node, question : Question):
    ...

def multiple_choice_processing(node, question : Question):
    ...

def multiple_answer_processing(node, question : Question):
    ...

def short_answer_processing(node, question : Question):
    ...

def essay_processing(node, question : Question):
    ...

def matching_processing(node, question : Question):
    ...

def multiple_dropdowns_processing(node, question : Question):
    ...

def calculated_processing(node, question : Question):
    ...

def numerical_processing(node, question : Question):
    ...



