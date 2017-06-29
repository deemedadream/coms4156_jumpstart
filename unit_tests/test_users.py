import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from models import users_model
from models.model import Model
from google.cloud import datastore
import pytest
import logging
import flask

class Test_Users(Model):

	@pytest.fixture(scope='module')
	def user(self):
		self.ds = self.get_client()
		key = self.ds.key('user')
		user = datastore.Entity(
			key=key
		)
		user.update({
		'id': 1234567898765432,
		'email' : 'test@test.org',
		'family_name' : 'Last',
		'given_name' : 'First',
		'verified_email' : True,
		})
		self.ds.put(user)
		return user


	def create_user_test(self):
		user = users_model.Users()
		assert user is not None

	def test_get_user(self, user):
		uid = users_model.Users().get_or_create_user(user)
		assert uid == 1234567898765432

	def is_valid_uni_test(self):
		assert users_model.is_valid_uni('jak2270') == True
