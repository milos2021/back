from db import Db
from flask import request, Flask, jsonify, session
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json
import mysql.connector
import requests
import jwt
from datetime import datetime


mydb = mysql.connector.connect(
			host="localhost",
			user="m.djacic",
			password="Soccer123",
			database="reporting",
			buffered=True,
			auth_plugin='mysql_native_password'
		)

mycursor = mydb.cursor()

import pandas as pd
empdata = pd.read_csv('reporting/2_prematch_6_meseci.csv', index_col=False, delimiter = ',', header=None)
empdata.fillna(0, inplace=True)
mycursor.execute('SET NAMES utf8mb4')
mycursor.execute("SET CHARACTER SET utf8mb4")
mycursor.execute("SET character_set_connection=utf8mb4")
mydb.commit()
for i,row in empdata.iterrows():
	#here %S means string values 
	if i > 49581:
		sql = "INSERT INTO StatisticUserReport VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,2,0)"
		mycursor.execute(sql, tuple(row))
		print("Record inserted "+str(i))
		# the connection is not auto committed by default, so we must commit to save our changes
		mydb.commit()

