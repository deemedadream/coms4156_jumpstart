from model import Model
from datetime import datetime, date
from google.cloud import datastore
import logging
import sys

class Students(Model):

    def __init__(self, sid):
        self.sid = sid
        self.ds = self.get_client()

    def get_uni(self):
        query = self.ds.query(kind='student')
        query.add_filter('sid', '=', self.sid)
        result = list(query.fetch())
        return result[0]['uni']

    def get_courses(self):
        query = self.ds.query(kind='enrolled_in')
        query.add_filter('sid', '=', self.sid)
        enrolledCourses = list(query.fetch())
        logging.warning("Printing students line 23 ===========================================================================================")
        logging.warning(enrolledCourses)
        result = list()
        courses = list()
        for enrolledCourse in enrolledCourses:
            query = self.ds.query(kind='courses')
            query.add_filter('cid', '=', enrolledCourse['cid'])
            courses = list(query.fetch())
            logging.warning("Printing students line 31 ===========================================================================================")
            logging.warning(courses)
        if courses:
            for course in courses:
                query = self.ds.query(kind='sessions')
                query.add_filter('cid', '=', course['cid'])
                results = list(query.fetch())
                course['window_open'] = results[0]['window_open']
        logging.warning("Printing students line 39 ===========================================================================================")
        logging.warning(courses)
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
        key = self.ds.key('attendance_records')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'seid': int(seid),
            'sid': self.sid, 
            'signed_in': True
        })
        self.ds.put(entity)
        '''query = self.ds.query(kind='attendance_records')
        query.add_filter('seid', '=', int(seid))
        result = list(query.fetch())
        result.update({
            'seid': int(seid),
        })
        self.ds.put(result)'''


    def get_course_attendance(self, cid):
        query = self.ds.query(kind='sessions')
        query.add_filter('cid', '=', int(cid))
        sessions = list(query.fetch())
        results = list()
        for session in sessions:
            query = self.ds.query(kind='attendance_records')
            query.add_filter('seid', '=', session['seid'])
            #query.add_filter('sid', '=', self.sid)
            results = list(query.fetch())
            logging.warning("Printing students line 110 ===========================================================================================")
            logging.warning(cid)
            logging.warning(self.sid)
            logging.warning(session['seid'])
            logging.warning(len(results))
            if results:
                session['signed_in'] = "Signed in"
                #session['message'] = results[0]['message']
            else:
                session['signed_in'] = "Not signed in"
        return sessions

    def get_num_attendance_records(self, cid):
        results = self.get_course_attendance(cid)
        return len(results)
