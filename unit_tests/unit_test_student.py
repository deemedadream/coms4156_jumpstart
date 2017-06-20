import logging
import sys
import pytest
import flask

from models.model import Model
from models import students_model
from google.cloud import datastore

TEST_STUDENT = dict(sid=1, uni='tst9999')
TEST_COURSES = [dict(tid=t, cid=c) for t,c in [(1, 1), (2, 2)]]
TEST_ENROLLMENT = [dict(sid=TEST_STUDENT['sid'], cid=c['cid'])
                   for c in TEST_COURSES]

class TestStudent(Model):

    '''Storing mock data'''

    @pytest.fixture(scope='module')
    def student(self):
        ds = self.get_client()
        key = ds.key('student')
        entity = datastore.Entity(
            key=key
        )
        entity.update(TEST_STUDENT)
        ds.put(entity)
        student = students_model.Students(
            TEST_STUDENT['sid']
        )
        return student

    @pytest.fixture(scope='module')
    def student_with_courses(self):
        ds = self.get_client()
        #add student
        key_s = ds.key('student')
        entity_s = datastore.Entity(
            key=key_s
        )
        entity_s.update(TEST_STUDENT)
        ds.put(entity_s)
        student = students_model.Students(
            TEST_STUDENT['sid']
        )

        #add courses
        key_c = ds.key('courses')
        entity_c = datastore.Entity(
            key=key_c
        )
        for course in TEST_COURSES:
            entity_c.update(course)
        ds.put(entity_c)

        #add enrollments
        key_e = ds.key('enrollments')
        entity_e = datastore.Entity(
            key=key_e
        )
        for course in TEST_COURSES:
            entity_e.update(course)
        ds.put(entity_e)

        return student

    '''Tests'''

    def test_get_uni_existing_student(self, student):
        uni = student.get_uni()
        assert uni == TEST_STUDENT['uni']

    def test_get_uni_nonexistant_student(self):
        invalid_id = 9999
        student = students_model.Students(invalid_id)
        uni = student.get_uni()
        assert uni is None

    def test_get_courses(self, student_with_courses):
        student = student_with_courses
        courses = student.get_courses()
        assert len(courses) == len(TEST_ENROLLMENT)

    def test_get_courses_no_courses(self, student):
        courses = student.get_courses()
        assert len(courses) == 0

