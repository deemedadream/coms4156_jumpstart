from model import Model
from datetime import datetime, date
from google.cloud import datastore
import logging
import copy
import sys

class Students(Model):

    def __init__(self, sid):
        self.sid = sid
        self.ds = self.get_client()

    def get_uni(self):
        query = self.ds.query(kind='student')
        query.add_filter('sid', '=', self.sid)
        result = list(query.fetch())
        return result[0]['uni'] if result else None

    def get_courses(self):
        """Returns courses the student is enrolled in
        along with whether there is a session window open
        for each course and whether the student is already
        signed in"""

        #Check student's enrollments
        query = self.ds.query(kind='enrolled_in')
        query.add_filter('sid', '=', self.sid)
        enrolledCourses = list(query.fetch())
        attendance_records = list()
        sessions = list()
        courses = list()

        #Retrieve courses student is enrolled in
        for enrolledCourse in enrolledCourses:
            query = self.ds.query(kind='courses')
            query.add_filter('cid', '=', enrolledCourse['cid'])
            courses.extend(list(query.fetch()))
        final = copy.deepcopy(enrolledCourses)

        for course in courses:
            query = self.ds.query(kind='sessions')
            query.add_filter('cid', '=', course['cid'])
            sessions = list(query.fetch())
            course['window_open'] = False
            course['signed_in'] = False
            course['secret_valid'] = None

            #check for open sessions
            for session in sessions:
                if session['window_open']:
                    course['window_open'] = True

                    #check if the student signed in to this open session already
                    query = self.ds.query(kind='attendance_records')
                    query.add_filter('seid', '=', session['seid'])
                    query.add_filter('sid', '=', self.sid)
                    attendance_records = list(query.fetch())
                    if attendance_records:
                        course['signed_in'] = attendance_records[0]['signed_in']
                    break
        return courses

    def get_secret_and_seid(self, cid = None):
        if cid is None:
            cid = -1

        results = list()
        query = self.ds.query(kind='sessions')
        query.add_filter('cid', '=', int(cid))
        query.add_filter('window_open', '=', True)
        sessions = list(query.fetch())
        for session in sessions:
            if session['window_open']==True:
                results.append(session)
        if len(results) == 1:       #Works because open_window() ensures that only one window is open at a time
            secret = results[0]['secret']
            seid = results[0]['seid']
        else:
            secret, seid = None, -1
        return secret, seid

    def has_signed_in(self):
        _, seid = self.get_secret_and_seid()

        if seid == -1:
            return False
        else:
            query = self.ds.query(kind='sessions')
            query.add_filter('seid', '=', int(seid))
            sessions = list(query.fetch())
            results = list()
            for session in sessions:
                query = self.ds.query(kind='attendance_records')
                query.add_filter('seid', '=', int(session['seid']))
                query.add_filter('sid', '=', self.sid)
                results = results + list(query.fetch())
            return True if len(results) == 1 else False

    def insert_attendance_record(self, seid):
        query = self.ds.query(kind='attendance_records')
        query.add_filter('seid', '=', int(seid))
        query.add_filter('sid', '=', self.sid)
        result = list(query.fetch())
        if not result:
            key = self.ds.key('attendance_records')
            entity = datastore.Entity(
                key=key)
            entity.update({
                'seid': int(seid),
                'sid': self.sid,
                'signed_in': False
            })
            self.ds.put(entity)

    def sign_in(self, sid=None, seid=None):
        if sid is None:
            sid = self.sid
        if seid is None:
            seid = self.seid
        query = self.ds.query(kind="attendance_records")
        query.add_filter("sid", "=", sid)
        query.add_filter("seid", "=", seid)
        result = list(query.fetch())
        entity = result[0]
        entity.update({
        'signed_in' : True
        })
        self.ds.put(entity)


    def get_course_attendance(self, cid):
        query = self.ds.query(kind='sessions')
        query.add_filter('cid', '=', int(cid))
        sessions = list(query.fetch())
        results = list()
        for session in sessions:
            query = self.ds.query(kind='attendance_records')
            query.add_filter('seid', '=', session['seid'])
            query.add_filter('sid', '=', self.sid)
            results = list(query.fetch())
            session['signed_in'] = "Not signed in"
            for result in results:
                if result['signed_in']:
                    session['signed_in'] = "Signed in"
        return sessions

    def get_num_attendance_records(self, cid):
        results = self.get_course_attendance(cid)
        num_ar = 0
        for r in results:
            if r['signed_in'] == "Signed in":
                num_ar += 1
        return num_ar
