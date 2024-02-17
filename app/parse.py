
from quiz import Quiz
from question import MultipleChoice




def parseQTI(file):

    quiz = Quiz
    
    tree = ET.parse(open_file)
    root = tree.getroot()

    #logging.info(root.iter('item'))
    
   
    for item in root.findall('item'):
        logging.info("accessed")
        quizzes.append(item)

    

    for question_elem in root.iter('item'):
        logging.info(question_elem.attrib)
        question_dict = {}
        question_dict['ident'] = question_elem.attrib['ident']
        for child_elem in question_elem:
            question_dict[child_elem.tag] = child_elem.text
        questions.append(question_dict)

    logging.info(questions)





    return 

def parseMultipleChoice(item):


    return MultipleChoice