from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json


class Competition(Resource):

	def __init__(self):
		self.db = Db()

	def get(self):
		query = "select Id as 'id', CompetitionName as 'title', CompetitionSportId as 'cs_id' from Competitions"
		result = self.db.engine.execute(query)
		rows = result.fetchall()
		keys = result.keys()
		data = self.db.clean_select_results(rows, keys)
		return {
				'data': data
			}