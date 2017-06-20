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
        logging.basicConfig(filename='example.log',level=logging.DEBUG)
        #logging.info("printing")
        #logging.critical("printing")
        #logging.warning("printing")

    def open_session(self, new_cid = None):
        if new_cid is None:
            new_cid = self.cid  
        #find or create session
        query = self.ds.query(kind='sessions')
        #query.add_filter('date', '=', self.date)
        query.add_filter('cid', '=', new_cid)
        #query.add_filter('secret', '>', -1)
        result = list(query.fetch())
        logging.warning("printing sessions_model at line 31================================================================================")
        logging.warning(result)
        if not result:
            logging.warning("printing sessions_model at line 34================================================================================")
            logging.warning(self.seid)
            self.cid = new_cid
            key = self.ds.key('sessions')
            entity = datastore.Entity(
                key=key)
            entity.update({
                'seid' : -1,
                'cid' : new_cid,
                'date' : self.date,
                'window_open' : False,
                'secret' : -1
            })
            self.ds.put(entity)
            self.seid = entity.key.id
            entity.update({
                'seid' : self.seid
            })
            logging.warning("printing sessions_model at line 52================================================================================")
            logging.warning(entity)
            self.ds.put(entity)
            return entity

        elif int(result[0]['seid']) > -1 and int(result[0]['cid']) > -1 and str(result[0]['date']) == 'blank':
            key = self.ds.key('sessions', result[0]['seid'])
            entity = datastore.Entity(
                key=key)
            entity.update({
                'date' : self.date,
            })
            self.ds.put(entity)
            logging.warning("printing sessions_model at line 64================================================================================")
            logging.warning(entity)
            return entity
            #result[0]['date']=str(date.today())

        else:
            self.seid = result[0]['seid']
            self.cid = result[0]['cid']
            self.date = result[0]['date']
            self.window_open = result[0]['window_open']
            self.secret = result[0]['secret']
            logging.warning("OLD SESSION sessions line 74================================================================================")
            logging.warning(result)
            return result[0]

    def open_window(self):
        '''Opens a session for this course
        and returns the secret code for that session.
        '''
        self.date = str(date.today())
        logging.warning("printing sessions_model at line 67================================================================================")
        logging.warning(self.seid)
        query = self.ds.query(kind='sessions')
        query.add_filter('seid', '=', self.seid)
        result = list(query.fetch())
        logging.warning("printing sessions_model at line 72================================================================================")
        logging.warning(result)
        entity = result[0]
        #entity = self.open_session(self.cid)
        # auto-generated secret code for now
        randsecret = randint(1000, 9999)
        self.secret = int(randsecret)
        entity.update({
            'window_open' : True,
            'secret': self.secret,
            'date' : self.date
        })
        logging.warning("printing sessions_model at line 81================================================================================")
        logging.warning(entity)
        self.ds.put(entity)
        query = self.ds.query(kind='sessions')
        query.add_filter('seid', '=', self.seid)
        result = list(query.fetch())
        logging.warning("printing sessions_model at line 87================================================================================")
        logging.warning(result)
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