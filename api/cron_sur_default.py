from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
from datetime import datetime, timedelta
import json
import mysql.connector
import os

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


db = Db()
#od = str(datetime.now()-timedelta(days=1))[:-16] + " 08:00:00.000"
#do = str(datetime.now())[:-16] + " 08:00:00.000"
od = "2021-12-21 08:00:00.000"
do = "2021-12-27 08:00:00.000"
print(od)
print(do)
slipType = 1
with db.engine.begin() as conn:
	podaci = []
	result = conn.execute(
	'exec dbo.m_getDefaultUsersData @from="'+str(od)+'", @to="'+str(do)+'", @slipType='+str(slipType))
	db.__del__()
	if result is None:
		result = []
	keys = ['UserName','SlipUserId','ProcessedDateTime','broj_parova_mean','broj_tiketa','kvota_linija_mean','kvota_tiketa_mean','bet_mean','sum_bet','sum_win']
	for row in result:
		obj = {}
		for key in keys:
			if not row[key]:
				obj[key]=0
			else:
				obj[key]=row[key]
		podaci.append({
			'username':obj['UserName'],
			'slipuserid':obj['SlipUserId'],
			'date':str(obj['ProcessedDateTime']),
			'brojparovamean':round(float(obj['broj_parova_mean']),2),
			'brojtiketa':int(obj['broj_tiketa']),
			'kvotalinijamean':round(float(obj['kvota_linija_mean']),2),
			'kvotatiketamean':round(float(obj['kvota_tiketa_mean']),2),
			'betmean':round(float(obj['bet_mean']),2),
			'sumbet':round(float(obj['sum_bet']),2),
			'sumwin':round(float(obj['sum_win']),2), 
			'sliptype':slipType
		})
duzina = len(podaci)
for idx,podatak in enumerate(podaci):
	print("Inserting "+str(idx+1)+" out of"+str(duzina))
	mycursor = mydb.cursor()
	mycursor.execute('SET NAMES utf8mb4')
	mycursor.execute("SET CHARACTER SET utf8mb4")
	mycursor.execute("SET character_set_connection=utf8mb4")
	podatak['username'] = json.dumps(podatak['username'],ensure_ascii=False).encode("utf-8","replace").decode("utf-8", 'replace')
	sql_data = 'insert into StatisticUserReportDefault values('+str(podatak['username'])+',"'+str(podatak['slipuserid'])+'","'+str(podatak['date'])+'",'+str(podatak['brojparovamean'])+','+str(podatak['brojtiketa'])+','+str(podatak['kvotalinijamean'])+','+str(podatak['kvotatiketamean'])+','+str(podatak['betmean'])+','+str(podatak['sumbet'])+','+str(podatak['sumwin'])+','+str(podatak['sliptype'])+')'
	mycursor.execute(sql_data)
mydb.commit()
