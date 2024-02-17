import logging
import xml.etree.ElementTree as ET
from typing import List

class Quiz:
    id: str
    point_possible_total: int
    questions: List
