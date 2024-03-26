import logging
import xml.etree.ElementTree as ET
from typing import List
import random

class Quiz:
    id: str
    title: str
    point_possible_total: int
    description: str
    questions: List
    shuffle_answers: bool

    def __init__(self):
        self.questions = []

    def __str__(self):
        return '\n'.join([str(q) for q in self.questions])

    def prep(self):
        for question in self.questions:
            if question.question_type == "calculated_question":
                qvar = question.possible_questions[random.randint(0, len(question.possible_questions) - 1)]
                question.chosenID = qvar.id
