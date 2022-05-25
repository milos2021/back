from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json


class SlipDetailedPreview(Resource):

	def __init__(self):
		self.db = Db()

	def post(self):
		data = request.get_json(force=True)
		ticketId = data['ticketId']
		with self.db.engine.begin() as conn:
			podaci = []
			result = conn.execute(
			'exec dbo.m_getSlipDataById @slipId="'+str(ticketId)+'"')
			if result is None:
				result = []
			for row in result:
				podaci.append({
					'ID tiketa':row['ID tiketa'],
					'Vreme uplate':str(row['Vreme uplate']) if row['Vreme uplate'] else None,
					'Ulog':float(row['Ulog']) if row['Ulog'] else None,
					'TotalWinningAmount':float(row['TotalWinningAmount']) if row['TotalWinningAmount'] else None,
					'BonusAmount':float(row['BonusAmount']) if row['BonusAmount'] else None,
					'BasicWinningAmount':float(row['BasicWinningAmount']) if row['BasicWinningAmount'] else None,
					'Status':row['Status'],
					'Status Linije':row['Status Linije'],
					'Domacin':row['Home'],
					'Status':row['Status'] if row['Status'] else 'Aktivan',
					'Gost':row['Away'],
					'BetOdds':float(row['BetOdds']) if row['BetOdds'] else None,
					'Tip':row['Tip'],
					'BetParamText':row['BetParamText'],
					'NumberOfMatches':row['NumberOfMatches'],
					'Name':row['Name'], #sport
					'CompetitionName':row['CompetitionName'],
					'BetGameName':row['BetGameName'],
					'BetGameOutcomeShortName':row['BetGameOutcomeShortName'],
					'SlipType':row['SlipType'],
					'SumOdds':float(row['Sum Odds']) if row['SumOdds'] else None,
					'SlipUserId':row['SlipUserId']
				})
				
			return {
				'tiket':podaci
			}

  
