from model import Model 
from datetime import datetime, date
from google.cloud import datastore
import sessions_model
import logging
import sys

class Teachers(Model):

    def __init__(self, tid):
        self.tid = tid
        self.now = datetime.now()
        self.today = datetime.today()
        self.ds = self.get_client()

    def get_courses(self):
        query = self.ds.query(kind='teaches')
        query.add_filter('tid', '=', self.tid)
        teaches = list(query.fetch())
        results = list()
        for teach in teaches:
            query = self.ds.query(kind='courses')
            query.add_filter('cid', '=', teach['cid'])
            results = results + list(query.fetch())
        return results

    def get_courses_with_session(self):
        query = self.ds.query(kind='teaches')
        query.add_filter('tid', '=', self.tid)
        teaches = list(query.fetch())
        courses = list()
        for teach in teaches:
            query = self.ds.query(kind='courses')
            query.add_filter('cid', '=', teach['cid'])
            courses = courses + list(query.fetch())
        for course in courses:
            course['active'] = 0
            query = self.ds.query(kind='sessions')
            query.add_filter('cid', '=', course['cid'])
            query.add_filter('date', '=', str(date.today()))
            sessions = list(query.fetch())
            for session in sessions:
                if session['window_open'] == True:
                    course['active'] = 1
                    course['secret'] = session['secret']
                    break
        return courses

    def get_course(self, course_name=None, cid=None):
        query = self.ds.query(kind='courses')
        if course_name:
            query.add_filter('name', '=', course_name)
        if cid:
            query.add_filter('cid', '=', cid)
        result = list(query.fetch())
        return result[0] if result else None

    def add_course(self, course_name):
        old_course = self.get_course(course_name=course_name)
        
        #If a course of the same name doesn't already exist create one
        if not old_course:
            key = self.ds.key('courses')
            entity = datastore.Entity(
                key=key)
            entity.update({
                'name': course_name
            })
            self.ds.put(entity)
            cid = entity.key.id
            entity.update({
                'cid': cid
            })
            self.ds.put(entity)
        else:
            #Check if existing course is already taught; if so return -1
            cid = int(old_course['cid'])
            query = self.ds.query(kind='teaches')
            query.add_filter('cid', '=', cid)
            query.add_filter('tid', '=', self.tid)
            teaches = list(query.fetch())
            if teaches:
                return -1
            
        key = self.ds.key('teaches')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'tid': self.tid,
            'cid': cid
        })
        self.ds.put(entity)
        return cid

    def remove_course(self, cid):
        key = self.ds.key('courses', int(cid))
        self.ds.delete(key)

        # remove course from students' enrolled list
        query = self.ds.query(kind='enrolled_in')
        query.add_filter('cid', '=', int(cid))
        results = list(query.fetch())
        for result in results:
            self.ds.delete(result.key)
