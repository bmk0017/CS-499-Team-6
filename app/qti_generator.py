from app.question import *
from app.quiz import *
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import re
import tempfile
import zipfile
import os

#---------------------------------------WORK IN PROGRESS--------------------------------------------

def quiztoQTI(quiz):
    createQTI(quiz).write('temp/' + quiz.id, encoding='utf-8', xml_declaration=True)

    # with tempfile.TemporaryDirectory(dir = os.getcwd() + '\\temp') as td:
    #     with zipfile.ZipFile(td, 'w', zipfile.ZIP_DEFLATED) as zf:
    #         zf.write('temp/quiz.id')

def createQTI(quiz : Quiz):
    root = ET.Element('questestinterop')
    root.set("xmlns", "http://www.imsglobal.org/xsd/ims_qtiasiv1p2")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:schemaLocation", "http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd")
    
    assessment = ET.SubElement(root, 'assessment', ident=quiz.id, title=quiz.title)

    qtimetadata = ET.SubElement(assessment, 'qtimetadata')
    meta_field(qtimetadata, 'cc_maxattempts', 'unlimited')

    section = ET.SubElement(assessment, 'section', ident="root_section")
    for q in quiz.questions:
        add_question(section, q)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    
    return tree   
    
def add_question(node, question : Question):
    item = ET.SubElement(node, 'item', ident=question.parent_id, title=question.question_title)
    itemmetadata = ET.SubElement(item, 'itemmetadata')
    qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
    meta_field(qtimetadata, 'question_type', question.question_type)
    meta_field(qtimetadata, 'points_possible', question.points_possible)
    meta_field(qtimetadata, 'original_answer_ids', ",".join(get_original_answer_ids(question)))
    meta_field(qtimetadata, 'assessment_question_identifierref', question.question_id)

    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext_html(material, question.question_content)
    fill_presentation(presentation, question)

    if question.question_type != 'text_only_question':
        resprocessingTag = ET.SubElement(item, 'resprocessing')
        outcomes = ET.SubElement(resprocessingTag, 'outcomes')
        ET.SubElement(outcomes, 'decvar', maxvalue='100', minvalue='0', varname='SCORE', vartype='Decimal')
        resprocessing(resprocessingTag, question)

    itemproc_extension_gen(item, question)

    feedback_gen(item, question)

#------------------RESPROCESSING--------------------

def resprocessing(node, question):

    answer_feedback_resprocessing(node, question)

    if question.question_type in ["multiple_choice_question", "true_false_question"]:
        multiple_choice_resprocessing(node, question)
    elif question.question_type == "multiple_answers_question":
        multiple_answer_resprocessing(node, question)
    elif question.question_type == "short_answer_question":
        short_answer_resprocessing(node, question)
    elif question.question_type == "essay_question":
        essay_resprocessing(node, question)
    elif question.question_type == "matching_question":
        matching_resprocessing(node, question)
    elif question.question_type in ["multiple_dropdowns_question", "fill_in_multiple_blanks_question"]:
        multiple_dropdowns_resprocessing(node, question)
    elif question.question_type == "calculated_question":
        calculated_resprocessing(node, question)
    elif question.question_type == "numerical_question":
        numerical_resprocessing(node, question)

def answer_feedback_resprocessing(node, question : Question):
    for id in question.feedback:
        if id not in ['correct', 'general_incorrect', 'general'] and question.question_type not in ["matching_question"]:
            respcondition = ET.SubElement(node, 'respcondition')
            respcondition.set('continue', 'Yes')
            conditionvar = ET.SubElement(respcondition, 'conditionvar')

            respident_name = "response1"
            if question.question_type in ['multiple_dropdowns_question', 'fill_in_multiple_blanks_question']:
                for key, value in question.correct_choices.items():
                    if list(value)[0] == id:
                        name = key
                
                respident_name = 'response_' + name

            if question.question_type == 'short_answer_question':
                ET.SubElement(conditionvar, 'varequal', respident=respident_name).text = question.correct_choices[id]
            else:
                ET.SubElement(conditionvar, 'varequal', respident=respident_name).text = id

            ET.SubElement(respcondition, 'displayfeedback', feedbacktype="Response", linkrefid=id + '_fb')
        elif (id == 'general_incorrect' and question.question_type not in ['matching_question', 'multiple_dropdowns_question', 'fill_in_multiple_blanks_question', 'numerical_question']) or id =='general' :
            respcondition = ET.SubElement(node, 'respcondition')
            respcondition.set('continue', 'Yes')
            conditionvar = ET.SubElement(respcondition, 'conditionvar')
            ET.SubElement(conditionvar, 'other')
            ET.SubElement(respcondition, 'displayfeedback', feedbacktype="Response", linkrefid=id + '_fb')

def multiple_choice_resprocessing(node, question : Question):
    respcondition = ET.SubElement(node, 'respcondition')
    respcondition.set('continue', 'No')

    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    ET.SubElement(conditionvar, 'varequal', respident= 'response1').text = question.correct_choice

    ET.SubElement(respcondition, 'setvar', action="Set", varname="SCORE").text = '100'
    correct_feedback_gen(respcondition, question)

