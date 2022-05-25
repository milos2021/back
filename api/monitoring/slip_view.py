from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import mysql.connector
import json


class SlipView(Resource):

    def __init__(self):
        self.db = Db()
  
    @staticmethod
    def noneEncapsulator(arg):
        return float(0) if not arg else float(arg)

    def post(self):
        data = request.get_json(force=True)
        od = data['from']
        do = data['to']
        code = data['code']
        matchId = data['matchId']
        cs = data['cs']
        param = data['param']
        if param is None:
            param = 'NULL'
        if cs is None:
            cs = 'NULL'
        
        with self.db.engine.begin() as conn:
            podaci = []
            result = conn.execute(
            'exec dbo.m_prematchLoad @from="'+str(od)+'", @to="'+str(do)+'", @code="'+str(code)+'", @matchId='+str(matchId)+', @param="'+str(param)+'", @cs='+str(cs))
            if result is None:
                result = []
            for row in result:
                podaci.append({
                    'Ceka se':row['Ceka se'],
                    'BetParamText':str(row['BetParamText']) if row['BetParamText'] else None,
                    'Pot Win':self.noneEncapsulator(row['Pot Win']),
                    'Id':str(row['Id']),
                    'Amount':self.noneEncapsulator(row['Amount']),
                    'NumberOfMatches':row['NumberOfMatches'],
                    'ClientAcceptanceTime':str(row['ClientAcceptanceTime']) if row['ClientAcceptanceTime'] else None,
                    'UserName':row['UserName'],
                    'HomeCompetitorName':row['HomeCompetitorName'],
                    'AwayCompetitorName':row['AwayCompetitorName'],
                    'SportId':row['SportId'],
                    'BetOdds':row['BetOdds'],
                    'SumOdds':row['SumOdds'],
                    'SlipWinningStatus':row['SlipWinningStatus'],
                    'SlipGroupLineWinningStatus':str(row['SlipGroupLineWinningStatus']) if row['SlipGroupLineWinningStatus'] else None,
                    'BetGameOutcomeCodeForPrinting':row['BetGameOutcomeCodeForPrinting'],
                    'TotalWinningAmount':self.noneEncapsulator(row['TotalWinningAmount']),
                    'BonusAmount':self.noneEncapsulator(row['BonusAmount'])
                })
                
            return {
                'tiket':podaci
            }
