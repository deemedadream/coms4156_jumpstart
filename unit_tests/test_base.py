import sys
import os
import unittest
import logging

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from models import model as m 
from google.cloud import datastore

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.ds = m.Model().get_client()
        self.context = {}

    def tearDown(self):
        for key in self.context:
            for instance in self.context[key]:
                if not self.destroy_model(key, **instance):
                    logging.warning("Unable to delete {}: {}".format(key, str(instance)))
    
    def get_model(self, model, **kwargs):
        query = self.ds.query(kind=model)
        for attr in kwargs:
            query.add_filter(attr, '=', kwargs[attr])
        result = list(query.fetch())
        return result[0] if result else None

    def store_context(self, model, **kwargs):
        if model not in self.context:
            self.context[model] = []
        self.context[model].append(kwargs)

    def store_model(self, model, **kwargs):
        key = self.ds.key(model)
        entity = datastore.Entity(
            key=key
            )
        entity.update(**kwargs)
        self.ds.put(entity)

        #record the attributes of what we stored in the context
        #so tearDown removes it later
        if model not in self.context:
            self.context[model] = []
        self.context[model].append(kwargs)

        return kwargs

    def destroy_model(self, model, **kwargs):
        query = self.ds.query(kind=model)
        for attr in kwargs:
            query.add_filter(attr, '=', kwargs[attr])
        result = list(query.fetch())
        if result:
            self.ds.delete_multi([r.key for r in result])
            return True
        return False