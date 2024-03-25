
from app.quiz import *
from app.question import *
import tempfile
import logging
import zipfile
import os

import xml.etree.ElementTree as ET


def ziptoQuizObj(filePath):
    with tempfile.TemporaryDirectory() as td:
        try:
            with zipfile.ZipFile(filePath) as archive:
                archive.extractall(td)
        except zipfile.BadZipFile as error:
            print(error)

        quizList = []
        for root, dirs, file in os.walk(td):
            for f in file:
                if f not in ['assessment_meta.xml', 'imsmanifest.xml']:
                    quiz = parseQuiz(os.path.join(root, "assessment_meta.xml"))
                    quizList.append(parseQTI(os.path.join(root, f), quiz))
                    
    return quizList

def parseQuiz(file):
    baseQuiz = Quiz()

    tree = ET.parse(file)
    root = tree.getroot()

    baseQuiz.title = root.find(r'./{*}title').text
    baseQuiz.description = root.find(r'./{*}description').text
    baseQuiz.id = root.attrib['identifier']
    baseQuiz.description = root.find(r'./{*}points_possible').text
    if root.find(r'./{*}shuffle_answers').text == 'true':
        baseQuiz.shuffle_answers = True
    else:
        baseQuiz.shuffle_answers = False

    return baseQuiz
        

def parseQTI(file, quiz:Quiz):

    allQuestions = quiz
    
    tree = ET.parse(file)
    root = tree.getroot()
    
    for question_elem in root.findall(r'./{*}assessment/{*}section/{*}item'):
        for child in question_elem.iter(r'{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}qtimetadatafield'):
            if child.find(r'{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldlabel').text == 'question_type':
                question_type = child.find(r'{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldentry').text
        if question_type == MultipleChoice.question_type:
            question = parseMultipleChoice(question_elem)
        elif question_type == TrueFalse.question_type:
            question = parseTrueFalse(question_elem)
        elif question_type == FillintheBlank.question_type:
            question = parseFillintheBlank(question_elem)
        elif question_type == FillinMultipleBlanks.question_type:
            question = parseFillinMultipleBlanks(question_elem)
        elif question_type == MultipleAnswers.question_type:
            question = parseMultipleAnswers(question_elem)
        elif question_type == MultipleDropdowns.question_type:
            question = parseMultipleDropdowns(question_elem)
        elif question_type == Matching.question_type:
            question = parseMatching(question_elem)
        elif question_type == Numeric.question_type:
            question = parseNumeric(question_elem)
        elif question_type == Formula.question_type:
            question = parseFormula(question_elem)
        elif question_type == Essay.question_type:
            question = parseEssay(question_elem)
        elif question_type == FileUpload.question_type:
            question = parseFileUpload(question_elem)
        elif question_type == Text.question_type:
            question = parseText(question_elem) 

        if type(question)!=type(None): #This IF may not be neccessary later on
            allQuestions.questions.append(question)
    
    return allQuestions

#WIP
def parseMultipleChoice(item):
    question = MultipleChoice()

    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text
    
    #Retrieve all choices with corresponding Id
    for child in item.findall(r'./{*}presentation/{*}response_lid/{*}render_choice/{*}response_label'):
        question.choices[child.attrib['ident']] = child.find(r"./{*}material/{*}mattext").text

    #Retrieve Id of correct answer choice
    question.correct_choice = item.find(r"./{*}resprocessing/{*}respcondition[@continue='No']/{*}conditionvar/{*}varequal").text
    
    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

    return question

def parseTrueFalse(item):
    question = TrueFalse()

    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text

    #Retrieve all choices with corresponding Id
    for child in item.findall(r'./{*}presentation/{*}response_lid/{*}render_choice/{*}response_label'):
        question.choices[child.attrib['ident']] = child.find(r"./{*}material/{*}mattext").text

    #Retrieve Id of correct answer choice
    question.correct_choice = item.find(r"./{*}resprocessing/{*}respcondition[@continue='No']/{*}conditionvar/{*}varequal").text
    
    #Retrieve feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text


    return question

def parseFillintheBlank(item):
    question = FillintheBlank()

    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text

    #Retrieve Id of correct answer choices
    for child in item.findall(r"./{*}resprocessing/{*}respcondition[@continue='Yes']"):
        if (match := child.find(r"./{*}conditionvar/{*}varequal[@respident='response1']")) is not None:
            question.correct_choices[child.find(r'./{*}displayfeedback').attrib['linkrefid'].removesuffix('_fb')] = match.text

    newIDValue = -1
    checkChoices = item.find(r"./{*}resprocessing/{*}respcondition[@continue='No']/{*}conditionvar")
    for child in checkChoices.findall(r"./{*}varequal[@respident='response1']"):
        if child.text not in question.correct_choices.values():
            question.correct_choices[str(newIDValue)] = child.text
            newIDValue -= 1
    
    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

    return question

def parseFillinMultipleBlanks(item):
    question = FillinMultipleBlanks()

    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text

    #Retrieve Id of correct answer choices
    for child in item.findall(r"./{*}presentation/{*}response_lid"):
        blank = child.find(r"./{*}material/{*}mattext").text
        current_blank_choices = {}
        for elem in child.findall(r"./{*}render_choice/{*}response_label"):
            current_blank_choices[elem.attrib['ident']] = elem.find(r"./{*}material/{*}mattext").text
        question.correct_choices[blank] = current_blank_choices
    
    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

    return question

