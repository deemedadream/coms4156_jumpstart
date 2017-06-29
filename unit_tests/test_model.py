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

    def setup_module(modlule):
        pass
    
    '''Grey box test - check that datastore query returns and has correct type'''
    def  test_get_client(self):
        ds = model.Model().get_client()
        query = ds.query(kind='courses')
        result = list(query.fetch())
        assert 1 < 2