#WIP

from typing import List, Dict
from dataclasses import dataclass


class Question:
    question_title: str
    points_possible: str
    question_id: str
    question_content: str
    feedback = {}
    # general_feedback: str

class MultipleChoice(Question):
    question_type = "multiple_choice_question"
    choices = {}
    correct_choice: str
    # choices_feedback = {}            #Dict[<id of choice>, <feedback>] - Dict[str, str]
    # correct_feedback: str
    # incorrect_feedback: str

    def __str__(self):
        return ("------------------------"
                + self.question_type + "\n" 
                + self.question_title + "\n" 
                + self.question_content +"\n" 
                + str(self.choices) 
                + "\nCorrect Choice\n" + self.correct_choice 
                + "\nPoints:\n" + self.points_possible + "\n" 
                + str(self.feedback))

class TrueFalse(Question):
    question_type = "true_false_question"
    choices = {}                     #Dict[int, str]
    correct_choice: str
    # choices_feedback = {}            #Dict[<id of choice>, <feedback>] - Dict[int, str]
    # correct_feedback: str
    # incorrect_feedback: str

    def __str__(self):
        return ("------------------------"
                + self.question_type 
                + "\n" + self.question_title 
                + "\n"+ self.question_content 
                + "\n" + str(self.choices) 
                + "\nCorrect Choice\n" + self.correct_choice 
                + "\nPoints:\n" + self.points_possible
                + "\n" + str(self.feedback))
    

class FillintheBlank(Question):
    question_type = "short_answer_question" 
    correct_choices = {}            #Dict[int, str]
    # choices_feedback = {}           #Dict[<id of choice>, <feedback>] - Dict[int, str]
    # correct_feedback: str
    # incorrect_feedback: str

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nCorrect Choices\n" + str(self.correct_choices) 
                + "\nPoints:\n" + self.points_possible 
                + "\n" + str(self.feedback))

class FillinMultipleBlanks(Question):
    question_type = "fill_in_multiple_blanks_question"
    correct_choices = {}            #Dict[<name of blank>, Dict[<id of choice>, <str of correct choice>]] - Dict[str, Dict[int, str]]
    # choices_feedback = {}           #Dict[<id of choice>, <feedback>] - Dict[int, str]
    # correct_feedback: str
    # incorrect_feedback: str

class MultipleAnswers(Question):
    question_type = "multiple_answers_question"
    choices = {}                    #Dict[int, str]
    correct_choices = []            #List[int]                  
    # choices_feedback = {}           #Dict[<id of choice>, <feedback>] - Dict[int, str]
    # correct_feedback: str
    # incorrect_feedback: str

class MultipleDropdowns(Question):
    question_type = "multiple_dropdowns_question"
    choices = {}                    #Dict[<name of dropdown>, Dict[<id of choice>, <str of choice]] - Dict[str, Dict[int, str]]
    correct_choices = {}            #Dict[<name of dropdown>, <id of correct choice>] - Dict[str, int]
    # choices_feedback = {}           #Dict[<id of choice>, <feedback>] - Dict[int, str]
    # correct_feedback: str
    # incorrect_feedback: str

class Matching(Question):
    question_type = "matching_question"
    left_choices = {}               #Dict[<id of left choice>, <str of left choice>] - Dict[int, str]
    right_choices = {}              #Dict[<id of right choice>, <str of right choice>] - Dict[int, str]
    correct_choices = {}            #Dict[<left choice id>, <right matching choice id] - Dict[int, int]
    # incorrect_choices_feedback = {} #Dict[<id of left choice>, <feedback>] - Dict[int, str]
    # correct_feedback: str
    # incorrect_feedback: str

class Numeric(Question):
    question_type = "numerical_question"

    answer_range: dict #Double Check
    # correct_feedback: str
    # incorrect_feedback: str

class Formula(Question):
    question_type = "calculated_question"
    #possible_question_values: Dict[str, ]
    # correct_feedback: str
    # incorrect_feedback: str

class Essay(Question):
    question_type = "essay_question"

class FileUpload(Question):
    question_type = "file_upload_question"

class Text(Question):
    question_type = "text_only_question"
    points_possible = 0

class Variable:
    variable_name: str
    min_value: str
    max_value: str
    value_with_answers: Dict[int, Dict[str, str]]         #Dict[<id>, Dict[value, answer]]  