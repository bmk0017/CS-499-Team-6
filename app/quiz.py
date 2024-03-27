import logging
import xml.etree.ElementTree as ET
from typing import List
import hashlib

class Quiz:
    id: str
    title: str
    point_possible_total: int
    description: str
    questions: List
    shuffle_answers: bool

    def __init__(self):
        self.questions = []

    def __str__(self):
        return '\n'.join([str(q) for q in self.questions])
    
    def getHash(self):
        return 'i' + hashlib.md5(str(self).encode()).hexdigest()