def multiple_answer_resprocessing(node, question : Question):
    respcondition = ET.SubElement(node, 'respcondition')
    respcondition.set('continue', 'No')

    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    andTag = ET.SubElement(conditionvar, 'and')
    for id in question.correct_choices:
        ET.SubElement(andTag, 'varequal', respident= 'response1').text = id

    for id in question.choices:
        if id not in question.correct_choices:
            notTag = ET.SubElement(andTag, 'not')
            ET.SubElement(notTag, 'varequal', respident= 'response1').text = id

    ET.SubElement(respcondition, 'setvar', action="Set", varname="SCORE").text = '100'
    correct_feedback_gen(respcondition, question)

def short_answer_resprocessing(node, question : Question):
    respcondition = ET.SubElement(node, 'respcondition')
    respcondition.set('continue', 'No')

    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    for id in question.correct_choices:
        ET.SubElement(conditionvar, 'varequal', respident= 'response1').text = question.correct_choices[id]

    ET.SubElement(respcondition, 'setvar', action="Set", varname="SCORE").text = '100'
    correct_feedback_gen(respcondition, question)

def essay_resprocessing(node, question : Question):
    respcondition = ET.SubElement(node, 'respcondition')
    respcondition.set('continue', 'No')

    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    ET.SubElement(conditionvar, 'other')

def matching_resprocessing(node, question : Question):
    points = 100 / len(question.correct_choices)
    points = "%.2f" % points

    for key, value in question.correct_choices.items():
        respcondition = ET.SubElement(node, 'respcondition')

        conditionvar = ET.SubElement(respcondition, 'conditionvar')
        ET.SubElement(conditionvar, 'varequal', respident= 'response_' + key).text = value
        ET.SubElement(respcondition, 'setvar', varname="SCORE", action="Add").text = points

        if key in question.feedback:
            respcondition = ET.SubElement(node, 'respcondition')

            conditionvar = ET.SubElement(respcondition, 'conditionvar')
            notTag = ET.SubElement(conditionvar, 'not')
            ET.SubElement(notTag, 'varequal', respident= 'response_' + key).text = value
            ET.SubElement(respcondition, 'displayfeedback', feedbacktype="Response", linkrefid= key + "_fb")

def multiple_dropdowns_resprocessing(node, question : Question):
    points = 100 / len(question.correct_choices)
    points = "%.2f" % points

    for key, value in question.correct_choices.items():
        respcondition = ET.SubElement(node, 'respcondition')

        conditionvar = ET.SubElement(respcondition, 'conditionvar')
        ET.SubElement(conditionvar, 'varequal', respident= 'response_' + key).text = value if question.question_type == 'multiple_dropdowns_question' else list(value)[0]

        ET.SubElement(respcondition, 'setvar', varname="SCORE", action="Add").text = points

def calculated_resprocessing(node, question : Question):
    respcondition = ET.SubElement(node, 'respcondition', title='correct')
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    ET.SubElement(conditionvar, 'other')

    ET.SubElement(respcondition, 'setvar', action="Set", varname="SCORE").text = '100'

    respcondition = ET.SubElement(node, 'respcondition', title='incorrect')
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    notTag = ET.SubElement(conditionvar, 'not')
    ET.SubElement(notTag, 'other')

    ET.SubElement(respcondition, 'setvar', action="Set", varname="SCORE").text = '0'

def numerical_resprocessing(node, question : Question):
    for key, value in question.exact_answers.items():
        respcondition = ET.SubElement(node, 'respcondition')
        respcondition.set('continue', 'No')

        conditionvar = ET.SubElement(respcondition, 'conditionvar')
        if value is None:
            ET.SubElement(conditionvar, 'vargte', respident="response1").text = question.answer_ranges[key][0]
            ET.SubElement(conditionvar, 'varlte', respident="response1").text = question.answer_ranges[key][1]
        else:
            orTag = ET.SubElement(conditionvar, 'or')
            ET.SubElement(orTag, 'varequal', respident="response1").text = value
            andTag = ET.SubElement(orTag, 'and')
            ET.SubElement(andTag, 'vargte', respident="response1").text = question.answer_ranges[key][0]
            ET.SubElement(andTag, 'varlte', respident="response1").text = question.answer_ranges[key][1]

        ET.SubElement(respcondition, 'setvar', action="Set", varname="SCORE").text = '100'
        if key in question.feedback:
            ET.SubElement(respcondition, 'displayfeedback', feedbacktype="Response", linkrefid= key + "_fb")
        if 'correct' in question.feedback:
            ET.SubElement(respcondition, 'displayfeedback', feedbacktype="Response", linkrefid= "correct_fb")

