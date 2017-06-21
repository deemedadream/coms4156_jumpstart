from model import Model
from datetime import date, datetime
from random import randint
from google.cloud import datastore
import logging
import sys

class Sessions(Model):

    def __init__(self):
        self.seid = -1
        self.cid = -1
        self.date = 'blank'
        self.ds = self.get_client()
        self.window_open = False
        self.secret = -1

    def open_session(self, new_cid = None):
        if new_cid is None:
            new_cid = self.cid  
        #find or create session
        query = self.ds.query(kind='sessions')
        #query.add_filter('date', '=', self.date)
        query.add_filter('cid', '=', int(new_cid))
        #query.add_filter('secret', '>', -1)
        result = list(query.fetch())
        if not result:
            self.cid = new_cid
            key = self.ds.key('sessions')
            entity = datastore.Entity(
                key=key)
            entity.update({
                'seid' : -1,
                'cid' : int(new_cid),
                'date' : self.date,
                'window_open' : False,
                'secret' : -1
            })
            self.ds.put(entity)
            self.seid = int(entity.key.id)
            entity.update({
                'seid' : int(self.seid)
            })
            self.ds.put(entity)
            return self.seid

        elif result[0]['seid'] > -1 and result[0]['cid'] > -1 and result[0]['date'] == 'blank':
            key = self.ds.key('sessions', result[0]['seid'])
            entity = datastore.Entity(
                key=key)
            entity.update({
                'seid' : result[0]['seid'],
                'cid' : result[0]['cid'],
                'window_open' : False,
                'secret' : result[0]['secret'],
                'date' : str(date.today()),
            })
            self.ds.put(entity)
            return result[0]['seid']
            #result[0]['date']=str(date.today())

        else:
            self.seid = result[0]['seid']
            self.cid = result[0]['cid']
            self.date = result[0]['date']
            self.window_open = result[0]['window_open']
            self.secret = result[0]['secret']
            return result[0]['seid']

    def open_window(self, seid):
        '''Opens a session for this course
        and returns the secret code for that session.
        '''
        self.date = str(date.today())
        query = self.ds.query(kind='sessions')
        query.add_filter('seid', '=', seid)
        result = list(query.fetch())
        entity = result[0]
        if result[0]['window_open'] == True:
            return True
        #entity = self.open_session(self.cid)
        # auto-generated secret code for now
        randsecret = randint(1000, 9999)
        self.secret = int(randsecret)
        entity.update({
            'window_open' : True,
            'secret': int(self.secret),
            'date' : self.date
        })
        self.ds.put(entity)
        query = self.ds.query(kind='sessions')
        query.add_filter('date', '=', self.date)
        result = list(query.fetch())
        self.window_open = result[0]['window_open']
        return result[0]['window_open']


    def close_window(self, close_seid = None):
        if close_seid is None:
            close_seid = self.seid                #close window for this section if no seid  passed
        query = self.ds.query(kind='sessions')    #find session
        query.add_filter('seid', '=', close_seid)
        result = list(query.fetch())
        entity = result[0]
        if (entity['window_open'] == True):
            entity.update({
            'window_open' : False,
            'secret' : -1
            })
            self.ds.put(entity)
        else:
             pass
        query = self.ds.query(kind='sessions')
        query.add_filter('seid', '=', self.seid)
        result = list(query.fetch())
        self.window_open = result[0]['window_open']
        self.secret = result[0]['secret']
        return result[0]['window_open']


    def get_secret_code(self):
        self.open_session(self.cid)
        if self.window_open:
            return self.secret
        else:
            return -1

    def get_current_roster_size(self):
        return 0

    def store_session(self):
        key = self.ds.key('sessions', self.seid)
        entity = datastore.Entity(
            key=key)
        entity.update({
            'seid' : self.seid,
            'cid' : self.cid,
            'date' : self.date,
            'window_open' : self.window_open,
            'secret' : -self.secret
            })
        self.ds.put(entity)