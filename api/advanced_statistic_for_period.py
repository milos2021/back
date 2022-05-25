from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json


class AdvancedStatisticForPeriod(Resource):

	def __init__(self):
		self.db = Db()

	@staticmethod
	def noneEncapsulator(arg):
		return float(0) if not arg else float(arg)

	def post(self):
		data = request.get_json(force=True)
		sportId = data['sportId']
		betGameId = data['betGameId']
		betGameOutcomeId = data['betGameOutcomeId']
		competitionId = data['competitionId']
		monthFrom = data['monthFrom']
		monthTo = data['monthTo']
		slipType = data['slipType']
		if slipType == 4:
			slipType = 0
		
		#aspects:
		#1 - day
		#2 - month
		#3 - year
		with self.db.engine.begin() as conn:
			podaci = []
			result = conn.execute(
			'exec dbo.m_UserInOutStatisticPerPeriod @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @sportId='+("NULL" if not sportId else str(sportId))+', @betGameOutcomeId='+("NULL" if not betGameOutcomeId else str(betGameOutcomeId))+', @betGameId='+("NULL" if not betGameId else str(betGameId))+', @slipType='+("NULL" if not slipType and slipType!=0 else str(slipType))+', @competitionId='+("NULL" if not competitionId else str(competitionId)))
			for row in result:
				podaci.append({
				'UserName':row['UserName'],
				'BrojTiketaBet':self.noneEncapsulator(row['Broj Tiketa Bet']),
				'SumaBet':self.noneEncapsulator(row['Suma Bet']),
				'BrojTiketaWin':self.noneEncapsulator(row['Broj Tiketa Win']),
				'SumaWin':self.noneEncapsulator(row['Suma Win']),
				'Ggr':self.noneEncapsulator(row['GGR']),
				'Margin':self.noneEncapsulator(row['Margin'])				})
			return {
				'tiket':podaci
			}

	
		# rows = result.fetchall()
		# keys = result.keys()
		# data = self.db.clean_select_results(rows, keys)
		# return {
		# 		'data': data
		# 	}