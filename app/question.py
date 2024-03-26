from typing import List, Dict

class Question:
    question_title: str
    points_possible: str
    question_id: str
    question_content: str
    feedback: Dict
    
    def __init__(self):
        self.feedback = {}

class MultipleChoice(Question):
    question_type = "multiple_choice_question"
    choices: Dict[str, str]
    correct_choice: str

    def __init__(self):
        super().__init__()
        self.choices = {}

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type + "\n" 
                + self.question_title + "\n" 
                + self.question_content +"\n" 
                + str(self.choices) 
                + "\nCorrect Choice\n" + self.correct_choice 
                + "\nPoints:\n" + self.points_possible + "\n" 
                + str(self.feedback))

class TrueFalse(Question):
    question_type = "true_false_question"
    choices: Dict[str, str]
    correct_choice: str

    def __init__(self):
        super().__init__()
        self.choices = {}

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\n"+ self.question_content 
                + "\n" + str(self.choices) 
                + "\nCorrect Choice\n" + self.correct_choice 
                + "\nPoints:\n" + self.points_possible
                + "\n" + str(self.feedback))
    

class FillintheBlank(Question):
    question_type = "short_answer_question" 
    correct_choices: Dict[str, str]
    
    def __init__(self):
        super().__init__()
        self.correct_choices = {}

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nCorrect Choices\n" + str(self.correct_choices) 
                + "\nPoints:\n" + self.points_possible 
                + "\n" + str(self.feedback))

class FillinMultipleBlanks(Question):
    question_type = "fill_in_multiple_blanks_question"
    correct_choices: Dict[str, Dict[str, str]]           #Dict[<name of blank>, Dict[<id of choice>, <str of correct choice>]]

    def __init__(self):
        super().__init__()
        self.correct_choices = {}

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nCorrect Choices\n" + str(self.correct_choices) 
                + "\nPoints:\n" + self.points_possible 
                + "\n" + str(self.feedback))

class MultipleAnswers(Question):
    question_type = "multiple_answers_question"
    choices: Dict[str, str]
    correct_choices: List[int]                  

    def __init__(self):
        super().__init__()
        self.choices = {}
        self.correct_choices = []

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nChoices:\n" + str(self.choices)
                + "\nCorrect Choices:\n" + str(self.correct_choices) 
                + "\nPoints:\n" + self.points_possible 
                + "\n" + str(self.feedback))

class MultipleDropdowns(Question):
    question_type = "multiple_dropdowns_question"
    choices: Dict[str, Dict[str, str]]         #Dict[<name of dropdown>, Dict[<id of choice>, <str of choice]] - 
    correct_choices: Dict[str, str]            #Dict[<name of dropdown>, <id of correct choice>] - 

    def __init__(self):
        super().__init__()
        self.choices = {}
        self.correct_choices = {}

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nChoices:\n" + str(self.choices)
                + "\nCorrect Choices:\n" + str(self.correct_choices) 
                + "\nPoints:\n" + self.points_possible 
                + "\n" + str(self.feedback))

class Matching(Question):
    question_type = "matching_question"
    left_choices: Dict[str, str]               #Dict[<id of left choice>, <str of left choice>] - Dict[int, str]
    right_choices: Dict[str, str]               #Dict[<id of right choice>, <str of right choice>] - Dict[int, str]
    correct_choices: Dict[str, str]            #Dict[<left choice id>, <right matching choice id] - Dict[int, int]

    def __init__(self):
        super().__init__()
        self.left_choices = {}
        self.right_choices = {}
        self.correct_choices = {}

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nLeft Choices:\n" + str(self.left_choices)
                + "\nRight Choices:\n" + str(self.right_choices)
                + "\nCorrect Choices:\n" + str(self.correct_choices) 
                + "\nPoints:\n" + self.points_possible 
                + "\n" + str(self.feedback))
        

class Numeric(Question):
    question_type = "numerical_question"
    exact_answers: Dict[str, str]
    answer_ranges: Dict[str, str]

    def __init__(self):
        super().__init__()
        self.exact_answers = {}
        self.answer_ranges = {}

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nExact Answers:\n" + str(self.exact_answers)
                + "\nAnswer Ranges:\n" + str(self.answer_ranges)
                + "\nPoints:\n" + self.points_possible 
                + "\n" + str(self.feedback))
    
class Variable:
    id: str
    variable_name_value: Dict[str, str]
    answers: List

    def __init__(self):
        self.variable_name_value = {}
        self.answers = []

    def __repr__(self):
        return ("\n===="
            + "\nID: " + self.id
            + "\nVariable Name and Value: " + str(self.variable_name_value)
            + "\nAnswers: " + str(self.answers))

class Equation:
    formulas: List
    answer_tolerance: str
    decimal_places: str
    variable_range: Dict[str, Dict[str, str]]
    variable_scale: Dict[str, str]

    def __init__(self):
        self.formulas = []
        self.variable_range = {}
        self.variable_scale = {}

    def __str__(self):
        return (str(self.formulas)
            + "\nAnswer Tolerance: " + self.answer_tolerance
            + "\nDecimal Places: " + self.decimal_places
            + "\nVariable Range: " + str(self.variable_range)
            + "\nVariable Scale: " + str(self.variable_scale))

class Formula(Question):
    question_type = "calculated_question"
    possible_questions: List
    equation: Equation
    chosenID: int
    
    def __init__(self):
        super().__init__()
        self.possible_questions = []
        self.equation = Equation()

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nQuestion:\n" + self.question_content
                + "\nEquation:\n" + str(self.equation)
                + "\nQuestions:\n" + str(self.possible_questions)
                + "\nPoints: " + self.points_possible 
                + "\n" + str(self.feedback))

class Essay(Question):
    question_type = "essay_question"

    def __init__(self):
        super().__init__()

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nQuestion:\n" + str(self.question_content)
                + "\nPoints: " + self.points_possible 
                + "\n" + str(self.feedback))

class FileUpload(Question):
    question_type = "file_upload_question"

    def __init__(self):
        super().__init__()

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nQuestion:\n" + str(self.question_content)
                + "\nPoints: " + self.points_possible 
                + "\n" + str(self.feedback))

class Text(Question):
    question_type = "text_only_question"
    points_possible = 0

    def __init__(self):
        super().__init__()

    def __str__(self):
        return ("\n------------------------\n"
                + self.question_type 
                + "\n" + self.question_title 
                + "\nQuestion:\n" + str(self.question_content)
                + "\nPoints: " + self.points_possible)




