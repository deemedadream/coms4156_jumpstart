import logging
import sys
import pytest
import flask

from datetime import date, datetime
from models.model import Model
from datetime import date
from models import users_model, index_model, teachers_model, students_model, courses_model, sessions_model, attendance_records_model, model
from google.cloud import datastore

class TestUnits(Model):

    @pytest.fixture(scope="module")
    def ds():
        ds = model.Model().get_client()
        return ds
        
    ''' mock data'''
    def upper_bound_course_entity(self):
        ds = model.Model().get_client()
        key = ds.key('courses')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'course_name': 'EENG6778',
            'cid': 99999999
        })
        return entity

    def ulower_bound_course_entity(self):
        ds = model.Model().get_client()
        key = ds.key('courses')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'course_name': '',
            'cid': 0
        })
        return entity
        
    def upper_bound_course_model(self)
        cm = courses_model.Courses()
        
    
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
        
    '''Blackbox tests main equivalence class'''
    
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
        ds = model.Model().get_client()
        cm = courses_model.Courses()
        assert self.upper_bound_course_entity() == 5
    
    
    def test_store_course(self, cid = None, course_name = None):
        ds = model.Model().get_client()
        if cid is None:
            cm = courses_model.Courses()   #cid is not given
        else:
            cm = courses_model.Courses(cid)
        if course_name is None:
            cm.course_name = 'COMS4111'
        else:
            cm.course_name = course_name
        cm.store_course()
        query = ds.query(kind='courses')
        query.add_filter('cid', '=', cm.cid)
        query.add_filter('course_name', '=', cm.course_name)
        results = list(query.fetch())
        assert len(results) == 1      #only one copy stored
        assert cm.store_course() == results[0]  #query finds the copy
    
    def test_store_course_lower_bound_cid(self):
        self.test_store_course(1)          
    
    def test_store_course_lower_bound_cid(self):
        self.test_store_course(99999999)   
    
 