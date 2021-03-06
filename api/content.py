from main import db
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint
from section import Section


class Content(db.Model):
    __tablename__ = 'contents'

    conCourseID = db.Column(db.String(30), primary_key=True)
    conClassID = db.Column(db.Integer, nullable=False, primary_key=True)
    conSectionID = db.Column(db.String(30), nullable=False, primary_key=True)
    contentID = db.Column(db.String(255), primary_key=True)
    conName = db.Column(db.String(255), nullable=False)
    doctype = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)

    __table_args__ = (ForeignKeyConstraint([conCourseID, conClassID, conSectionID],
                    [Section.secCourseID, Section.secClassID, Section.sectionID]),
                      {})
    sectionContent = db.relationship(
    'Section', primaryjoin='and_(Content.conClassID == Section.secClassID, Section.secCourseID == Content.conCourseID, Section.sectionID == Content.conSectionID)', backref='contents')

    def __init__(self, conCourseID, conClassID, conSectionID, contentID, conName, doctype, link):
        self.conCourseID = conCourseID
        self.conClassID = conClassID
        self.conSectionID = conSectionID
        self.contentID = contentID
        self.conName = conName
        self.doctype = doctype
        self.link = link


    def json(self):
        return {
            "contentID": self.contentID,
            "name": self.conName,
            "doctype": self.doctype,
            "link": self.link
        }
        
    def get_section_content(courseID, classID, sectionID):
        try:
            contentList = Content.query.filter_by(conCourseID=courseID, conClassID = classID, conSectionID = sectionID).all()
            return 200, [content.json() for content in contentList]
        except Exception as e:
            return 400, "No content found. " + str(e)

    def create_section_content(data):
        data = data['data']
        try:
            for content in data:
                contents = Content(content["courseID"], content["classID"], content["sectionID"], content["contentID"], content["contentName"], content["doctype"], content["link"])
                db.session.add(contents)
            db.session.commit()
            return 201, "Content created"
        except Exception as e:
            return 500, "Couldn't create"






