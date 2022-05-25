from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text


class RepStats(Resource):
	""" Tiket View """

	def __init__(self):
		self.db = Db()

	@staticmethod
	def noneEncapsulator(arg):
		return float(0) if not arg else float(arg)

	def post(self):
		data = request.get_json(force=True)
		rangeFrom = data['rangeFrom']
		rangeTo = data['rangeTo']
		if rangeFrom == '' or rangeFrom is None:
			rangeFrom=-1
		if rangeTo == '' or rangeTo is None:
			rangeTo=-1
		monthFrom = data['monthFrom']
		monthTo = data['monthTo']
		slipType = data['slipType']
		aspect = data['aspect']
		years = ""
		if data['year']:
			result = data['year']
			for index in range(len(result)):
				if index==len(result)-1:
					years+="'"+str(result[index])+"'"
				else:
					years+="'"+str(result[index])+"',"
		podaci = []
		print(years)
		with self.db.engine.begin() as conn:
			if aspect == 3:
				result = conn.execute(
				'exec dbo.m_createRepStatsStatisticPerDay @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @slipType='+str(slipType))
				for row in result:
					podaci.append({
					'Opseg':row['Opseg'].strftime("%Y-%m-%d"),
					'SumBet':self.noneEncapsulator(row['SumBet']),
					'SumWin':self.noneEncapsulator(row['SumWin']),
					'SumRegularWin':self.noneEncapsulator(row['SumRegularWin']),
					'CtrbRegular':self.noneEncapsulator(row['CtrbRegular']),
					'SumBonusWin':self.noneEncapsulator(row['SumBonusWin']),
					'CtrbBonus':self.noneEncapsulator(row['CtrbBonus']),
					'SumCashbackWin':self.noneEncapsulator(row['SumCashbackWin']),
					'CtrbCashback':self.noneEncapsulator(row['CtrbCashback']),
					'GgrRegular':self.noneEncapsulator(row['GgrRegular']),
					'GgrRegularMargin':self.noneEncapsulator(row['GgrRegularMargin']),
					'Ggr':self.noneEncapsulator(row['Ggr']),
					'GgrMargin':self.noneEncapsulator(row['GgrMargin'])
				})
			if aspect == 4:
				result = conn.execute(
				'exec dbo.m_createBettingStatisticPerYear  @year="'+str(years)+'", @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @slipType='+str(slipType))
				for row in result:
					podaci.append({
					'Opseg':row['Opseg'],
					'Bet':self.noneEncapsulator(row['Bet']),
					'SumBet':self.noneEncapsulator(row['SumBet']),
					'AvgBet':self.noneEncapsulator(row['AvgBet']),
					'GwaOdds':self.noneEncapsulator(row['GwaOdds']),
					'GwaEvents':self.noneEncapsulator(row['GwaEvents']),
					'Win':self.noneEncapsulator(row['Win']),
					'CtrbBets':self.noneEncapsulator(row['CtrbBets']),
					'SumWin':self.noneEncapsulator(row['SumWin'])
				})		
			if aspect == 5:
				result = conn.execute(
				'exec dbo.m_createBettingStatisticPerMonth @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @slipType='+str(slipType))
				for row in result:
					podaci.append({
					'Opseg':row['Opseg'],
					'Bet':self.noneEncapsulator(row['Bet']),
					'SumBet':self.noneEncapsulator(row['SumBet']),
					'AvgBet':self.noneEncapsulator(row['AvgBet']),
					'GwaOdds':self.noneEncapsulator(row['GwaOdds']),
					'GwaEvents':self.noneEncapsulator(row['GwaEvents']),
					'Win':self.noneEncapsulator(row['Win']),
					'CtrbBets':self.noneEncapsulator(row['CtrbBets']),
					'SumWin':self.noneEncapsulator(row['SumWin'])
				})			

		return {
				'tiket': podaci
			}

  
