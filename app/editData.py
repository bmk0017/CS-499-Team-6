from app.question import *
from app.quiz import *

class Edit:

    mcQuestion = MultipleChoice()
    tfQuestion = TrueFalse()
    fillQuestion = FillintheBlank()
    fillMultiQuestion = FillinMultipleBlanks()
    multiAnsQuestion = MultipleAnswers()
    multiDropQuestion = MultipleDropdowns()
    matchQuestion = Matching()
    question = Question()
    quiz = Quiz()

    def editQuizTitle(quiz, newQuizTitle):

        quiz.title = newQuizTitle
        return quiz
    
    def editQuizPoints(quiz, newQuizPoints):

        quiz.point_possible_total = newQuizPoints
        return quiz

    def editQuizDescription(quiz, newQuizDescription):

        quiz.description = newQuizDescription
        return quiz
    
    def changeShuffling(quiz):

        return not quiz.shuffle_answers
    
    def editQuestionTitle(question, newQuestTitle):

        question.title = newQuestTitle
        return question
    
    def editQuestionPoints(question, newQuestPoints):

        question.points_possible = newQuestPoints
        return question
    
    def editQuestionContent(question, newQuestContent):

        question.content = newQuestContent
        return question
    
    def replaceAllQuestionChoices(mcQuestion, newQuestionChoices):

        mcQuestion.choices = newQuestionChoices
        return mcQuestion
    
    def addQuestionChoice(mcQuestion, newQuestionChoice):

        mcQuestion.choices.append(newQuestionChoice)
        return mcQuestion
    
    def replaceQuestionChoice(mcQuestion, newQuestionChoice, x):

        mcQuestion.choices[x] = newQuestionChoice
        return mcQuestion
    
    def changeQuestionMCCorrectChoice(mcQuestion, newQuestionCorrect):

        mcQuestion.correct_choice = newQuestionCorrect
        return mcQuestion
    
    def changeQuestionTFCorrectChoice(tfQuestion):

        return not tfQuestion
    
    def changeQuestionFBCorrectChoice(fillQuestion, newQuestionCorrect):

        fillQuestion.correct_choice = newQuestionCorrect
        return fillQuestion
    
    def addQuestion(quiz, question):

        quiz.questions.append(question)
        return quiz
    
    def deleteQuestion(quiz, question):

        if quiz.questions[question]:
            quiz.questions.remove(question)
        
        else:
            print("No question exists")

        return quiz
    