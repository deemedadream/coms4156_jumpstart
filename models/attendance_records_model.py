from model import Model
from google.cloud import datastore

class Attendance_Records(Model):

    def __init__(self, sid, seid, signed_in=False, excuse_provided=False):
        self.sid = sid
        self.seid = int(seid)
        self.signed_in = signed_in
        self.excuse_provided = excuse_provided
        self.ds = self.get_client()

    def insert_attendance_record(self):
        key = self.ds.key("attendance_records")
        entity = datastore.Entity(key=key)
        entity.update({
            'sid': self.sid,
            'seid': self.seid,
        })
        self.ds.put(entity)

    def remove_attendance_record(self):
        query = self.ds.query(kind="attendance_records")
        query.add_filter("sid", "=", self.sid)
        query.add_filter("seid", "=", self.seid)
        result = list(query.fetch())
        for record in result:
            self.ds.delete(record)

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
        for excuse in result:
            self.ds.delete(excuse)




