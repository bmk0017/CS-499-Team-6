import logging
import xml.etree.ElementTree as ET
from typing import List

class Quiz:
    id: str
    title: str
    point_possible_total: int
    description: str
    questions: List
    shuffle_answers: bool

    def __init__(self):
        self.questions = []
