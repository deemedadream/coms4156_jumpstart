import logging
import sys
import pytest
import flask
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from datetime import date, datetime
from models.model import Model
from datetime import date
from models import users_model, index_model, teachers_model, students_model, courses_model, sessions_model, attendance_records_model, model
from google.cloud import datastore

class TestUnits(Model):

    def upper_bound_course_entity(self):
        ds = model.Model().get_client()
        key = ds.key('courses')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'course_name': 'EENG6778',
            'cid': 99999999
        })
        ds.put(entity)
        key_id = int(entity.key.id)
        return key_id

    def lower_bound_course_entity(self):
        ds = model.Model().get_client()
        key = ds.key('courses')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'course_name': '',
            'cid': 0
        })
        return entity
        
    def upper_bound_course_model(self):
        cm = courses_model.Courses()
      
    def delete_course(self, del_cid):
        ds = model.Model().get_client()
        key = ds.key('courses', int(del_cid))
        ds.delete(key)
        
    def delete_enrolled(self, del_cid):
        ds = model.Model().get_client()
        query = ds.query(kind='enrolled')
        query.add_filter('cid', '=', int(del_cid))
        results = list(query.fetch())
        for i in range(0, len(results)):
            key = ds.key(resutls[i])
            ds.delete(key)
    
    '''Blackbox tests lower bounds'''
    
    def test_courses_model_constructor(self):
        cm = courses_model.Courses(0)
        assert cm.cid == 0
        assert cm.course_name == ""
    
    def test_courses_model_constructor_no_cid(self):
        cm = courses_model.Courses()
        cm.cid = 0
        assert cm.cid == 0
        assert cm.course_name == ""        
        
        '''Blackbox tests upper bounds'''
    
    def test_courses_model_constructor(self):
        cm = courses_model.Courses(99999999)
        assert cm.cid == 99999999
        assert cm.course_name == ""
    
    def test_courses_model_constructor_no_cid(self):
        cm = courses_model.Courses()
        cm.cid = 99999999
        assert cm.cid == 99999999
        assert cm.course_name == ""   
        
        '''Greybox tests'''
    
    def test_get_students(self):
        key_id = self.upper_bound_course_entity()
        ds = model.Model().get_client()
        cm = courses_model.Courses()
        assert len(cm.get_students()) == 0
        key = ds.key('enrolled_in')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'sid' : 653,
            'cid' : 99999999
            })
        ds.put(entity)
        key = ds.key('user')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'id' : 653,
            })
        ds.put(entity)
        assert len(cm.get_students(99999999)) > 0
        self.delete_course(key_id)
    
    def test_get_students_sids(self):
        key_id = self.upper_bound_course_entity()
        ds = model.Model().get_client()
        cm = courses_model.Courses()
        assert len(cm.get_students()) == 0
        key = ds.key('enrolled_in')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'sid' : 653,
            'cid' : 99999999
            })
        ds.put(entity)
        assert len(cm.get_students(99999999)) > 0
        self.delete_course(key_id)
    
    '''def test_add_student(self):
        ds = model.Model().get_client()
        cm = courses_model.Courses()
        assert cm.add_student('adsfas') == -1 #an invalid uni
        key = ds.key('student')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'uni' : 'ttc2132',
            'sid' : 99999999
            })
        ds.put(entity)
        key_id = int(entity.key.id)
        cm.cid = 99999999
        assert cm.add_student('ttc2132') == 0   #not enrolled
        assert cm.add_student('ttc2132') == -2  #already enrolled
        key = ds.key('student', key_id)
        ds.delete(key)
        self.delete_enrolled(99999999) 
        cm.remove_student('ttc2132')'''
        
 