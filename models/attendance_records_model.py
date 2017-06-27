from model import Model
from google.cloud import datastore

class Attendance_Records(Model):

    def __init__(self, sid, seid, signed_in=None, excuse_provided=False):
        if signed_in is None:
            signed_in = False
        self.sid = int(sid)
        self.seid = int(seid)
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
        self.ds.delete_multi(result)

    def get_excuse(self):
        query = self.ds.query(kind="excuses")
        query.add_filter("sid", "=", self.sid)
        query.add_filter("seid", "=", self.seid)
        result = list(query.fetch())
        return result[0] if len(result) > 0 else []

    def provide_excuse(self, excuse):
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
        self.ds.delete_multi(result)
