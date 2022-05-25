from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import mysql.connector
import json


class PrematchLoad(Resource):

	def __init__(self):
		self.mydb = mysql.connector.connect(
			host="localhost",
			user="m.djacic",
			password="Soccer123",
			database="reporting",
			buffered=True,
			auth_plugin='mysql_native_password'
		)
	@staticmethod
	def noneEncapsulator(arg):
		return float(0) if not arg else float(arg)

	def get(self):
		sql = "select * from PrematchLoad"
		mycursor = self.mydb.cursor()
		mycursor.execute(sql)
		result = mycursor.fetchall()
		data = []
		one = {}
		for obj in result:
			podaci = {
				'Start':str(obj[0]),
				'Match ID':obj[1],
				'Sport':obj[2],
				'Match':obj[3] + "-" + obj[4],
				'Outcome':obj[5],
				'#Bets':self.noneEncapsulator(obj[6]),
				'ΣBet':self.noneEncapsulator(obj[7]),
				'#Bets2':self.noneEncapsulator(obj[8]),
				'ΣBet2':self.noneEncapsulator(obj[9]),
				'ΣWin2':self.noneEncapsulator(obj[10]),
				'Last Change':str(obj[11]),
				'Avg Odd':self.noneEncapsulator(obj[12])
			}
			data.append(podaci)
				
		return {"data":data}, 200
