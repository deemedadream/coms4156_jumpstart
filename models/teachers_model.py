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
        logging.warning("printing teachers line 30================================================================================")
        logging.warning(teaches)
        courses = list()
        for teach in teaches:
            query = self.ds.query(kind='courses')
            query.add_filter('cid', '=', teach['cid'])
            courses = courses + list(query.fetch())
        logging.warning("printing teachers line 37================================================================================")
        logging.warning(courses)
        results = list()
        for course in courses:
            logging.warning("printing teachers line 44================================================================================")
            logging.warning(course['cid'])
            ssm = sessions_model.Sessions()
            ssm.open_session(course['cid'])
            query = self.ds.query(kind='sessions')
            query.add_filter('cid', '=', course['cid'])
            sessions = list(query.fetch())
            logging.warning("printing teachers line 49================================================================================")
            logging.warning(sessions)
            for session in sessions:
                logging.warning("printing teachers_model at line 50================================================================================")
                logging.warning(session)
                if session['window_open'] == True:
                    course['active'] = 1
                    course['secret'] = sessions[0]['secret']
                    logging.warning("printing teachers_model at line 56================================================================================")
                    logging.warning('active')
                else:
                    course['active'] = 0
                    #results.append(session)
                    course['secret'] = sessions[0]['secret']
                    logging.warning("printing teachers_model at line 61================================================================================")
                    logging.warning('inactive')
            logging.warning("printing teachers_model at line 53================================================================================")
            logging.warning(course)
        # result = courses + sessions
        logging.warning("printing teachers_model at line 66================================================================================")
        logging.warning(courses)
        return courses


    def add_course(self, course_name):
        key = self.ds.key('courses')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'name': course_name
        })
        self.ds.put(entity)
        cid = entity.key.id
        logging.warning("printing teachers_model at line 66================================================================================")
        logging.warning(cid)
        entity.update({
            'cid': cid
        })
        self.ds.put(entity)

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