def parseMultipleAnswers(item):
    question = MultipleAnswers()

    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text

    #Retrieve answer choices
    for child in item.findall(r'./{*}presentation/{*}response_lid/{*}render_choice/{*}response_label'):
        question.choices[child.attrib['ident']] = child.find(r"./{*}material/{*}mattext").text

    #Retrieve Id of correct answer choice
    for child in item.findall(r"./{*}resprocessing/{*}respcondition[@continue='No']/{*}conditionvar/{*}and/{*}varequal"):
        question.correct_choices.append(child.text)
    
    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

    return question

def parseMultipleDropdowns(item):
    question = MultipleDropdowns()

    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text


    #Retrieve answer choices
    response_blank_id = {} 
    for child in item.findall(r"./{*}presentation/{*}response_lid"):
        blank = child.find(r"./{*}material/{*}mattext").text
        response_blank_id[child.attrib['ident']] = blank
        current_blank_choices = {}
        for elem in child.findall(r"./{*}render_choice/{*}response_label"):
            current_blank_choices[elem.attrib['ident']] = elem.find(r"./{*}material/{*}mattext").text
        question.choices[blank] = current_blank_choices

    #Retrieve Id of correct answer choice
    for child in item.findall(r"./{*}resprocessing/{*}respcondition/{*}conditionvar/{*}varequal"):
        question.correct_choices[response_blank_id[child.attrib['respident']]] = child.text
        
    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

    return question

def parseMatching(item):
    question = Matching()

    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text

    #Retrieve Id of left choices and right choices
    first = True
    for child in item.findall(r"./{*}presentation/{*}response_lid"):
        if first:
            for elem in child.findall(r'./{*}render_choice/{*}response_label'):
                question.right_choices[elem.attrib['ident']] = elem.find(r'./{*}material/{*}mattext').text
            first = False
        question.left_choices[child.attrib['ident'].removeprefix("response_")] = child.find(r'./{*}material/{*}mattext').text

    #Retrieve the correct left to right choices
    for child in item.findall(r"./{*}resprocessing/{*}respcondition/{*}conditionvar/{*}varequal"):
        question.correct_choices[child.attrib['respident'].removeprefix('response_')] = child.text

    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

    return question

def parseNumeric(item):
    question = Numeric()

    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text

    #Retrieve Exact answer if there is one, and the answer range
    newIDValue = -1
    for child in item.findall(r"./{*}resprocessing/{*}respcondition[@continue='No']/{*}conditionvar"):
        currentID = None

        #Get an ID if there is one
        if (id := child.findall(r'./{*}displayfeedback')) is not None: #If there is feedback tags
            for elem in id: #if the feedback tag isn't 'correct_fb' then get the feedback id
                if (tag := elem.attrib['linkrefid']) != 'correct_fb':
                    currentID = tag.removesuffix('_fb')
                        
        #If this has an exact answer store that, otherwise don't
        if (match := child.find(r'./{*}or')) is not None: 
            if currentID is None:
                currentID = str(newIDValue)
                newIDValue -= 1

            question.exact_answers[currentID] = match.find(r'./{*}varequal').text

            #Differentiate between GTE and GT, aswell as LTE and LT
            greater = 0
            lesser = 0
            if (gt := match.find(r'./{*}and/{*}vargte')) is not None:
                greater = gt.text
            else:
                greater = match.find(r'./{*}and/{*}vargt').text

            if (lt := match.find(r'./{*}and/{*}varlte')) is not None:
                lesser = lt.text
            else:
                lesser = match.find(r'./{*}and/{*}varlt').text

            question.answer_ranges[currentID] = [greater,lesser]
        else:
            #Does the element require a new ID
            if currentID is None:
                currentID = str(newIDValue)
                newIDValue -= 1

            question.exact_answers[currentID] = None

            #Differentiate between GTE and GT, aswell as LTE and LT
            greater = 0
            lesser = 0
            if (gt := child.find(r'./{*}vargte')) is not None:
                greater = gt.text
            else:
                greater = child.find(r'./{*}vargt').text

            if (lt := child.find(r'./{*}varlte')) is not None:
                lesser = lt.text
            else:
                lesser = child.find(r'./{*}varlt').text

            question.answer_ranges[currentID] = [greater,lesser]
    
    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

    return question

def parseFormula(item):
    question = Formula()

     #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text

    #Retrieve Equation/Formula Information
    question.equation.answer_tolerance = item.find(r'./{*}itemproc_extension/{*}calculated/{*}answer_tolerance').text
    question.equation.decimal_places = item.find(r'./{*}itemproc_extension/{*}calculated/{*}formulas').attrib['decimal_places']
    for child in item.findall(r'./{*}itemproc_extension/{*}calculated/{*}formulas/{*}formula'):
        question.equation.formulas.append(child.text)

    for child in item.findall(r'./{*}itemproc_extension/{*}calculated/{*}vars/{*}var'):
        range = {}
        range[child.find(r'./{*}min').text] = child.find(r'./{*}max').text
        question.equation.variable_range[child.attrib['name']] = range
        question.equation.variable_scale[child.attrib['name']] = child.attrib['scale']

    #Retrieve Variable value and answers
    for child in item.findall(r'./{*}itemproc_extension/{*}calculated/{*}var_sets/{*}var_set'):
        var = Variable()
        var.id = child.attrib['ident']
        for elem in child.findall(r'./{*}var'):
            var.variable_name_value[elem.attrib['name']] = elem.text
        
        for elem in child.findall(r'./{*}answer'):
            var.answers.append(elem.text)
        question.possible_questions.append(var)

    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

        
    return question

def parseEssay(item):
    question = Essay()

    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text
        
    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

    return question

def parseFileUpload(item):
    question = FileUpload()

    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text
        
    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

    return question

def parseText(item):
    question = Text()
    
    #Retrieve question title
    question.question_title = item.attrib['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item.attrib['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text
        
    return question