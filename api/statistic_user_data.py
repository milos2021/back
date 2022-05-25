from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json


class StatisticUserData(Resource):

	def __init__(self):
		self.db = Db()
	
	@staticmethod
	def row2dict(row):
		d = {}
		for column in row.__table__.columns:
			d[column.name] = str(getattr(row, column.name))

		return d

	def post(self):
		data = request.get_json(force=True)
		od = data['from']
		do = data['to']
		slipType = data['slipType']
		userId = data['userId']
		with self.db.engine.begin() as conn:
			podaci = []
			result = conn.execute(
			'exec dbo.m_getFilteredUserData @from="'+str(od)+'", @to="'+str(do)+'", @userId="'+str(userId)+'", @slipType='+str(slipType))
			if result is None:
				result = []
			keys = ["Num Lines", "RiskLevel", "Perc Hit", "Minuti razlika mean", "Bet Mean", "Bet Std", "Win Mean", "Kvota linija mean", "Kvota tiketa mean", 'Kvota tiketa std','Broj Tiketa','Broj parova mean','Fudbal Sum Bet','Fudbal Sum Win','Kosarka Sum Bet','Kosarka Sum Win','Tenis Sum Bet','Tenis Sum Win', 'Igraci Specijal Sum Bet','Igraci Specijal Sum Win','Ostalo Sum Bet','Ostalo Sum Win']
			for row in result:
				obj = {}
				for key in keys:
					if not row[key]:
						obj[key]=0
					else:
						obj[key]=row[key]
				podaci.append({
					'numlines':int(obj['Num Lines']),
					'risklevel':int(obj['RiskLevel']),
					'perchit':float(obj['Perc Hit']),
					'minutirazlikamean':float(obj['Minuti razlika mean']),
					'betmean':round(float(obj['Bet Mean']),2),
					'betstd':round(float(obj['Bet Std']),2),
					'winmean':round(float(obj['Win Mean']),2),
					'kvotalinijamean':round(float(obj['Kvota linija mean']),2),
					'kvotatiketamean':round(float(obj['Kvota tiketa mean']),2),
					'kvotatiketastd':round(float(obj['Kvota tiketa std']),2), 
					'brojtiketa':int(obj['Broj Tiketa']),
					'brojparovamean':round(float(obj['Broj parova mean']),2),
					'fudbalsumbet':round(float(obj['Fudbal Sum Bet']),2),
					'fudbalsumwin':round(float(obj['Fudbal Sum Win']),2),
					'profitfudbal':round(float(obj['Fudbal Sum Bet'])-float(obj['Fudbal Sum Win']),2),
					'marginfudbal':((float(obj['Fudbal Sum Bet'])-float(obj['Fudbal Sum Win']))/float(obj['Fudbal Sum Bet'])) if obj['Fudbal Sum Bet'] else 0,
					'kosarkasumbet':round(float(obj['Kosarka Sum Bet']),2),
					'kosarkasumwin':round(float(obj['Kosarka Sum Win']),2),
					'profitkosarka':round(float(obj['Kosarka Sum Bet'])-float(obj['Kosarka Sum Win']),2),
					'marginkosarka':((float(obj['Kosarka Sum Bet'])-float(obj['Kosarka Sum Win']))/float(obj['Kosarka Sum Bet'])) if obj['Kosarka Sum Bet'] else 0,
					'tenissumbet':round(float(obj['Tenis Sum Bet']),2),
					'tenissumwin':round(float(obj['Tenis Sum Win']),2),
					'profittenis':round(float(obj['Tenis Sum Bet'])-float(obj['Tenis Sum Win']),2),
					'margintenis':((float(obj['Tenis Sum Bet'])-float(obj['Tenis Sum Win']))/float(obj['Tenis Sum Bet'])) if obj['Tenis Sum Bet'] else 0,
					'igracispecijalsumbet':round(float(obj['Igraci Specijal Sum Bet']),2),
					'igracispecijalsumwin':round(float(obj['Igraci Specijal Sum Win']),2),
					'profitigracispecijal':round(float(obj['Igraci Specijal Sum Bet'])-float(obj['Igraci Specijal Sum Win']),2),
					'marginigracispecijal':((float(obj['Igraci Specijal Sum Bet'])-float(obj['Igraci Specijal Sum Win']))/float(obj['Igraci Specijal Sum Bet'])) if obj['Igraci Specijal Sum Bet'] else 0,
					'ostalosumbet':round(float(obj['Ostalo Sum Bet']),2),
					'ostalosumwin':round(float(obj['Ostalo Sum Win']),2),   
					'profitostalo':round(float(obj['Ostalo Sum Bet'])-float(obj['Ostalo Sum Win']),2),
					'marginostalo':((float(obj['Ostalo Sum Bet'])-float(obj['Ostalo Sum Win']))/float(obj['Ostalo Sum Bet'])) if obj['Ostalo Sum Bet'] else 0,
					'bet':round(sum([float(obj['Fudbal Sum Bet']), float(obj['Kosarka Sum Bet']),float(obj['Tenis Sum Bet']), float(obj['Igraci Specijal Sum Bet']), float(obj['Ostalo Sum Bet'])]),2),
					'win':round(sum([float(obj['Fudbal Sum Win']), float(obj['Kosarka Sum Win']),float(obj['Tenis Sum Win']), float(obj['Igraci Specijal Sum Win']), float(obj['Ostalo Sum Win'])]),2)
				})
				
			return {
				'tiket':podaci
			}
