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
# od = str(datetime.now()-timedelta(days=1))[:-16] + " 08:00:00.000"
# do = str(datetime.now())[:-16] + " 08:00:00.000"
od = "2021-12-21 08:00:00.000"
do = "2021-12-27 08:00:00.000"
print(od)
print(do)
slipType = 1
with db.engine.begin() as conn:
	podaci = []
	result = conn.execute(
	'exec dbo.m_getFilteredUsersData @from="'+str(od)+'", @to="'+str(do)+'", @slipType='+str(slipType)+', @sportId=NULL')
	db.__del__()
	if result is None:
		result = []
	keys = ['UserName','SlipUserId','ProcessedDateTime','Num Lines','Broj Tiketa','Fudbal Sum Bet','Fudbal Sum Win','Fudbal Broj Tiketa','Kosarka Sum Bet','Kosarka Sum Win','Kosarka Broj Tiketa','Tenis Sum Bet','Tenis Sum Win','Tenis Broj Tiketa','Igraci Specijal Sum Bet','Igraci Specijal Sum Win','Igraci Specijal Broj Tiketa', 'Ostalo Sum Bet', 'Ostalo Sum Win', 'Ostalo Broj Tiketa']
	for row in result:
		obj = {}
		for key in keys:
			if not row[key]:
				obj[key]=0
			else:
				obj[key]=row[key]
		podaci.append({
			'username':obj['UserName'],
			'SlipUserId':obj['SlipUserId'],
			'date':str(obj['ProcessedDateTime']),
			'numlines':int(obj['Num Lines']),
			'brojtiketa':int(obj['Broj Tiketa']),
			'fudbalsumbet':round(float(obj['Fudbal Sum Bet']),2),
			'fudbalsumwin':round(float(obj['Fudbal Sum Win']),2),
			'fudbalbrojtiketa':int(obj['Fudbal Broj Tiketa']),
			'kosarkasumbet':round(float(obj['Kosarka Sum Bet']),2),
			'kosarkasumwin':round(float(obj['Kosarka Sum Win']),2),
			'kosarkabrojtiketa':int(obj['Kosarka Broj Tiketa']),
			'tenissumbet':round(float(obj['Tenis Sum Bet']),2),
			'tenissumwin':round(float(obj['Tenis Sum Win']),2),
			'tenisbrojtiketa':int(obj['Tenis Broj Tiketa']),
			'igracispecijalsumbet':round(float(obj['Igraci Specijal Sum Bet']),2),
			'igracispecijalsumwin':round(float(obj['Igraci Specijal Sum Win']),2),
			'igracispecijalbrojtiketa':int(obj['Igraci Specijal Broj Tiketa']),
			'ostalosumbet':round(float(obj['Ostalo Sum Bet']),2),
			'ostalosumwin':round(float(obj['Ostalo Sum Win']),2),
			'ostalobrojtiketa':int(obj['Ostalo Broj Tiketa']),
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
	sql_data = 'insert into StatisticUserReportFiltered values('+str(podatak['username'])+',"'+str(podatak['SlipUserId'])+'","'+str(podatak['date'])+'",'+str(podatak['numlines'])+','+str(podatak['brojtiketa'])+','+str(podatak['fudbalsumbet'])+','+str(podatak['fudbalsumwin'])+','+str(podatak['fudbalbrojtiketa'])+','+str(podatak['kosarkasumbet'])+','+str(podatak['kosarkasumwin'])+','+str(podatak['kosarkabrojtiketa'])+','+str(podatak['tenissumbet'])+','+str(podatak['tenissumwin'])+','+str(podatak['tenisbrojtiketa'])+','+str(podatak['igracispecijalsumbet'])+','+str(podatak['igracispecijalsumwin'])+','+str(podatak['igracispecijalbrojtiketa'])+','+str(podatak['ostalosumbet'])+','+str(podatak['ostalosumwin'])+','+str(podatak['ostalobrojtiketa'])+','+str(podatak['sliptype'])+")"
	mycursor.execute(sql_data)
mydb.commit()
