from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json


class SportReport(Resource):

	def __init__(self):
		self.db = Db()

	@staticmethod
	def noneEncapsulator(arg):
		return float(0) if not arg else float(arg)

	def post(self):
		data = request.get_json(force=True)
		sportId = data['sportId']
		competitionId = data['competitionId']
		monthFrom = data['monthFrom']
		monthTo = data['monthTo']
		slipType = data['slipType']
		aspect = data['aspect']
		year = data['year']
		#aspects:
		#1 - day
		#2 - month
		#3 - year
		with self.db.engine.begin() as conn:
			podaci = []
			if aspect == 1:
				result = conn.execute(
				'exec dbo.m_createSportStatisticPerDay @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @sportId='+str(sportId)+', @competitionId='+("NULL" if not competitionId else str(competitionId))+', @slipType='+("NULL" if not slipType and slipType!=0 else str(slipType)))
				for row in result:
					podaci.append({
					'Date':row['Datum'],
					'Bet':row['Bet'],
					'SumBet':self.noneEncapsulator(row['SumBet']),
					'AvgBet':self.noneEncapsulator(row['AvgBet']),
					'GwaOdds':self.noneEncapsulator(row['GwaOdds']),
					'GwaEvents':self.noneEncapsulator(row['GwaEvents']),
					'CtrbBets':self.noneEncapsulator(row['CtrbBets']),
					'SumWin':self.noneEncapsulator(row['SumWin']),
					'Win':row['Win']
					})
			if aspect == 3:
				result = conn.execute(
				'exec dbo.m_createSportStatisticPerYear @year="'+str(year)+'", @sportId='+str(sportId)+', @competitionId='+("NULL" if not competitionId else str(competitionId))+', @slipType='+("NULL" if not slipType and slipType!=0 else str(slipType)))
				for row in result:
					podaci.append({
					'Date':row['Datum'],
					'Bet':row['Bet'],
					'SumBet':self.noneEncapsulator(row['SumBet']),
					'AvgBet':self.noneEncapsulator(row['AvgBet']),
					'GwaOdds':self.noneEncapsulator(row['GwaOdds']),
					'GwaEvents':self.noneEncapsulator(row['GwaEvents']),
					'CtrbBets':self.noneEncapsulator(row['CtrbBets']),
					'SumWin':self.noneEncapsulator(row['SumWin']),
					'Win':row['Win']
					})
			if aspect == 2:
				result = conn.execute(
				'exec dbo.m_createSportStatisticPerMonth @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @sportId='+str(sportId)+', @competitionId='+("NULL" if not competitionId else str(competitionId))+', @slipType='+("NULL" if not slipType and slipType!=0 else str(slipType)))
				for row in result:
					podaci.append({
					'Date':row['Datum'],
					'Bet':row['Bet'],
					'SumBet':self.noneEncapsulator(row['SumBet']),
					'AvgBet':self.noneEncapsulator(row['AvgBet']),
					'GwaOdds':self.noneEncapsulator(row['GwaOdds']),
					'GwaEvents':self.noneEncapsulator(row['GwaEvents']),
					'CtrbBets':self.noneEncapsulator(row['CtrbBets']),
					'SumWin':self.noneEncapsulator(row['SumWin']),
					'Win':row['Win']
					})

			if aspect == 4:
				result = conn.execute(
				'exec dbo.m_createSportStatisticPerMatch @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @sportId='+str(sportId)+', @competitionId='+("NULL" if not competitionId else str(competitionId)))
				for row in result:
					podaci.append({
					'Date':row['MatchStartDate'].strftime("%Y-%m-%d"),
					'SlipId':row['Id'],
					'MatchId':row['MatchId'],
					'BetGameOutcomeName':row['BetGameOutcomeName'],
					'BetGameName':row['BetGameName'],
					'HomeCompetitorName':row['HomeCompetitorName'],
					'AwayCompetitorName':row['AwayCompetitorName'],
					'HomeValue':row['HomeValue'],
					'AwayValue':row['AwayValue'],
					'SumBet':self.noneEncapsulator(row['SumBet']),
					'SumWin':self.noneEncapsulator(row['Razlika']),
					'Granica':row['BetParamText'],
					'BetGameId':row['BetGameId'],
					'BetGameOutcomeId':row['BetGameOutcomeId']
					})
			return {
				'tiket':podaci
			}

	
		# rows = result.fetchall()
		# keys = result.keys()
		# data = self.db.clean_select_results(rows, keys)
		# return {
		# 		'data': data
		# 	}