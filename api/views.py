from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json
from datetime import datetime
import mysql.connector

class Tiket(Resource):
	""" Tiket View """

	def __init__(self):
		self.db = Db()
		self.mydb = mysql.connector.connect(
			host="10.0.90.23",
			user="m.djacic",
			password="Soccer123",
			database="arhiva",
			buffered=True,
			auth_plugin='mysql_native_password'
		)
		

	@staticmethod
	def noneEncapsulator(arg):
		return float(0) if not arg else float(arg)
	
	def datetimeConverter(o):
		if isinstance(o, datetime.date):
			return o.__str__()

	def post(self):
		data = request.get_json(force=True)
		realTime = data['realtime']
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
		month = data['month']
		years = ""
		if data['year']:
			result = data['year']
			for index in range(len(result)):
				if index==len(result)-1:
					years+="'"+str(result[index])+"'"
				else:
					years+="'"+str(result[index])+"',"
		podaci = []
		

		mycursor = self.mydb.cursor()
		check = 'SELECT * FROM combinations where r_id=1 AND month='+str(month)+' AND year="'+years+'" AND period is null and payment_type is null and slip_type='+str(slipType)+' AND aspect='+str(aspect)
		mycursor.execute(check)
		result = mycursor.fetchone()
		day_created = None
		if result:
			cached_data = result[0]
			day_created = result[8]
		if not mycursor.rowcount or realTime or day_created!=monthTo:
			with self.db.engine.begin() as conn:
				if aspect == 0:
					result = conn.execute(
					'exec dbo.m_createBettingStatisticForRanges @rf='+str(rangeFrom)+', @rt='+str(rangeTo)+', @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @slipType='+str(slipType))
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

				if aspect == 1:
					result = conn.execute(
					'exec dbo.m_createBettingStatisticForNumberOfEvents @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @slipType='+str(slipType))
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
				if aspect == 3:
					result = conn.execute(
					'exec dbo.m_createBettingStatisticPerDay @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @slipType='+str(slipType))
					for row in result:
						datum = None
						if isinstance(row['Opseg'], str):
							datum = row['Opseg']
						else:
							datum = row['Opseg'].strftime("%Y-%m-%d")
						podaci.append({
						'Opseg':datum,
						'Bet':self.noneEncapsulator(row['Bet']),
						'SumBet':self.noneEncapsulator(row['SumBet']),
						'AvgBet':self.noneEncapsulator(row['AvgBet']),
						'GwaOdds':self.noneEncapsulator(row['GwaOdds']),
						'GwaEvents':self.noneEncapsulator(row['GwaEvents']),
						'Win':self.noneEncapsulator(row['Win']),
						'CtrbBets':self.noneEncapsulator(row['CtrbBets']),
						'SumWin':self.noneEncapsulator(row['SumWin'])
					})
					print(podaci)
				if aspect == 4:
					result = conn.execute(
					'exec dbo.m_createBettingStatisticPerYear  @year='+str(years)+', @from="'+str(monthFrom)+'", @to="'+str(monthTo)+'", @slipType='+str(slipType))
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
			if not realTime:					
				sql_comb = "INSERT INTO combinations(r_id,month,year,slip_type,aspect,day_created) values(%s,%s,%s,%s,%s,%s)"
				sql_comb_val = (1,str(month),years,str(slipType),str(aspect), str(monthTo))
				mycursor.execute(sql_comb, sql_comb_val)
				self.mydb.commit()
				last_insert_id=mycursor.lastrowid
				sql = "INSERT INTO data(comb_id,json_data) values("+str(last_insert_id)+",%s)"
				val = (json.dumps(podaci),)
				mycursor.execute(sql, val)
				self.mydb.commit()
				# print(mycursor.rowcount, "record inserted.")
			return {
					'tiket': podaci
				}
		else:
			mycursor = self.mydb.cursor()
			sql_data = 'SELECT json_data FROM data where comb_id='+str(cached_data)
			mycursor.execute(sql_data)
			result = json.loads(mycursor.fetchone()[0])
			return {
				'tiket':result
			}

		

  
