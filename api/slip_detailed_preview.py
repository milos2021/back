from db import Db
from db_land import DbLand
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json


class SlipDetailedPreview(Resource):

	def __init__(self):
		self.name = "slip-view"

	def post(self):
		data = request.get_json(force=True)
		source = data['source']
		ticketId = data['ticketId']
		if source == 2:
			self.db = DbLand()
		if source == 1:
			self.db = Db()
		with self.db.engine.begin() as conn:
			podaci = []
			result = conn.execute(
			'exec dbo.m_getSlipDataByIdWithScore @slipId='+str(ticketId))
			if result is None:
				result = []
			if source == 2:
				for row in result:
					podaci.append({
						'Id':row['Id'],
						'HomeValue':row['HomeValue'],
						'AwayValue':row['AwayValue'],
						'MatchStartDate':str(row['MatchStartDate']) if row['MatchStartDate'] else None,
						'ID tiketa':row['ID tiketa'],
						'Vreme uplate':str(row['Vreme uplate']) if row['Vreme uplate'] else None,
						'Ulog':float(row['Ulog']) if row['Ulog'] else 0.00,
						'TotalWinningAmount':float(row['TotalWinningAmount']) if row['TotalWinningAmount'] else 0.00,
						'BonusAmount':float(row['BonusAmount']) if row['BonusAmount'] else 0.00,
						'BasicWinningAmount':float(row['BasicWinningAmount']) if row['BasicWinningAmount'] else 0.00,
						'Status Linije':row['Status linije'],
						'Domacin':row['Domacin'],
						'Status':row['Status'] if row['Status'] else 'Aktivan',
						'Gost':row['Gost'],
						'BetOdds':float(row['BetOdds']) if row['BetOdds'] else None,
						'Tip':row['Tip'],
						'BetParamText':row['BetParamText'],
						'NumberOfMatches':row['NumberOfMatches'],
						'Name':row['Name'], #sport
						'CompetitionName':row['CompetitionName'],
						'BetGameName':row['BetGameName'],
						'BetGameOutcomeShortName':row['BetGameOutcomeShortName'],
						'SlipType':row['SlipType'],
						'SumOdds':float(row['SumOdds']) if row['SumOdds'] else None,
						'SlipUserId':row['SlipUserId']
					})
			if source == 1:
				for row in result:
					podaci.append({
						'Id':row['Id'],
						'HomeValue':row['HomeValue'],
						'AwayValue':row['AwayValue'],
						'UserName':row['UserName'],
						'MatchStartDate':str(row['MatchStartDate']) if row['MatchStartDate'] else None,
						'ID tiketa':row['ID tiketa'],
						'Vreme uplate':str(row['Vreme uplate']) if row['Vreme uplate'] else None,
						'Ulog':float(row['Ulog']) if row['Ulog'] else 0.00,
						'TotalWinningAmount':float(row['TotalWinningAmount']) if row['TotalWinningAmount'] else 0.00,
						'BonusAmount':float(row['BonusAmount']) if row['BonusAmount'] else 0.00,
						'BasicWinningAmount':float(row['BasicWinningAmount']) if row['BasicWinningAmount'] else 0.00,
						'Status Linije':row['Status linije'],
						'Domacin':row['Domacin'],
						'Status':row['Status'] if row['Status'] else 'Aktivan',
						'Gost':row['Gost'],
						'BetOdds':float(row['BetOdds']) if row['BetOdds'] else None,
						'Tip':row['Tip'],
						'BetParamText':row['BetParamText'],
						'NumberOfMatches':row['NumberOfMatches'],
						'Name':row['Name'], #sport
						'CompetitionName':row['CompetitionName'],
						'BetGameName':row['BetGameName'],
						'BetGameOutcomeShortName':row['BetGameOutcomeShortName'],
						'SlipType':row['SlipType'],
						'SumOdds':float(row['SumOdds']) if row['SumOdds'] else None,
						'SlipUserId':row['SlipUserId']
					})
				
			return {
				'tiket':podaci
			}

  
