import logging
import sys
import pytest
import flask

from models.model import Model
from models import attendance_record_model as arm
from models import students_model
from google.cloud import datastore

TEST_STUDENT = dict(sid=1, uni='tst9999')
TEST_COURSES = [dict(tid=t, cid=c) for t,c in [(1, 1), (2, 2)]]
TEST_ENROLLMENTS = [dict(sid=TEST_STUDENT['sid'], cid=c['cid'])
                    for c in TEST_COURSES]
TEST_SESSIONS = [dict(cid=c[i]['cid'], seid=i)
                 for i in range(len(TEST_COURSES))]
TEST_RECORD = dict(sid=TEST_STUDENT['sid'],
                   seid=TEST_SESSIONS[0]['seid'])
TEST_EXCUSE = dict(sid=TEST_RECORD['sid'],
                   seid=TEST_RECORD['seid'],
                   excuse='Excuse me.')

class TestAttendanceRecord(Model):

    '''Mock Data'''

    @pytest.fixture(scope='module')
    def student_with_courses(self):
        ds = self.get_client()
        # add student
        key_s = ds.key('student')
        entity_s = datastore.Entity(
            key=key_s
        )
        entity_s.update(TEST_STUDENT)
        ds.put(entity_s)
        student = students_model.Students(
            TEST_STUDENT['sid']
        )

        # add courses
        key_c = ds.key('courses')
        entity_c = datastore.Entity(
            key=key_c
        )
        for course in TEST_COURSES:
            entity_c.update(course)
        ds.put(entity_c)

        # add enrollments
        key_e = ds.key('enrollments')
        entity_e = datastore.Entity(
            key=key_e
        )
        for course in TEST_COURSES:
            entity_e.update(course)
        ds.put(entity_e)

        # add sessions
        key_se = ds.key('sessions')
        entity_se = datastore.Entity(
            key=key_se
        )
        for session in TEST_SESSIONS:
            entity_se.update(session)
        ds.put(entity_se)

        return student

    '''Tests'''

    def test_insert_attendance_record(self, student_with_courses):
        session = TEST_SESSIONS[0]
        record = arm.Attendance_Record(
            TEST_STUDENT['sid'],
            session['seid']
        )
        record.insert_attendance_record()
        stored_record = arm.Attendance_Record.get_record(
            TEST_STUDENT['sid'],
            session['seid']
        )
        assert stored_record.sid == TEST_STUDENT['sid']
        assert stored_record.seid == session['seid']

    def test_insert_attendance_record_without_enrollment(self):
        session = TEST_SESSIONS[0]
        record = arm.Attendance_Record(
            TEST_STUDENT['sid'],
            session['seid']
        )
        record.insert_attendance_record()
        results = arm.Attendance_Record.get_record(
            TEST_STUDENT['sid'],
            session['seid']
        )
        assert len(results) == 0

    def test_remove_attendance_record(self, student_with_courses):
        ds = self.get_client()
        key = ds.key('attendance_record')
        entity = datastore.Entity(key=key)
        entity.update(TEST_RECORD)
        ds.put(entity)

        ar = arm.Attendance_Record(**TEST_RECORD)
        ar.remove_attendance_record()

        results = arm.Attendance_Record.get_record(
            **TEST_RECORD
        )
        assert len(results) == 0

    def test_provide_excuse(self, student_with_courses):
        ar = arm.Attendance_Record(**TEST_RECORD)
        ar.provide_excuse(excuse=TEST_EXCUSE['excuse'])

        result = ar.get_excuse()
        assert len(result) == 1
        assert result[0].sid == TEST_RECORD['sid']
        assert result[0].seid = TEST_RECORD['seid']
        assert result[0].excuse == TEST_EXCUSE['excuse']

    def test_provide_excuse_without_absence(self, student_with_courses):
        ds = self.get_client()
        key = ds.key('attendance_record')
        entity = datastore.Entity(key=key)
        entity.update(TEST_RECORD)
        ds.put(entity)

        ar = arm.Attendance_Record(**TEST_RECORD)
        ar.provide_excuse(TEST_EXCUSE['excuse'])

        result = ar.get_excuse()
        assert len(result) == 0

    def test_remove_excuse(self, student_with_courses):
        ds = self.get_client()
        key = ds.key('excuses')
        entity = datastore.Entity(key=key)
        entity.update(TEST_EXCUSE)
        ds.put(entity)

        ar = arm.Attendance_Record(**TEST_RECORD)
        ar.remove_excuse()

        result = ar.get_excuse()
        assert len(result) == 0
