
#import os
#import imhere
#import unittest
#import tempfile
#from flask import session
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from datetime import date, datetime
from models.model import Model

import flask
from datetime import date
from models import users_model, index_model, teachers_model, students_model, courses_model, sessions_model, attendance_records_model, model
from google.cloud import datastore

class TestUnits(Model):
    
    def setup_method(self, test_sessions_model):
        pass
        
    ''' mock data'''
    def upper_partition_course_entity(self):
        ds = model.Model().get_client()
        key = ds.key('courses')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'name': "Strings123"
        })
        ds.put(entity)
        cid = int(entity.key.id)
        entity.update({
            'name': "Strings123",
            'cid' : int(cid)
        })
        ds.put(entity)
        return entity
    
    def upper_partition_session_entity(self):
        ds = model.Model().get_client()
        key = ds.key('sessions')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'date': str(date.today()),
            'cid': 99999999,
            'window_open' : False,
            'self.secret' : -1
        })
        ds.put(entity)
        seid = int(entity.key.id)
        entity.update({
            'date': str(date.today()),
            'cid': 99999999,
            'window_open' : False,
            'self.secret' : -1,
            'seid' : int(seid)
        })
        ds.put(entity)
        return entity

    def lower_partition_session_entity(self):
        ds = model.Model().get_client()
        key = ds.key('sessions')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'date': '',
            'cid': 99999999,
            'window_open' : False,
            'self.secret' : -1
        })
        ds.put(entity)
        seid = int(entity.key.id)
        entity.update({
            'date': '',
            'cid': 99999999,
            'window_open' : False,
            'self.secret' : -1,
            'seid' : int(seid)
        })
        ds.put(entity)
        return entity
    
    def delete_session(self, del_seid):
        ds = model.Model().get_client()
        query = ds.query(kind='sessions')
        query.add_filter('seid', '=', int(del_seid))
        results = list(query.fetch())
        for result in results:
            key = ds.key('sessions', int(del_seid))
            ds.delete(key)
        
    
    def test_sessions_model_constructor(self):
        ssm = sessions_model.Sessions()
        assert ssm.seid == -1
        assert ssm.window_open == False
        assert ssm.cid == -1
        assert ssm.date == 'blank'
        assert ssm.secret == -1
        
    def test_print(self):
        ds = model.Model().get_client()
        query = ds.query(kind='sessions')
        #query.add_filter('date', '=', self.date)
        #query.add_filter('cid', '=', 68)
        result = list(query.fetch())
        print('\n' + 'Sessions =================================================================================================')
        for session in result:
            print(session)
                
    def test_open_session_with_cid_arg(self):
        self.ds = self.get_client()
        ssm = sessions_model.Sessions()
        ssm.date = str(date.today())
        cid = self.upper_partition_course_entity()['cid']
        seid = ssm.open_session(cid)
        assert ssm.cid == cid
        self.delete_session(seid)
        
    def test_open_window(self):
        ssm = sessions_model.Sessions()
        cid = self.upper_partition_course_entity()['cid']
        seid = ssm.open_session(cid)
        assert ssm.seid <> -1
        assert ssm.window_open == False
        ssm.open_window()
        assert ssm.open_window() == True 
        assert ssm.window_open == True
        self.ds = self.get_client()
        query = self.ds.query(kind='sessions')
        query.add_filter('cid', '=', cid)
        result = list(query.fetch())
        assert result[0]['secret'] <> -1         #opening window changes the secret
        self.delete_session(seid)

    def test_close_window1(self):
        session = self.lower_partition_session_entity()
        ssm = sessions_model.Sessions()
        ssm.open_session(session['cid'])
        ssm.open_window()
        assert ssm.window_open == True
        assert ssm.close_window() == False 
        assert ssm.window_open == False 
        self.delete_session(session['seid'])
    
    def test_close_window2(self):
        session = self.upper_partition_session_entity()
        ssm = sessions_model.Sessions()
        ssm.open_session(session['cid'])
        ssm.open_window()
        assert ssm.window_open == True
        assert ssm.close_window() == False 
        assert ssm.window_open == False 
        self.delete_session(session['seid'])
    
        
    def test_get_current_roster_size(self):
        ssm = sessions_model.Sessions()
        cid = self.upper_partition_course_entity()['cid']
        seid = ssm.open_session(cid)
        assert ssm.get_current_roster_size() == 0
        ds = model.Model().get_client()
        key = ds.key('enrolled_in')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'sid' : 653,
            'cid' : cid
            })
        ds.put(entity)
        assert ssm.get_current_roster_size() == 1
        self.delete_session(seid)
        


        

