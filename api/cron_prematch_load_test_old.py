from db import Db
from db_land import DbLand
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
from datetime import datetime, timedelta
import json
import mysql.connector
import os
import pandas as pd
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

mydb = mysql.connector.connect(
	host="localhost",
	user="m.djacic",
	password="Soccer123",
	database="reporting",
	buffered=True,
	auth_plugin='mysql_native_password',
	charset="utf8mb4",
	use_unicode=True
)

def noneEncapsulator(arg):
	return float(0) if not arg else float(arg)

# risk = pd.read_csv(os.path.join(dir_path,"risk_per_competition.csv"))
# validCompetitions = risk['Competition ID'].tolist()
db = Db()
db2 = DbLand()
do = str(datetime.now()+timedelta(hours=2))
size = len(do)
do = do[:size-3]
od = str(datetime.now()+timedelta(hours=2)-timedelta(days=5))[:-16] + " 08:00:00.000"
podaci = []
result_web = []
result_land = []
print(od)
print(do)
with db.engine.begin() as conn:
	result_web = conn.execute(
	'exec dbo.m_prematchLoadMain @from="'+str(od)+'", @to="'+str(do)+'"')
	db.__del__()
	if result_web is None:
		result_web = []
	
	with db2.engine.begin() as conn2:
		result_land = conn2.execute(
		'exec dbo.m_prematchLoadMain @from="'+str(od)+'", @to="'+str(do)+'"')
		db2.__del__()
		if result_land is None:
			result_land = []
		found = False

		result_web = [i for i in result_web]
		result_land = [i for i in result_land]
		for row in result_web:
			for row2 in result_land:
				if str(row['Home Team'])==str(row2['Home Team']) and str(row['Away Team'])==str(row2['Away Team']) and str(row['Outcome'])==str(row2['Outcome']):
					found=True
					podaci.append({
						'Start':str(row['Start']) if row['Start'] else None,
						'Match ID':row['MatchId'],
						'Sport':row['Sport'] if hasattr(row, 'Sport') else row['SportId'],
						'CompetitionId':row['CompetitionId'] if hasattr(row, 'CompetitionId') else 0,
						'Home Team':row['Home Team'],
						'Away Team':row['Away Team'],
						'Outcome':row['Outcome'],
						'TotalImpactNumBets':noneEncapsulator(row['TotalImpactNumBets'])+noneEncapsulator(row2['TotalImpactNumBets']),
						'TotalImpactSumBet':noneEncapsulator(row['TotalImpactSumBet'])+noneEncapsulator(row2['TotalImpactSumBet']),
						'DirectImpactNumberBets':noneEncapsulator(row['DirectImpactNumberBets'])+noneEncapsulator(row2['DirectImpactNumberBets']),
						'DirectImpactSumBet':noneEncapsulator(row['DirectImpactSumBet'])+noneEncapsulator(row2['DirectImpactSumBet']),
						'DirectImpactWin':noneEncapsulator(row['DirectImpactWin'])+noneEncapsulator(row2['DirectImpactWin']),
						'Avg Odd':(noneEncapsulator(row['Avg Odd'])+noneEncapsulator(row2['Avg Odd']))/2
					})
			if not found:
				podaci.append({
					'Start':str(row['Start']) if row['Start'] else None,
					'Match ID':row['MatchId'],
					'Sport':row['Sport'] if hasattr(row, 'Sport') else row['SportId'],
					'CompetitionId':row['CompetitionId'] if hasattr(row, 'CompetitionId') else 0,
					'Home Team':row['Home Team'],
					'Away Team':row['Away Team'],
					'Outcome':row['Outcome'],
					'TotalImpactNumBets':float(row['TotalImpactNumBets']) if row['TotalImpactNumBets'] else None,
					'TotalImpactSumBet':float(row['TotalImpactSumBet']) if row['TotalImpactSumBet'] else None,
					'DirectImpactNumberBets':float(row['DirectImpactNumberBets']) if row['DirectImpactNumberBets'] else None,
					'DirectImpactSumBet':float(row['DirectImpactSumBet']) if row['DirectImpactSumBet'] else None,
					'DirectImpactWin':float(row['DirectImpactWin']) if row['DirectImpactWin'] else None,
					'Avg Odd':float(row['Avg Odd']) if row['Avg Odd'] else None
				})
			else:
				found = False
		for row in result_land:
			for row2 in result_web:
				if str(row['Home Team'])==str(row2['Home Team']) and str(row['Away Team'])==str(row2['Away Team']) and str(row['Outcome'])==str(row2['Outcome']):
					found=True
			if not found:
				podaci.append({
					'Start':str(row['Start']) if row['Start'] else None,
					'Match ID':row['MatchId'],
					'Sport':row['Sport'] if hasattr(row, 'Sport') else row['SportId'],
					'CompetitionId':row['CompetitionId'] if hasattr(row, 'CompetitionId') else 0,
					'Home Team':row['Home Team'],
					'Away Team':row['Away Team'],
					'Outcome':row['Outcome'],
					'TotalImpactNumBets':float(row['TotalImpactNumBets']) if row['TotalImpactNumBets'] else None,
					'TotalImpactSumBet':float(row['TotalImpactSumBet']) if row['TotalImpactSumBet'] else None,
					'DirectImpactNumberBets':float(row['DirectImpactNumberBets']) if row['DirectImpactNumberBets'] else None,
					'DirectImpactSumBet':float(row['DirectImpactSumBet']) if row['DirectImpactSumBet'] else None,
					'DirectImpactWin':float(row['DirectImpactWin']) if row['DirectImpactWin'] else None,
					'Avg Odd':float(row['Avg Odd']) if row['Avg Odd'] else None
				})
			else:
				found = False

		print(len(podaci))
		mycursor = mydb.cursor()
		sql = "DELETE FROM PrematchLoadTest"
		mycursor.execute(sql)
		mydb.commit()
		vreme = str(datetime.now()+timedelta(hours=2))
		for row in podaci:
			sql_comb = "INSERT INTO PrematchLoadTest(start,match_id,sport,home_team,away_team,outcome,total_impact_num_bets,total_impact_sum_bet,direct_impact_num_bets,direct_impact_sum_bet,direct_impact_win, entry_datetime, avg_odd) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			sql_comb_val = (row['Start'], row['Match ID'], row['Sport'], row['Home Team'], row['Away Team'], row['Outcome'], row['TotalImpactNumBets'], row['TotalImpactSumBet'], row['DirectImpactNumberBets'],row['DirectImpactSumBet'], row['DirectImpactWin'], vreme, row['Avg Odd'])
			mycursor.execute(sql_comb, sql_comb_val)
		mydb.commit()


# entryTime = datetime.now()+timedelta(hours=2)
# for index,row in alerts.iterrows():
# 	if row['CompetitionId'] in validCompetitions:
# 		startDate = row['Start']
# 		alertStatus = 0
# 		if startDate > entryTime:
# 			hourDiff = (startDate-entryTime)/np.timedelta64(1,'h')
# 			try:
# 				riskValue = risk[(risk['Competition ID'] == row['CompetitionId']) & (risk['start_hour']<hourDiff) & (risk['end_hour']>hourDiff)]['percentile_95'].values[0]
# 			except:
# 				pass
# 			if row['TotalImpactSumBet']>riskValue:
# 				alertStatus = 1
# 		sql_comb = "INSERT INTO MatchAlerts(match_id, competition_id, current_sum_bet, entry_time, match_start_date, alert_status) values(%s,%s,%s,%s,%s,%s)"
# 		sql_comb_val = (row['Match ID'], row['CompetitionId'], row['TotalImpactSumBet'], entryTime, row['Start'], alertStatus)
# 		mycursor.execute(sql_comb, sql_comb_val)
# mydb.commit()
