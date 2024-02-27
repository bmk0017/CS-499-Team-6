
from app.quiz import *
from app.question import *
import logging

import xml.etree.ElementTree as ET


def parseQTI(file):

    allQuestions = Quiz()
    
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
            logging.info(question)
        

    for q in allQuestions.questions:
        logging.info(q)
    
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

    #
    newIDValue = -1
    for child in item.findall(r"./{*}resprocessing/{*}respcondition[@continue='No']/{*}conditionvar"):
        currentID = None

        #Get an ID if there is one
        if (id := child.findall(r'./{*}displayfeedback')) is not None: #If there is feedback tags
                for elem in id: #if the feedback tag isn't 'correct_fb' then get the feedback id
                    if (tag := elem.attrib['linkrefid']) is not 'correct_fb':
                        currentID = tag.removesuffix('_fb')
                        
        #If this has an exact answer store that, otherwise don't
        if (match := child.find(r'./{*}or')) is not None: 
            if currentID is None:
                currentID = str(newIDValue)
                newIDValue -= 1

            question.exact_answers[currentID] = match.find(r'./{*}varequal').text

            question.answer_ranges[currentID] = [match.find(r'./{*}and/{*}vargte').text,match.find(r'./{*}and/{*}varlte').text]
        else:
            if currentID is None:
                currentID = str(newIDValue)
                newIDValue -= 1

            question.exact_answers[currentID] = None

            question.answer_ranges[currentID] = [child.find(r'./{*}vargte').text,child.find(r'./{*}varlte').text]
    
    #Retrieve item feedback
    for child in item.findall(r'./{*}itemfeedback'):
        question.feedback[child.attrib['ident'].removesuffix('_fb')] = child.find(r'./{*}flow_mat/{*}material/{*}mattext').text


    return question

def parseFormula(item):
    question = Formula()

    return #question

def parseEssay(item):
    question = Essay()

    return #question

def parseFileUpload(item):

    return

def parseText(item):

    return