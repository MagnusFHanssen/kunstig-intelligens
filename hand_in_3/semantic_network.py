# Module for simple semantic networks

class Network:
    """Class for semantic networks"""
    def __init__(self):
        self.concepts = []
        self.relations = []

    def knows(self, concept):
        if isinstance(concept, Concept):
            return concept in self.concepts
        else:
            return concept in [c.name for c in self.concepts]



class Concept:
    """Class for a concept in a semantic network"""
    def __init__(self, name):
        self.name = name


class Relation:
    """Relation between concepts in a semantic network"""
    def __init__(self, subject, direct_object, descriptor):
        self.descriptor = descriptor
        self.subject = subject
        self.direct_object = direct_object
