import logging
import sys
import unittest
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from unit_test_base import BaseTestCase
from models import students_model as sm

from datetime import date, timedelta
from random import randint
from google.cloud import datastore

STUDENT = dict(sid=1, uni='tst9999')

COURSES = [dict(tid=t, cid=c) for t,c in [(1, 1), (2, 2)]]

ENROLLMENT = [dict(sid=STUDENT['sid'], cid=c['cid'])
                   for c in COURSES]

SESSIONS = [dict(seid=i,
                 cid=COURSES[0]['cid'],
                 date=str(date.today() - timedelta(days=i)),
                 window_open=False,
                 secret=randint(1000, 9999)) for i in range(5)]

RECORDS = [dict(seid=s['seid'],
                sid=STUDENT['sid']) for s in SESSIONS]

class StudentTestCase(BaseTestCase):

    def setUp(self):
        super(StudentTestCase, self).setUp()
        self.store_model('student', **STUDENT)
        for course in COURSES:
            self.store_model('courses', **course)

    def test_get_uni_existing_student(self):
        student = sm.Students(sid=STUDENT['sid'])
        uni = student.get_uni()
        self.assertEquals(uni, STUDENT['uni'])

    def test_get_uni_nonexistant_student(self):
        invalid_id = 9999
        student = sm.Students(sid=invalid_id)
        uni = student.get_uni()
        self.assertFalse(uni)

    def test_get_courses(self):
        student = sm.Students(sid=STUDENT['sid'])
        for enrolled in ENROLLMENT:
            self.store_model('enrolled_in', **enrolled)

        student_courses = sorted(student.get_courses(), 
                                 key=lambda c: c['cid'])
        correct_courses = sorted(COURSES, 
                                 key=lambda x: x['cid'])
        self.assertEquals(len(student_courses), len(correct_courses))
        '''
        for c1, c2 in zip(student_courses, correct_courses):
            for c_field in c1:
                self.assertEquals(c1[c_field], c2[c_field])
        '''

    def test_get_courses_no_courses(self):
        student = sm.Students(sid=STUDENT['sid'])
        courses = student.get_courses()

        self.assertEquals(len(courses), 0)

    def test_get_course_attendance(self):
        for session in SESSIONS:
            self.store_model('sessions', **session)

        for record in RECORDS:
            self.store_model('attendance_records', **record)

        student = sm.Students(sid=STUDENT['sid'])
        attendance = sorted(student.get_course_attendance(COURSES[0]['cid']), 
                            key=lambda x: x['seid'])
        correct_att = sorted(SESSIONS, key=lambda x: x['seid'])

        self.assertEquals(len(attendance), len(correct_att))
        for s1, s2 in zip(attendance, correct_att):
            for attr in s1:
                self.assertEquals(s1[attr], s2[attr])

if __name__ == '__main__':
    unittest.main()

