
from app.quiz import Quiz
from app.question import *
import logging

import xml.etree.ElementTree as ET


def parseQTI(file):

    questions = [] #Change
    
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
            questions.append(question)
            logging.info(questions)
           
    return questions

#WIP
def parseMultipleChoice(item):
    question = MultipleChoice

    #Retrieve question title
    question.question_title = item['title']

    #Retrieve points possible
    question.points_possible = item.find(r'./{*}itemmetadata/{*}qtimetadata')[1][1].text

    #Retrieve assessment Id
    question.question_id = item['ident']
    
    #Retrieve the question content
    question.question_content = item.find(r'./{*}presentation/{*}material/{*}mattext').text
    
    #Retrieve all choices with corresponding Id
    for child in item.findall(r'./{*}presentation/{*}response_lid/{*}render_choice/{*}response_label'):
        question.choices[child.attrib['ident']] = child.find(r"./{*}material/{*}mattext").text

    #Retrieve Id of correct answer choice
    question.correct_choice = item.find(r"./{*}resprocessing/{*}respcondition[@continue='No']/{*}conditionvar/{*}varequal").text
    
    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.choices_feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text

    #Retrieve the correct feedback
        
    #Retrieve the incorrect feedback
        
    #Retrieve the general feedback

    return question

def parseTrueFalse(item):

    return 

def parseFillintheBlank(item):

    return

def parseFillinMultipleBlanks(item):

    return

def parseMultipleAnswers(item):

    return

def parseMultipleDropdowns(item):

    return

def parseMatching(item):

    return

def parseNumeric(item):

    return

def parseFormula(item):

    return

def parseEssay(item):

    return

def parseFileUpload(item):

    return

def parseText(item):

    return