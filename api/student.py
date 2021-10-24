from main import db
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint


class Student(db.Model):
    __tablename__ = 'students'

    studentID = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(30), nullable=False)
    sPosition = db.Column(db.String(30), nullable = False)


    def __init__(self, studentID, studentName, sPosition):
        self.studentID = studentID
        self.studentName = studentName
        self.sPosition = sPosition


    def json(self):
        return {
            "studentID" : self.studentID,
            "studentName": self.studentName,
            "sPosition" : self.sPosition,
        }

    def get_all():
        try:
            studentList = Student.query.all()
            if len(studentList):
                return 200, [student.json() for student in studentList]
        except Exception as e:
            return 404, "There are no students. " + str(e)