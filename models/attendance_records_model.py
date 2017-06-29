import logging

from model import Model
from google.cloud import datastore

class Attendance_Records(Model):

    def __init__(self, sid=-1, seid=-1, signed_in=None, excuse_provided=False):
        if signed_in is None:
            signed_in = False
        self.sid = sid
        self.seid = seid
        self.signed_in = signed_in
        self.excuse_provided = excuse_provided
        self.ds = self.get_client()

    def get_record(self):
        query = self.ds.query(kind="attendance_records")
        query.add_filter("sid", "=", self.sid)
        query.add_filter("seid", "=", self.seid)
        result = list(query.fetch())
        return result[0] if len(result) > 0 else []

    def insert_attendance_record(self):
        key = self.ds.key("attendance_records")
        entity = datastore.Entity(key=key)
        entity.update({
            'sid': int(self.sid),
            'seid': self.seid,
            'signed_in' : False
        })
        self.ds.put(entity)

    def remove_attendance_record(self):
        query = self.ds.query(kind="attendance_records")
        query.add_filter("sid", "=", self.sid)
        query.add_filter("seid", "=", self.seid)
        result = list(query.fetch())
        self.ds.delete_multi([r.key for r in result])

    def get_absences(self):
        query = self.ds.query(kind="attendance_records")
        absences = self.get_records(sid=self.sid,
                                    signed_in=False)
        sessions = []
        for a in absences:
            session = self.get_session(a['seid'])
            if session:
                sessions.append(session)
        return sessions

    def get_records(self, **kwargs):
        query = self.ds.query(kind="attendance_records")
        for attr in kwargs:
            query.add_filter(attr, "=", kwargs[attr])
        result = list(query.fetch())
        return result

    def get_excuse(self):
        query = self.ds.query(kind="excuses")
        query.add_filter("sid", "=", self.sid)
        query.add_filter("seid", "=", self.seid)
        result = list(query.fetch())
        return result[0] if len(result) > 0 else []

    def provide_excuse(self, excuse):
        #check if excuse already exists
        if not self.get_excuse():
            key = self.ds.key("excuses")
            entity = datastore.Entity(key=key)
            entity.update({
                'sid': self.sid,
                'seid': self.seid,
                'excuse': excuse
            })
            self.ds.put(entity)

    def remove_excuse(self):
        query = self.ds.query(kind="excuses")
        query.add_filter("sid", "=", self.sid)
        query.add_filter("seid", "=", self.seid)
        result = list(query.fetch())
        self.ds.delete_multi([r.key for r in result])

    def get_excuses_multi(self, **kwargs):
        query = self.ds.query(kind="excuses")
        if "sid" in kwargs:
            query.add_filter("sid", "=", kwargs["sid"])
        if "seid" in kwargs:
            query.add_filter("seid", "=", kwargs["seid"])
        results = list(query.fetch())
        return results

    def get_session(self, seid):
        query = self.ds.query(kind="sessions")
        query.add_filter("seid", "=", int(seid))
        results = list(query.fetch())
        return results[0] if results else None


