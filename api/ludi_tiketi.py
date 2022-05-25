from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json


class LudiTiketi(Resource):

	def __init__(self):
		self.db = Db()

	def post(self):
		data = request.get_json(force=True)
		od = data['from']
		do = data['to']
		status = data['status']
		if status is None:
			status = 'NULL'
		slipType = data['slipType']
		if slipType is None:
			slipType = 'NULL'
		betFrom = data['betFrom']
		betTo = data['betTo']
		winFrom = data['winFrom']
		winTo = data['winTo']
		oddsFrom = data['oddsFrom']
		oddsTo = data['oddsTo']
		matchCode = data['matchCode']
		if matchCode is None:
			matchCode = 'NULL'
		outcomeId = data['outcomeId']
		if outcomeId is None:
			outcomeId = 'NULL'
		with self.db.engine.begin() as conn:
			podaci = []
			result = conn.execute(
			'exec dbo.m_getFilteredSlipData @from="'+str(od)+'", @to="'+str(do)+'", @slipType='+str(slipType)+', @betFrom='+str(betFrom)+', @betTo='+str(betTo)+', @winFrom='+str(winFrom)+', @winTo='+str(winTo)+', @oddFrom='+str(oddsFrom)+', @oddTo='+str(oddsTo)+', @outcomeId='+str(outcomeId)+', @code='+str(matchCode)+', @status='+str(status))
			if result is None:
				result = []
			for row in result:
				podaci.append({
					'Id':row['Id'],
					'SlipUserId':row['SlipUserId'],
					'UserName':row['UserName'],
					'ClientAcceptanceTime':str(row['ClientAcceptanceTime']) if row['ClientAcceptanceTime'] else None,
					'Amount':float(row['Amount']) if row['Amount'] else None,
					'TotalWinningAmount':float(row['TotalWinningAmount']) if row['TotalWinningAmount'] else None,
					'SumOdds':float(row['SumOdds']) if row['SumOdds'] else None,
					'SlipWinningStatus':row['SlipWinningStatus']
				})
				
			return {
				'tiket':podaci
			}

  
