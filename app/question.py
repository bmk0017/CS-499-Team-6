#WIP

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Question:
    points_possible: int
    assessment_question_id: str
    question_content: str
    correct_feedback: str
    incorrect_feedback: str
    general_feedback: str

class MultipleChoice(Question):
    question_type = "multiple_choice_question"
    choices: Dict[int,str]
    correct_choice: int
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>]

class TrueFalse(Question):
    question_type = "true_false_question"
    choices: Dict[int, str]
    correct_choice: int
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>]


class FillintheBlank(Question):
    question_type = "short_answer_question" 
    correct_choices: Dict[int, str]
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>]

class FillinMultipleBlanks(Question):
    question_type = "fill_in_multiple_blanks_question"
    correct_choices: Dict[str, Dict[int, str]]  #Dict[<name of blank>, Dict[<id of choice>, <str of correct choice>]]
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>]

class MultipleAnswers(Question):
    question_type = "multiple_answers_question"
    choices: Dict[int, str]
    correct_choices: List[int]                  
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>] 

class MultipleDropdowns(Question):
    question_type = "multiple_dropdowns_question"
    choices: Dict[str, Dict[int, str]]          #Dict[<name of dropdown>, Dict[<id of choice>, <str of choice]]
    correct_choices: Dict[str, int]             #Dict[<name of dropdown>, <id of correct choice>]
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>]

class Matching(Question):
    question_type = "matching_question"
    left_choices: Dict[int, str]                #Dict[<id of left choice>, <str of left choice>]
    right_choices: Dict[int, str]               #Dict[<id of right choice>, <str of right choice>]
    correct_choices: Dict[int, int]             #Dict[<left choice id>, <right matching choice id]
    incorrect_choices_feedback: Dict[int, str]  #Dict[<id of left choice>, <feedback>]

class Numeric(Question):
    question_type = "numerical_question"
    answer_range: dict #Double Check

class Formula(Question):
    question_type = "calculated_question"
    possible_question_values: dict

class Essay(Question):
    question_type = "essay_question"
    suggested_answer = str

class FileUpload(Question):
    question_type = "text_only_question"
    points_possible = 0

