from db import Db
from flask import request, Flask, jsonify, session, abort
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json
import mysql.connector
from config import Config


class MonitoringData(Resource):

	def __init__(self):
		self.db = Db()
		mydb = mysql.connector.connect(
			host="localhost",
			user="root",
			password="Soccer123!",
			database="monitoring"
		)
	def post(self):
		o = Config()
		if request.remote_addr != o.IP or request.headers.get('Authorization') != o.TOKEN:
			abort(401)  # Forbidden
		else:
			data = request.get_json(force=True) 
			json_list = json.dumps(data['podaci'], separators=(',',':'))
			mycursor = mydb.cursor()
			mycursor.execute("INSERT INTO podaci(rawJson) values("+str(json_list)+")")
			mydb.commit()
		#returning for puroposes of testing
		#needs to be added as stringified json to db
		return 1

