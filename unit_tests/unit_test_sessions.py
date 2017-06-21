
#import os
#import imhere
#import unittest
#import tempfile
#from flask import session
import logging
import sys
from datetime import date, datetime
from models.model import Model

import flask
from datetime import date
from models import users_model, index_model, teachers_model, students_model, courses_model, sessions_model, attendance_records_model, model
from google.cloud import datastore

class TestUnits(Model):
    
    @pytest.fixture(scope="module")
    def ds():
        ds = model.Model().get_client()
        return ds

    ''' mock data'''
    def upper_partition_session_entity(self):
        ds = model.Model().get_client()
        key = ds.key('sessions')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'date': str(date.today()),
            'seid': 99999999
        })
        return entity

    def lower_partition_session_entity1(self):
        ds = model.Model().get_client()
        key = ds.key('sessions')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'seid': -1,
            'date': ''
        })
        return entity
    
    def lower_partition_session_entity2(self):
        ds = model.Model().get_client()
        key = ds.key('courses')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'seid': None
            'date': ''
        })
        return entity
        
        '''Blackbox tests lower bounds'''
    
    def test_sessions_model_constructor(self):
        ssm = sessions_model.Sessions(0)
        assert ssm.seid == 0
        assert ssm.window_open == False
    
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

    def setup_method(self, test_sessions_model):
        pass
     
    def test_open_session(self):
        self.ds = self.get_client()
        cm = courses_model.Courses()
        cm.cid = 5231292
        ssm = sessions_model.Sessions()
        ssm.open_session(5231292)
        ssm.open_window()
        print(ssm.secret)
        assert ssm.cid == 5231292
        query = self.ds.query(kind='courses')
        query.add_filter('cid', '=', 5231292)
        result = list(query.fetch())
        assert ssm.date == str(date.today())  #opening session sets date to today
        assert ssm.window_open == False       #window stays closed

        '''Greybox tests - retrieve from datastore'''
    def test_open_window(self):
        ssm = sessions_model.Sessions()
        assert ssm.window_open == False
        ssm.open_window()
        ssm.open_session(55)
        assert ssm.open_window() == True 
        assert ssm.window_open == True
        self.ds = self.get_client()
        query = self.ds.query(kind='sessions')
        query.add_filter('cid', '=', 55)
        result = list(query.fetch())
        assert result[0]['secret'] <> -1         #opening window changes the secret

    def test_close_window1(self, ds):
        entity = self.upper_partition_session_entity()
        entity = lower_partition_session_entity1(self)
        ssm = sessions_model.Sessions()
        ssm.open_window()
        assert ssm.window_open == True
        assert ssm.close_window() == False 
        assert ssm.window_open == False 
    
    def test_close_window1(self, ds):
        entity = self.lower_partition_session_entity1()
        throwaway = ssm.open_window()
        assert ssm.window_open == True
        assert throwaway == True
        assert ssm.close_window() == False 
        assert ssm.window_open == False 
    
    def test_close_window2(self, ds):
        entity = lower_partition_session_entity2(self)
        ssm = sessions_model.Sessions()
        ssm.open_window()
        assert ssm.window_open == True
        assert ssm.close_window() == False 
        assert ssm.window_open == False 
        
    def test_close_window3(self, ds):
        ssm = sessions_model.Sessions()
        entity = lower_partition_session_entity1(self)
        ssm = sessions_model.Sessions()
        ssm.open_window()
        assert ssm.window_open == True
        assert throwaway == True
        assert ssm.close_window() == False 
        assert ssm.window_open == False 

    def test_get_current_roster_size(self, ds)
        ssm = sessions_model.Sessions()
        assert ssm.get_current_roster_size() == 0
        key = self.ds.key('student')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'sid' : 654,
            'secret' : -self.secret
            })
        self.ds.put(entity)
        assert ssm.get_current_roster_size() == 1
        
    def test_get_secret_code(self):
        ssm = sessions_model.Sessions()
        assert ssm.secret == 0
        assert ssm.get_secret_code() == -1
        ssm.close_window()
        ssm.open_window()
        print(ssm.open_window())
        print(ssm.secret)
        assert ssm.secret == ssm.get_secret_code()
        ssm.close_window()
        assert ssm.get_secret_code() == -1
