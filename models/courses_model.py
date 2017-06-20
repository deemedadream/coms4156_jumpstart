from model import Model
from datetime import datetime, date, timedelta
from random import randint
from google.cloud import datastore
import logging
import sys

class Courses(Model):

    def __init__(self, cid=-1):
        self.cid = cid
        self.course_name = ""
        self.ds = self.get_client()

    def get_course_name(self):
        query = self.ds.query(kind='courses')
        query.add_filter('cid', '=', int(self.cid))
        result = list(query.fetch())
        return result[0]['name']

    def get_students(self):
        query = self.ds.query(kind='enrolled_in')
        query.add_filter('cid', '=', int(self.cid))
        enrolled_in = list(query.fetch())
        results = list()
        for enrolled in enrolled_in:
            query = self.ds.query(kind='user')
            query.add_filter('id', '=', enrolled['sid'])
            results = results + list(query.fetch())
        return results

    def add_student(self, uni):
        query = self.ds.query(kind='student')
        query.add_filter('uni', '=', uni)
        result = list(query.fetch())

        if len(result) == 1:
            # found a student with uni, attempt to add to enrolled_in
            sid = result[0]['sid']
            query = self.ds.query(kind='enrolled_in')
            query.add_filter('sid', '=', sid)
            query.add_filter('cid', '=', int(self.cid))
            result = list(query.fetch())
            if len(result) > 0:
                # failed because already in enrolled_in
                return -2

            key = self.ds.key('enrolled_in')
            entity = datastore.Entity(
                key=key)
            entity.update({
                'sid': sid,
                'cid': int(self.cid)
            })
            self.ds.put(entity)
            return 0

        else:
            # invalid uni
            return -1

    def remove_student(self, uni):
        query = self.ds.query(kind='student')
        query.add_filter('uni', '=', uni)
        result = list(query.fetch())

        if len(result) == 1:
            # found a student with uni, attempt to remove from enrolled_in
            sid = result[0]['sid']

            query = self.ds.query(kind='enrolled_in')
            query.add_filter('sid', '=', sid)
            query.add_filter('cid', '=', int(self.cid))
            result = list(query.fetch())

            if len(result) > 0:

                self.ds.delete(result[0].key)

                query = self.ds.query(kind='sessions')
                query.add_filter('cid', '=', int(self.cid))
                sessions = list(query.fetch())
                attendanceRecords = list()
                for session in sessions:
                    query = self.ds.query(kind='attendance_records')
                    query.add_filter('seid', '=', int(session['seid']))
                    attendanceRecords = attendanceRecords + list(query.fetch())
                for attendanceRecord in attendanceRecords:
                    self.ds.delete(attendanceRecord.key)
                return 0
            else:
                # failed because it was not in enrolled_in to begin with
                return -3
        else:
            # invalid uni
            return -1

    def get_sessions(self, single_seid = None):
        if single_seid is None:
            query = self.ds.query(kind='sessions')
            query.add_filter('cid', '=', self.cid)
            results = list(query.fetch())
            return results
        else:
            query = self.ds.query(kind='sessions')
            query.add_filter('cid', '=', self.cid)
            query.add_filter('seid', '=', single_seid)
            results = list(query.fetch())
            return results[0]

    def store_course(self):
        key = self.ds.key('courses', self.cid)
        entity = datastore.Entity(
            key=key)
        entity.update({
            'course_name' : self.course_name,
            'cid' : self.cid,
            })
        self.ds.put(entity)
        return entity