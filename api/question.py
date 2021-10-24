from main import db
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint


class Question(db.Model):
    __tablename__ = 'questions'

    secCourseID = db.Column(db.Integer, primary_key=True)
    secClassID = db.Column(db.String(30), nullable=False)
    sectionID = db.Column(db.String(30))
    question = db.Column(db.String(255))
    other = db.Column(db.String(255))


    def __init__(self, secCourseID, secClassID, sectionID, question, answer, other):
        self.secCourseID = secCourseID
        self.secClassID = secClassID
        self.sectionID = sectionID
        self.question = question
        self.other = other


    def json(self):
        return {
            "secCourseID" : self.secCourseID,
            "secClassID": self.secClassID,
            "sectionID" : self.sectionID,
            "question": self.question,
            "other": self.other
        }

    def compute_score(self):