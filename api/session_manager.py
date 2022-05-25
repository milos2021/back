from db import Db
from flask import request, Flask, jsonify, session
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json
import mysql.connector
import requests
import jwt
from datetime import datetime

class SessionManager(Resource):

	def __init__(self):
		self.db = Db()
		self.mydb = mysql.connector.connect(
			host="localhost",
			user="m.djacic",
			password="Soccer123",
			database="korisnici",
			buffered=True,
			auth_plugin='mysql_native_password'
		)
		#sql_comb = "INSERT INTO combinations(r_id,month,year,slip_type,aspect,day_created) values(%s,%s,%s,%s,%s,%s)"
		#sql_comb_val = (1,str(month),years,str(slipType),str(aspect), str(monthTo))
		#mycursor.execute(sql_comb, sql_comb_val)
		#self.mydb.commit()

		#mycursor = self.mydb.cursor()
		#sql_data = 'SELECT json_data FROM data where comb_id='+str(cached_data)
		#mycursor.execute(sql_data)
		#result = json.loads(mycursor.fetchone()[0])

	def post(self):
		mycursor = self.mydb.cursor()
		data = request.get_json(force=True) 

		username=None
		password=None


		if 'token' not in data.keys():
			username = data['username']
			password = data['password']

		token = None
		if 'token' in data.keys():
			token = data['token']

		if 'logout' in data.keys():
			print("uga")
			sql_logout = 'UPDATE korisnik set token="", loggedin=0 where token="'+str(token)+'"'
			mycursor.execute(sql_logout)
			self.mydb.commit()
			return {"message":"Logged out"}

		if token:
			sql_data = 'SELECT token, loggedin from korisnik where token="'+str(token)+'"'
			mycursor.execute(sql_data)
			result = mycursor.fetchall()
			if mycursor.rowcount:
				if result[0][1] == 1:
					return {"message":"Token valid"}, 200
				else:
					return {"message":"User logged out"}, 401
			else:
				return {"message":"Token not valid"}, 401

		url = "http://api.soccerbet.site:6080/user/validate/" + username + "/" + password
		headers = { "X-API-KEY": "4f313d46-1185-40e0-8429-6ccf1a3fd91e" }
		r = requests.get(url, headers=headers)
		result = json.loads(r.content)
		if 'detail' in result.keys():
			sql_data = 'SELECT id from korisnik where username="'+str(username)+'"'
			mycursor.execute(sql_data)
			if mycursor.rowcount:
				sql_failed_login = "UPDATE korisnik SET failed_attempts_count=failed_attempts_count+1 where id="+str(mycursor.fetchone()[0])
				mycursor.execute(sql_failed_login)
				self.mydb.commit()
			return result, 401
		else:
			data = {
			"email" : result['email'],
			"name" : result['givenName'],
			"login_datetime":str(datetime.today())
			}
			encoded_jwt = jwt.encode(data,'4f313d46-1185-40e0-8429-6ccf1a3fd91e',algorithm='HS256')
			#check if user exists
			sql_data = 'SELECT loggedin, id from korisnik where username="'+str(username)+'"'
			mycursor.execute(sql_data)
			data = mycursor.fetchall()
			if not mycursor.rowcount:
				sql_new_user = "INSERT INTO korisnik(username, loggedin, last_login, login_count, failed_attempts_count, locked, token) values(%s,%s,%s,%s,%s,%s,%s)"
				sql_new_user_val = (str(username), 1, str(datetime.today()), 1, 0, 0, encoded_jwt)
				mycursor.execute(sql_new_user, sql_new_user_val)
				self.mydb.commit()
				return {"token":encoded_jwt}
			else:
				is_logged_in = data[0][0] #promeniti posle za Fukija
				if is_logged_in == 1 and not data[0][1]==17:
					return {"detail":"You are already logged in on another machine. Please logout and try again."}, 406
				else:
					id = data[0][1]
					sql_existing_user = "UPDATE korisnik SET loggedin=1, last_login='"+str(datetime.today())+"', login_count = login_count + 1, token='"+encoded_jwt+"' where id="+str(id)
					mycursor.execute(sql_existing_user)
					self.mydb.commit()
					return {"token":encoded_jwt}

		return result
		
		

