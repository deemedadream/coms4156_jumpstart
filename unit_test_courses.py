
#import os
#import imhere
#import unittest
#import tempfile
#from flask import session
import logging
import sys
from datetime import date, datetime

import flask
from datetime import date
from models import users_model, index_model, teachers_model, students_model, courses_model, sessions_model, attendance_records_model, model
from google.cloud import datastore

class TestUnits():

    def setup_module(modlule):
        pass

    def test_courses_model(self):
        cm = courses_model.Courses()
        cm.cid = 'ttc2132'
        assert cm.cid == 'ttc2132' 
    
    def test_get_students(self):
        cm = courses_model.Courses(tid = 6554)
        assert cm.tid == 6554
        '''sm = students_model.Students()
        cm.cid = 6546
        cm.add_student("eet3245")
        print("before================================================================================")
        print(cm.get_students())
        assert len(cm.get_students()) <> 0
        #assert ssm.open_session() == ssm.seid
        #assert ssm.date == str(date.today())
        #assert ssm.window_open == False'''

'''
    def setup_method(self, test_sessions_model):
        pass
     
    def test_sessions_model(self):
        ssm = sessions_model.Sessions()
        #assert ssm.open_session() == ssm.seid
        #assert ssm.date == str(date.today())
        #assert ssm.window_open == False

    def test_open_window(self):
        ssm = sessions_model.Sessions()
        assert ssm.window_open == False
        ssm.open_window()
        assert ssm.open_window() == True 
        assert ssm.window_open == True

    def test_close_window(self):
        ssm = sessions_model.Sessions()
        entity = ssm.open_session()
        print("before================================================================================")
        print(ssm.window_open)
        print(entity)
        throwaway = ssm.open_window()
        assert ssm.window_open == True
        assert throwaway == True
        print("After===================================================================================")
        print(ssm.window_open)
        print(throwaway)
        assert ssm.close_window() == False
        print("Close window===================================================================================")
        print(ssm.window_open)
        assert ssm.window_open == False 

    def test_get_secret_code(self):
        ssm = sessions_model.Sessions()
        print(ssm.open_session())
        print(ssm.close_window())
        print("after close================================================================================")
        assert ssm.secret == 0
        assert ssm.get_secret_code() == -1
        print("After================================================================================")
        print(ssm.open_session())
        ssm.close_window()
        ssm.open_window()
        print(ssm.open_window())
        print(ssm.secret)
        assert ssm.secret == ssm.get_secret_code()
        ssm.close_window()
        assert ssm.get_secret_code() == -1'''