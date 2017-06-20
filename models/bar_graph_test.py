import bar_graph_model
from google.cloud import datastore
import pytest
import logging
import flask



class BarGraphTests():


	def create_graph_test(self):
		graph = bar_graph_model.BarGraph()
		assert graph is not None