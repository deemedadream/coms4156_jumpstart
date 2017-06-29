import logging
import sys
import flask
import unittest
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from unit_test_base import BaseTestCase
from models import model as m, \
                   students_model as sm, \
                   teachers_model as tm, \
                   index_model as im

from google.cloud import datastore
from datetime import date
from random import randint

STUDENT = dict(sid=1, uni='tst9999')
TEACHER = dict(tid=2)


class IndexTestCase(BaseTestCase):

    def setUp(self):
        super(IndexTestCase, self).setUp()
        self.store_model('student', **STUDENT)
        self.store_model('teacher', **TEACHER)        

    '''Tests'''

    def test_is_student(self):
        user = im.Index(uid=STUDENT['sid'])
        self.assertTrue(user.is_student())

    def test_is_student_but_not_student(self):
        user = im.Index(uid=TEACHER['tid'])
        self.assertFalse(user.is_student())

    def test_is_teacher(self):
        user = im.Index(uid=TEACHER['tid'])
        self.assertTrue(user.is_teacher())

    def test_is_teacher_but_not_teacher(self):
        user = im.Index(uid=STUDENT['sid'])
        self.assertFalse(user.is_teacher())


if __name__ == '__main__':
    unittest.main()