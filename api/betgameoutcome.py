from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json


class BetGameOutcome(Resource):

	def __init__(self):
		self.db = Db()

	def get(self):
		query = "select Id as 'id', BetGameOutcomeShortName as 'title', BetGameOutcomeSportId, BetGameId from BetGameOutcomes"
		result = self.db.engine.execute(query)
		rows = result.fetchall()
		keys = result.keys()
		data = self.db.clean_select_results(rows, keys)
		return {
				'data': data
			}

  
