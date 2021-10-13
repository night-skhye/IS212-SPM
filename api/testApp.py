import unittest
import flask_testing 
import json
from unittest import mock
from app import app, db, Course, Class, Prerequisite, Student, Completed, Registration


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/testdb'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        dummyCourse = Course(1, '3D Printing Software v1.0', 'A course on 3D printing software', '3D Printing Basics, 3D Printer Software Installation', False)
        dummyClass = Class(1,3, "Lim Ah Hock", "12-Sept-2021", "14-Sept-2023", 35, "9 Oct, 2021 to 9 Nov, 2021")
        dummyUserReg = Registration(1,1,3,"enrolled")
        db.session.add(dummyCourse)
        db.session.add(dummyClass)
        db.session.add(dummyUserReg)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestCreateCourse(TestApp):
    def test_get_course(self):
        response = self.client.get("/courses")
        self.assertEqual(response.json['code'], 200)

    def test_get_course_by_id(self):
        response = self.client.get("/courses/1")
        self.assertEqual(response.json['code'], 200)

class TestCreatePrereq(TestApp):
    def test_get_prereq_by_courseid(self):
        response = self.client.get("/prereqs/3")
        self.assertEqual(response.json['code'], 200)

class TestRegistration(TestApp):
    def test_force_update_registration_success(self):
        request_body = {
            "regStudentID": 1, 
            "regCourseID": 1, 
            "regClassID": 3, 
            "regStatus": "assigned"
        }
        response = self.client.post("/registerClass",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        print(response.json)
        self.assertEqual(response.json['data'], {"regStudentID": 1, "regCourseID": "1", "regClassID": 3, "regStatus": "assigned"})


    def test_force_create_registration_wDiff_Class_success(self):
        request_body = {
            "regStudentID": 1, 
            "regCourseID": 2, 
            "regClassID": 3, 
            "regStatus": "assigned"
        }
        response = self.client.post("/registerClass",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        print(response.json)
        self.assertEqual(response.json['data'], {"regStudentID": 1, "regCourseID": "2", "regClassID": 3, "regStatus": "assigned"})
        #create one more self.assert to check if it was deleted/updated

    def test_student_create_new_registration_success(self):
        request_body = {
            "regStudentID": 2, 
            "regCourseID": 1, 
            "regClassID": 3, 
            "regStatus": "enrolled"
        }
        response = self.client.post("/registerClass",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        print(response.json)
        self.assertEqual(response.json['data'], {"regStudentID": 1, "regCourseID": "1", "regClassID": 3, "regStatus": "enrolled"}
        )
    
    # def test_create_registration_already_taken(self):
        # d1 = Course(1, '3D Printing Software v1.0', 'A course on 3D printing software', '3D Printing Basics, 3D Printer Software Installation', False)
        # d2 = Class(1,3, "Lim Ah Hock", "12-Sept-2021", "14-Sept-2023", 35, "9 Oct, 2021 to 9 Nov, 2021")
        # d3 = Registration(1,1,3,"enrolled")
        # db.session.add(d1)
        # db.session.add(d2)
        # db.session.add(d3)
        # db.session.commit()

        # request_body = {
        #     "regStudentID": 1, 
        #     "regCourseID": 1, 
        #     "regClassID": 3, 
        #     "regStatus": "enrolled"
        # }
        # response = self.client.post("/registerClass",
        #                             data=json.dumps(request_body),
        #                             content_type='application/json')
        # print(response.json)
        # self.assertEqual(response.json['message'], {"Student has already been registered"}
        # )

    # def test_create_registration_prereqs_not_satisfied(self):
        #need to test initialising data in setUp function instead so no need to copy-paste
    
        # d1 = Course(1, '3D Printing Software v1.0', 'A course on 3D printing software', '3D Printing Basics, 3D Printer Software Installation', False)
        # d2 = Class(1,3, "Lim Ah Hock", "12-Sept-2021", "14-Sept-2023", 35, "9 Oct, 2021 to 9 Nov, 2021")
        # d3 = Registration(1,1,3,"enrolled")
        # db.session.add(d1)
        # db.session.add(d2)
        # db.session.add(d3)
        # db.session.commit()

        # request_body = {
        #     "regStudentID": 1, 
        #     "regCourseID": 1, 
        #     "regClassID": 3, 
        #     "regStatus": "enrolled"
        # }
        # response = self.client.post("/registerClass",
        #                             data=json.dumps(request_body),
        #                             content_type='application/json')
        # print(response.json)
        # self.assertEqual(response.json['message'], {"Student has already been registered"}
        # )
    # def test_create_registration_already_registered(self):

class TestCompleted(TestApp):

#Test if we are able to get the data if we create it
    def test_Completed(self):
        s1 = Student(1, 'Lim Ah Hock', 'Repair Engineer (Senior)')
        d1 = Completed(1, "3D Printing Hardware v1.0")
        db.session.add(d1)
        db.session.add(s1)
        db.session.commit()
        response = self.client.get("/completed/1",
                                    content_type='application/json')
        print(response.json['code'])
        self.assertEqual(response.json['data']['courses'], [{'ccStudentID': 1, 'completedCName': '3D Printing Hardware v1.0'}])


#test for automated courseCompleted. Once student passes the final quiz in a course, a record should be 
#automatically created in courseCompleted
    def test_auto_create_courseCompleted(self):
#Score table should be studentScore: studentID, clsCourseID, classID, clsTrainer, sectionID(chapter1), scorePercentage
        ss = studentScore(4,1,3,3,6,0.5) #SectionID should be last quiz in the course. I assume 6 is last one
        db.session.add(ss)
        db.session.commit()
        response = self.client.get("/completed/4",
                                    content_type='application/json')
        self.assertEqual(response.json['data']['courses'], [{'ccStudentID': 4, 'completedCName': '3D Printing Software v1.0'}])

#test for faulty automated courseCompleted. ONLY IF the student passes the final quiz in a course, then a record should be 
#automatically created in courseCompleted
    def test_faulty_auto_create_courseCompleted(self):
        ss2 = studentScore(4,1,3,3,3,0.5) #SectionID should be last quiz in the course
        db.session.add(ss2)
        db.session.commit()
        response = self.client.get("/completed/4",
                                    content_type='application/json')
#The creation of courseCompleted should fail as it is not the final quiz which the student passed
        self.assertEqual(response.json['code'], 500)

#Wei Xiang's TDD portion
class TestStudent(TestApp):

#Test if we are able to get the data if we create it
    def test_Student(self):
        s1 = Student(1, 'Lim Ah Hock', 'Repair Engineer (Senior)')
        db.session.add(s1)
        db.session.commit()
        response = self.client.get("/student/1",
                                    content_type='application/json')
        # print(response.json['data']['student'])
        self.assertEqual(response.json['data']['student'], {'sPosition': 'Repair Engineer (Senior)', 'studentID': 1, 'studentName': 'Lim Ah Hock'})
#Test if 2 students can have the same name. (They can)
    def test_Same_name_Student(self):
        s1 = Student(1, 'Lim Ah Hock', 'Repair Engineer (Senior)')
        s2 = Student(2, 'Lim Ah Hock', 'Repair Engineer (Senior)')
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()
        response = self.client.get("/student/2",
                                    content_type='application/json')
        self.assertEqual(response.json['code'], 200)

#Test if 2 students can have the same stuednt ID. (They cant)
#Currently there is no such function registerStudent
    def test_Same_studentID(self):
        s1 = Student(1, 'Lim Ah Hock', 'Repair Engineer (Senior)')
        # s2 = Student(1, 'Tan Kah Kee', 'Service Engineer (Junior)')
        db.session.add(s1)
        db.session.commit()
        request_body = {
            "regStudentID": 1, 
            "studentName": 'Tan Kah Kee', 
            "sPosition": 'Service Engineer (Junior)'
        }
        response = self.client.post("/registerStudent",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json['code'], 500)
        
if __name__ == '__main__':
    unittest.main()