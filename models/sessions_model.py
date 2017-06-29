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
        else:
            self.cid = new_cid
        #find or create session
        today = str(date.today())
        query = self.ds.query(kind='sessions')
        query.add_filter('cid', '=', int(new_cid))
        query.add_filter('date', '=', today)
        result = list(query.fetch())
        #If no sessions with today's date, create one. 
        if not result:
            #if there isn't, upsert a blank dated session
            #upsert because we don't want the database flooded with
            #blank sessions
            self.cid = new_cid
            key = self.ds.key('sessions', date=self.date)
            entity = datastore.Entity(
                key=key)
            entity.update({
                'seid' : -1,
                'cid' : int(new_cid),
                'date' : today,
                'window_open' : False,
                'secret' : -1
            })
            self.ds.put(entity)
            self.seid = int(entity.key.id)
            entity.update({
                'seid' : int(self.seid)
            })
            self.ds.put(entity)            
        else:
            self.seid = result[0]['seid']
            self.cid = result[0]['cid']
            self.date = result[0]['date']
            self.window_open = result[0]['window_open']
            self.secret = result[0]['secret']
        return self.seid

    def open_window(self, seid = None):
        if seid is None:
            seid = self.seid
        self.date = str(date.today())
        query = self.ds.query(kind='sessions')
        query.add_filter('seid', '=', seid)
        result = list(query.fetch())
        if result:
            entity = result[0]
        
        #Close the windows of old sessions
        query = self.ds.query(kind='sessions')
        query.add_filter('cid', '=', entity['cid'])
        old_sessions = list(query.fetch())
        if old_sessions:
            for session in old_sessions:
                self.close_window(session['seid'])

        # auto-generate secret code and open the windoww
        randsecret = randint(1000, 9999)
        self.secret = int(randsecret)
        entity.update({
            'window_open': True,
            'secret': int(self.secret),
            'date' : self.date
        })
        self.ds.put(entity)
        #return confirmed window status from db
        query = self.ds.query(kind='sessions')
        query.add_filter('seid', '=', seid)
        result = list(query.fetch())
        if result:
            self.window_open = result[0]['window_open']
            return result[0]['window_open']
        else:
            return False

    def close_window(self, close_seid = None):
        if close_seid is None:
            close_seid = self.seid                #close window for this section if no seid  passed
        query = self.ds.query(kind='sessions')    #find session
        query.add_filter('seid', '=', close_seid)
        result = list(query.fetch())
        if result:
            entity = result[0]
            if (entity['window_open'] == True):
                entity.update({
                'window_open' : False,
                'secret' : -1
                })
                self.ds.put(entity)
            else:
                 return False
            #return confirmed window status from db
            query = self.ds.query(kind='sessions')
            query.add_filter('seid', '=', close_seid)
            result = list(query.fetch())
            if result:
                self.window_open = result[0]['window_open']
                self.secret = result[0]['secret']
                return result[0]['window_open']
        else:
            return False

    def get_secret_code(self):
        self.open_session(self.cid)
        self.open_window()
        if self.window_open:
            return self.secret
        else:
            return -1

    def get_current_roster_size(self, seid_count = None):
        if seid_count is None:
            seid_count = self.seid
        query = self.ds.query(kind='attendance_records')
        query.add_filter('seid', '=', seid_count)
        result = list(query.fetch())
        roster_size = len(result)
        return roster_size

    def get_attendance_count(self, seid_count = None):
        if seid_count is None:
            seid_count = self.seid
        query = self.ds.query(kind='attendance_records')
        query.add_filter('seid', '=', seid_count)
        query.add_filter('signed_in', '=', True)
        result = list(query.fetch())
        attendance_count = len(result)
        return attendance_count

    def store_session(self):
        key = self.ds.key('sessions', self.seid)
        entity = datastore.Entity(
            key=key)
        entity.update({
            'seid' : self.seid,
            'cid' : self.cid,
            'date' : self.date,
            'window_open' : self.window_open,
            'secret' : self.secret
            })
        self.ds.put(entity)