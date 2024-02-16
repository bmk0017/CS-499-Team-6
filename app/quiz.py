import logging

import xml.etree.ElementTree as ET

class Quiz:
    id: int
    point_possible_total: int


#WIP No worky rn
def parseQTI():
    quizzes = []
    questions = []
    tree = ET.parse('C:\\Users\\matth\\Desktop\\Team 6 Project Extra Files\\team-6-quiz-export\\i618e88580f76f70a1ed28804f497df9c\\i618e88580f76f70a1ed28804f497df9c.xml')
    root = tree.getroot()

    #logging.info(root.iter('item'))
    
    logging.info("start")
    for item in root.findall('item'):
        logging.info("accessed")
        quizzes.append(item)

    logging.info(quizzes)
    

    for question_elem in root.iter('item'):
        logging.info(question_elem.attrib)
        question_dict = {}
        question_dict['ident'] = question_elem.attrib['ident']
        for child_elem in question_elem:
            question_dict[child_elem.tag] = child_elem.text
        questions.append(question_dict)

    logging.info(questions)

