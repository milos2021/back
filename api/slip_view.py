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
            query = ""
            if param == 'NULL':
                query = 'exec dbo.m_prematchLoad @from="'+str(od)+'", @to="'+str(do)+'", @code="'+str(code)+'", @param='+str(param)+', @matchId='+str(matchId)+', @cs='+str(cs)
            else:
                query = 'exec dbo.m_prematchLoad @from="'+str(od)+'", @to="'+str(do)+'", @code="'+str(code)+'", @param="'+str(param)+'", @matchId='+str(matchId)+', @cs='+str(cs)
            result = conn.execute(query)
            if result is None:
                result = []
            for row in result:
                podaci.append({
                    'Ceka se':row['Ceka se'],
                    'BetParamText':str(row['BetParamText']) if row['BetParamText'] else None,
                    'Pot win':self.noneEncapsulator(row['Pot win']),
                    'Id':str(row['Id']),
                    'Amount':self.noneEncapsulator(row['Amount']),
                    'NumberOfMatches':row['NumberOfMatches'],
                    'ClientAcceptanceTime':str(row['ClientAcceptanceTime']) if row['ClientAcceptanceTime'] else None,
                    'UserName':row['UserName'],
                    'HomeCompetitorName':row['HomeCompetitorName'],
                    'AwayCompetitorName':row['AwayCompetitorName'],
                    'SportId':self.noneEncapsulator(row['SportId']),
                    'BetOdds':self.noneEncapsulator(row['BetOdds']),
                    'SumOdds':self.noneEncapsulator(row['SumOdds']),
                    'SlipWinningStatus':row['SlipWinningStatus'],
                    'SlipGroupLineWinningStatus':str(row['SlipGroupLineWinningStatus']) if row['SlipGroupLineWinningStatus'] else None,
                    'BetGameOutcomeCodeForPrinting':row['BetGameOutcomeCodeForPrinting'],
                    'StartDate':str(row['StartDate']) if row['StartDate'] else None,
                    'CompetitionName':row['CompetitionName'],
                    'BetGameName':row['BetGameName'],
                    'MatchCode':row['MatchCode']
                })
            return {
                'tiket':podaci
            }
