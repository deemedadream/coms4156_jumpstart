import logging
import sys
import flask
import unittest
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from unit_test_base import BaseTestCase
from models import model as m, \
                   students_model as sm, \
                   courses_model as cm, \
                   teachers_model as tm, \
                   sessions_model as ssm, \
                   attendance_records_model as arm

from google.cloud import datastore
from datetime import date
from random import randint

STUDENT = dict(sid=1,
               uni='tst9999')

COURSES = [dict(tid=1, cid=1, name='c1'),
           dict(tid=2, cid=2, name='c2')]

ENROLLS = [dict(sid=STUDENT['sid'],
                cid=c['cid']) for c in COURSES]

SESSIONS = [dict(seid=i,
                 cid=c['cid'],
                 date=str(date.today()),
                 window_open=False,
                 secret=randint(1000, 9999)) for i, c in enumerate(COURSES)]

RECORD = dict(sid=STUDENT['sid'],
               seid=SESSIONS[0]['seid'])

EXCUSE = dict(sid=STUDENT['sid'],
              seid=SESSIONS[1]['seid'],
              excuse='Excuse me.')

"""Utility function"""

"""Testing context for unit tests"""

class AttendanceTestCase(BaseTestCase):

    def setUp(self):
        super(AttendanceTestCase, self).setUp()

        self.context = {}
        self.context['student'] = [self.store_model('student', **STUDENT)]
        self.context['courses'] = [self.store_model('courses', **course)
                   for course in COURSES]
        self.context['enrolled_in'] = [self.store_model('enrolled_in', **e)
                   for e in ENROLLS]
        self.context['sessions'] = [self.store_model('sessions', **s)
                    for s in SESSIONS]
        self.student = sm.Students(STUDENT['sid']),
        self.courses = [cm.Courses(c['cid']) for c in COURSES],
        self.record = arm.Attendance_Records(sid=RECORD['sid'], seid=RECORD['seid'])

    def test_insert_attendance_record(self):
        #check record already existis
        check = self.get_model('attendance_records',
                               sid=self.record.sid,
                               seid=self.record.seid)
        self.store_context('attendance_records', **RECORD)
        self.assertFalse(check)
        self.record.insert_attendance_record()
        result = self.get_model('attendance_records', 
                                sid=self.record.sid,
                                seid=self.record.seid)
        self.assertTrue(result)
        self.assertEquals(result['sid'], self.record.sid)
        self.assertEquals(result['seid'], self.record.seid)

    def test_insert_attendance_record_without_enrollment(self):
        record = dict(sid=STUDENT['sid'], seid=SESSIONS[1]['seid'])
        self.store_context('attendance_records', **record)
        check = self.get_model('attendance_records', **record)
        self.assertFalse(check)

        record_model = arm.Attendance_Records(**record)
        record_model.insert_attendance_record()
        result = self.get_model('attendance_records', **record)
        self.assertFalse(result)

    def test_remove_attendance_record(self):
        record = RECORD
        self.store_model('attendance_records', **record)
        check = self.get_model('attendance_records', **record)
        self.assertTrue(check)
        
        record_model = arm.Attendance_Records(**record)
        record_model.remove_attendance_record()
        result = self.get_model('attendance_records', **record)

        self.assertFalse(result)

    def test_provide_excuse(self):
        self.store_context('excuses', **EXCUSE)
        #check if attendance and excuses exist
        check_attendance = self.get_model('attendance_records',
                                          sid=EXCUSE['sid'],
                                          seid=EXCUSE['seid'])
        check_excuse = self.get_model('excuses', **EXCUSE)
        self.assertFalse(check_attendance)
        self.assertFalse(check_excuse)

        ar = arm.Attendance_Records(sid=EXCUSE['sid'],
                                    seid=EXCUSE['seid'])
        ar.provide_excuse(EXCUSE['excuse'])
        excuse = self.get_model('excuses', **EXCUSE)

        self.assertTrue(excuse)
        for field in EXCUSE:
            self.assertEquals(excuse[field], EXCUSE[field])

    def test_provide_excuse_without_absence(self):
        record = dict(sid=EXCUSE['sid'], seid=EXCUSE['seid'])
        self.store_model('attendance_records', **record)
        check_attendance = self.get_model('attendance_records', **record)
        self.assertTrue(check_attendance)

        self.store_context('excuses', **EXCUSE)
        ar = arm.Attendance_Records(**record)
        ar.provide_excuse(EXCUSE['excuse'])
        excuse = self.get_model('excuses', **EXCUSE)

        self.assertFalse(excuse)

    def test_remove_excuse(self):
        self.store_model('excuses', **EXCUSE)
        check = self.get_model('excuses', **EXCUSE)
        self.assertTrue(check)

        record_model = arm.Attendance_Records(sid=EXCUSE['sid'],
                                              seid=EXCUSE['seid'])
        record_model.remove_excuse()
        excuse = self.get_model('excuses', **EXCUSE)
        self.assertFalse(excuse)

if __name__ == '__main__':
    unittest.main()
