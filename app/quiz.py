import logging
import xml.etree.ElementTree as ET
from typing import List

class Quiz:
    id: str
    quiz_name: str
    point_possible_total: int
    description: str
    quiz_type: str
    questions: List
    shuffle_answers: bool

    def __init__(self):
        self.questions = []
