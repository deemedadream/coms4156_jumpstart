import teachers_model
from datetime import datetime, date
from google.cloud import datastore
import logging
import pytest
import flask


class TeacherTestUnits():

	def test_valid_init(self):
		teacher = teachers_model.Teachers(123456)
		assert teacher.tid == 123456

	def test_string_init(self):
		teacher = teachers_model.Teachers("125123")
		assert int(teacher.tid) == 125123

	def test_invalid_string_init(self):
		teacher = teachers_model.Teachers("ab123")		
		assert teacher.tid == "ab123"

	def test_set_tid(self):
		teacher = teachers_model.Teachers(123)
		teacher.tid = 321
		assert teacher.tid == 321

	def test_add_course(self):
		teacher = teachers_model.Teachers(123)
		cid = teacher.add_course('CS1')
		assert cid is not None

	def test_get_courses(self):
		teacher = teachers_model.Teachers(123)
		cid = teacher.add_course('CS1')
		results = teacher.get_courses()
		assert len(results) == 2

	def test_remove_courses(self):
		teacher = teachers_model.Teachers(123)
		results = teacher.get_courses()
		for result in results:
			teacher.remove_course(result['cid'])
		assert len(teacher.get_courses()) == 0