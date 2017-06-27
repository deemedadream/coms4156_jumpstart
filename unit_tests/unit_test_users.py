from models import users_model
from google.cloud import datastore
import pytest
import logging
import flask
from model import Model

class Unit_Test_Users(Model):

	@pytest.fixture(scope='module')
	def user(self):
		ds = self.get_client()
		key = self.ds.key('user')
		user = datastore.entity(
			key=key
		)
		user.update({
		'id': 1234567898765432
		'email' : 'test@test.org'
		'family_name' : 'Last'
		'given_name' : 'First'
		'verified_email' : True
		})
		ds.put(user)
		return user


	def create_user_test(self):
		user = users_model.Users()
		assert user is not None

	def test_get_user(self, user):
		user = users_model.Users()
		uid = user.get_or_create_user(user):
		assert uid = 1234567898765432

	def is_valid_uni_test(self):
		assert users_model.is_valid_uni('jak2270') == True
