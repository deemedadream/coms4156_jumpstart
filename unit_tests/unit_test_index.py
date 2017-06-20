import logging
import sys
import pytest
import flask

from models.model import Model
from models import index_model
from models import students_model
from google.cloud import datastore

TEST_STUDENT = dict(sid=1, uni='tst9999')
TEST_TEACHER = dict(tid=2)

class TestIndex(Model):

    '''Store mock data'''

    @pytest.fixture(scope='module')
    def student_and_teacher(self):
        ds = self.get_client()
        key_s = ds.key('student')
        entity = datastore.Entity(
            key=key_s
        )
        entity.update(TEST_STUDENT)
        ds.put(entity)

        key_t = ds.key('teacher')
        entity_t = datastore.Entity(
            key=key_t
        )
        ds.put(entity_t)

    '''Tests'''

    def test_is_student(self, student_and_teacher):
        user = index_model.Index(uid=TEST_STUDENT['sid'])
        assert user.is_student()

    def test_is_student_but_not_student(self, student_and_teacher):
        user = index_model.model.Index(uid=TEST_TEACHER['tid'])
        assert not user.is_student()

    def test_is_teacher(self, student_and_teacher):
        user = index_model.Index(uid=TEST_TEACHER['sid'])
        assert user.is_teacher()

    def test_is_teacher_but_not_teacher(self, student_and_teacher):
        user = index_model.model.Index(uid=TEST_STUDENT['tid'])
        assert not user.is_teacher()