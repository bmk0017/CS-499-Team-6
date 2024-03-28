import logging
import xml.etree.ElementTree as ET
from typing import List
import hashlib
import random

class Quiz:
    id: str
    title: str
    point_possible_total: int
    description: str
    questions: List

    def __init__(self):
        self.questions = []
        self.current_id_list = []

    def __str__(self):
        return '\n'.join([str(q) for q in self.questions])
    
    def getHash(self):
        return 'i' + hashlib.md5(str(self).encode()).hexdigest()
    
    def gen_choice_id(self):
        id = random.randint(1, 99999)
        current_ids = self.get_id_list()
        while id in current_ids:
            id = random.randint(1, 99999)
        return id 
        
    def get_id_list(self):
        id_list = []
        for q in self.questions:
            id_list.append(get_original_answer_ids(q))
        return id_list
    
def get_original_answer_ids(question):
    ids = []
    if question.question_type in ["multiple_choice_question", "true_false_question", "multiple_answers_question"]:
        for id in question.choices:
            ids.append(id)
    elif question.question_type == 'short_answer_question':
        for id in question.correct_choices:
            ids.append(id)
    elif question.question_type == 'fill_in_multiple_blanks_question':
        for name in question.correct_choices:
            for id in question.correct_choices[name]:
                ids.append(id)
    elif question.question_type == 'multiple_dropdowns_question':
        for name in question.choices:
            for id in question.choices[name]:
                ids.append(id)
    elif question.question_type == 'matching_question':
        for id in question.left_choices:
            ids.append(id)
    elif question.question_type == 'calculated_question':
        for var in question.possible_questions:
            ids.append(var.id)

    return ids

                
        