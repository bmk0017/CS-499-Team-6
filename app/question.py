#WIP

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Question:
    question_title: str
    points_possible: int
    assessment_question_id: str
    question_content: str
    general_feedback: str

@dataclass
class MultipleChoice(Question):
    question_type = "multiple_choice_question"
    choices: Dict[int,str]
    correct_choice: int
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>]
    correct_feedback: str
    incorrect_feedback: str

@dataclass
class TrueFalse(Question):
    question_type = "true_false_question"
    choices: Dict[int, str]
    correct_choice: int
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>]
    correct_feedback: str
    incorrect_feedback: str

@dataclass
class FillintheBlank(Question):
    question_type = "short_answer_question" 
    correct_choices: Dict[int, str]
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>]
    correct_feedback: str
    incorrect_feedback: str

@dataclass
class FillinMultipleBlanks(Question):
    question_type = "fill_in_multiple_blanks_question"
    correct_choices: Dict[str, Dict[int, str]]  #Dict[<name of blank>, Dict[<id of choice>, <str of correct choice>]]
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>]
    correct_feedback: str
    incorrect_feedback: str

@dataclass
class MultipleAnswers(Question):
    question_type = "multiple_answers_question"
    choices: Dict[int, str]
    correct_choices: List[int]                  
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>] 
    correct_feedback: str
    incorrect_feedback: str

@dataclass
class MultipleDropdowns(Question):
    question_type = "multiple_dropdowns_question"
    choices: Dict[str, Dict[int, str]]          #Dict[<name of dropdown>, Dict[<id of choice>, <str of choice]]
    correct_choices: Dict[str, int]             #Dict[<name of dropdown>, <id of correct choice>]
    choices_feedback: Dict[int, str]            #Dict[<id of choice>, <feedback>]
    correct_feedback: str
    incorrect_feedback: str

@dataclass
class Matching(Question):
    question_type = "matching_question"
    left_choices: Dict[int, str]                #Dict[<id of left choice>, <str of left choice>]
    right_choices: Dict[int, str]               #Dict[<id of right choice>, <str of right choice>]
    correct_choices: Dict[int, int]             #Dict[<left choice id>, <right matching choice id]
    incorrect_choices_feedback: Dict[int, str]  #Dict[<id of left choice>, <feedback>]
    correct_feedback: str
    incorrect_feedback: str

@dataclass
class Numeric(Question):
    question_type = "numerical_question"

    answer_range: dict #Double Check
    correct_feedback: str
    incorrect_feedback: str

@dataclass
class Formula(Question):
    question_type = "calculated_question"
    possible_question_values: Dict[str, ]
    correct_feedback: str
    incorrect_feedback: str

@dataclass
class Essay(Question):
    question_type = "essay_question"

@dataclass
class FileUpload(Question):
    question_type = "file_upload_question"

@dataclass
class Text(Question):
    question_type = "text_only_question"
    points_possible = 0

@dataclass
class Variable:
    variable_name: str
    min_value: str
    max_value: str
    value_with_answers: Dict[int, Dict[str, str]]         #Dict[<id>, Dict[value, answer]]  


