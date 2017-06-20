import users_model
from google.cloud import datastore
import pytest
import logging
import flask

class UsersTestUnits():

	def create_user_test(self):
		user = users_model.Users()
		assert user is not None
	def is_valid_uni_test(self):
		
		assert users_model.is_valid_uni('jak2270') == False


