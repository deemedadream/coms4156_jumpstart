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

        #If there are courses, check whether there are active sessions and student is signed in
        #right now, only checks if first session in the past sessions is open; what if that is not
        #the latest session? Also if there are multiple sessions, sets course[signed_in] to the
        #signed_in status of the attendance of the student on the last session in the result.
        #What we want is to set window_open and signed_in to the values of the latest session and 
        #attendance record for that session. Also we may want to write a restriction where only one session
        #can be open at a time for a course.
        for course in courses:
            query = self.ds.query(kind='sessions')
            query.add_filter('cid', '=', course['cid'])
            sessions = list(query.fetch())
            logging.warning(sessions)
            course['window_open'] = False
            course['signed_in'] = False

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
        '''query = self.ds.query(kind='enrolled_in')
#        query.add_filter('sid', '=', int(self.sid))
        enrolled_in = list(query.fetch())'''
        logging.warning("Printing students line 49 ===========================================================================================")
        logging.warning(cid)
        results = list()
        #for enrolled in enrolled_in:
        query = self.ds.query(kind='sessions')
        query.add_filter('cid', '=', int(cid))
        query.add_filter('window_open', '=', True)
        sessions = list(query.fetch())
        for session in sessions:
            if session['window_open']==True:
                results.append(session)
            # results = results + list(query.fetch())
        logging.warning("Printing students line 61 ===========================================================================================")
        logging.warning(results)
        if len(results) == 1:
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
        logging.warning("Printing students line 112 ===========================================================================================")
        logging.warning(seid)
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
            logging.warning("Printing students line 110 ===========================================================================================")
            #logging.warning(cid)
            logging.warning(self.sid)
            #logging.warning(session['seid'])
            #logging.warning(len(results))
            session['signed_in'] = "Not signed in"
            for result in results:
                if result['signed_in']:
                    session['signed_in'] = "Signed in"
        return sessions


    #need to make more efficient
    def get_num_attendance_records(self, cid):
        results = self.get_course_attendance(cid)
        num_ar = 0
        for r in results:
            if r['signed_in'] == "Signed in":
                num_ar += 1
        return num_ar