def itemproc_extension_gen(node, question):
    if question.question_type == 'calculated_question':
        itemproc_extension = ET.SubElement(node, 'itemproc_extension')
        calculated = ET.SubElement(itemproc_extension, 'calculated')
        ET.SubElement(calculated, 'answer_tolerance').text = question.equation.answer_tolerance

        for equ in question.equation.formulas:
            formulas = ET.SubElement(calculated, 'formulas', decimal_places=question.equation.decimal_places)
            ET.SubElement(formulas, 'formula').text = equ

        vars = ET.SubElement(calculated, 'vars')
        for key, value in question.equation.variable_range.items():
            var = ET.SubElement(vars, 'var', name=key, scale=question.equation.variable_scale[key])
            ET.SubElement(var, 'min').text = list(value.keys())[0]
            ET.SubElement(var, 'max').text = list(value.values())[0]
    
        var_sets = ET.SubElement(calculated, 'var_sets')
        for variable in question.possible_questions:
            var_set = ET.SubElement(var_sets, 'var_set', ident=variable.id)
            ET.SubElement(var_set, 'var', name=list(variable.variable_name_value.keys())[0]).text = list(variable.variable_name_value.values())[0]
            ET.SubElement(var_set, 'answer').text = variable.answers[0]


def feedback_gen(node, question):
    for key, value in question.feedback.items():
        itemfeedback = ET.SubElement(node, 'itemfeedback', ident=key + '_fb')
        flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
        material = ET.SubElement(flow_mat, 'material')
        mattext_html(material, value)

def correct_feedback_gen(node, question):
    if 'correct' in question.feedback:
        ET.SubElement(node, 'displayfeedback', feedbacktype="Response", linkrefid="correct_fb")

#------------------PRESENTATION--------------------

def fill_presentation(node, question):
    if question.question_type in ["multiple_choice_question", "true_false_question", "multiple_answers_question"]:
        multiple_choice_response(node, question)
    elif question.question_type in ["short_answer_question", "essay_question"]:
        short_answer_response(node, question)
    elif question.question_type == "matching_question":
        matching_response(node, question)
    elif question.question_type in ["multiple_dropdowns_question", "fill_in_multiple_blanks_question"]:
        multiple_dropdowns_response(node, question)
    elif question.question_type in ["calculated_question", "numerical_question"]:
        calculated_numeric_response(node, question)

def multiple_choice_response(node, question):
    response_lid = ET.SubElement(node, 'response_lid', ident='response1', rcardinality="Multiple" if question.question_type == 'multiple_answers_question' else "Single")
    render_choice = ET.SubElement(response_lid, 'render_choice')

    for id, value in question.choices.items():
        response_label = ET.SubElement(render_choice, 'response_label', ident=id)
        material = ET.SubElement(response_label, 'material')
        mattext_html(material, value)

def short_answer_response(node, question):
    response_str = ET.SubElement(node, 'response_str', ident='response1', rcardinality='Single')
    render_fib = ET.SubElement(response_str, 'render_fib')
    ET.SubElement(render_fib, 'response_label', ident='answer1', rshuffle='No')

def matching_response(node, question):
    for key, value in question.left_choices.items():
        response_lid = ET.SubElement(node, 'response_lid', ident='response_' + key)

        material = ET.SubElement(response_lid, 'material')
        mattext_html(material, value)

        render_choice = ET.SubElement(response_lid, 'render_choice')
        for id, val in question.right_choices.items():
            response_label = ET.SubElement(render_choice, 'response_label', ident=id)
            material = ET.SubElement(response_label, 'material')
            ET.SubElement(material, 'mattext').text = val

def multiple_dropdowns_response(node, question):
    choices = question.choices if question.question_type == 'multiple_dropdowns_question' else question.correct_choices

    for key, value in choices.items():
        response_lid = ET.SubElement(node, 'response_lid', ident='response_' + key)

        material = ET.SubElement(response_lid, 'material')
        ET.SubElement(material, 'mattext').text = key

        render_choice = ET.SubElement(response_lid, 'render_choice')
        for id, val in value.items():
            response_label = ET.SubElement(render_choice, 'response_label', ident=id)

            material = ET.SubElement(response_label, 'material')
            mattext_html(material, val)

def calculated_numeric_response(node, question):
    response_str = ET.SubElement(node, 'response_str', ident='response1', rcardinality='Single')
    render_fib = ET.SubElement(response_str, 'render_fib', fibtype='Decimal')
    ET.SubElement(render_fib, 'response_label', ident='answer1')    

def get_original_answer_ids(question : Question):
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
            
def mattext_html(node, value):
    if '<div>' in value or '<p>' in value:
        ET.SubElement(node, 'mattext', texttype="text/html").text = value
    else:
        ET.SubElement(node, 'mattext', texttype="text/plain").text = value

def prettify(elem):
     rough_string = ET.tostring(elem, 'utf-8')
     reparsed = minidom.parseString(rough_string)
     uglyXml = reparsed.toprettyxml(indent="\t")
     pattern = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
     return pattern.sub('>\g<1></', uglyXml)

def meta_field(node, label, entry):
    qtimetadatafield = ET.SubElement(node, 'qtimetadatafield')
    ET.SubElement(qtimetadatafield, 'fieldlabel').text = label
    ET.SubElement(qtimetadatafield, 'fieldentry').text = entry
