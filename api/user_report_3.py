from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json


class UserReport3(Resource):

    def __init__(self):
        self.db = Db()

    @staticmethod
    def noneEncapsulator(arg):
        return float(0) if not arg else float(arg)

    def post(self):
        data = request.get_json(force=True)
        tip = data['tip']
        if tip == 1:
            slipCount = data['slipCount']
            balanceLimit = data['balanceLimit']
        if tip == 2:
            od = data['from']
            do = data['to']
            userId = data['userId']
        query = ""
        with self.db.engine.begin() as conn:
            podaci = []
            if tip == 1:
                result = conn.execute(
                'exec dbo.m_getSpecificUsers @slipCount='+str(slipCount)+', @balanceLimit='+str(balanceLimit)+', @numberOfMonths=6')
                for row in result:
                    podaci.append({
                    'id':str(row['id']),
                    'balance':self.noneEncapsulator(row['balance']),
                    'username':row['username'],
                    'date_of_reg':row['date_of_reg'].strftime("%Y-%m-%d")
                    })
            if tip == 2:
                result = conn.execute(
                'exec dbo.m_getUserDataForPeriod @from='+str(od)+', @to='+str(do)+', @userId='+str(userId))
                for row in result:
                    podaci.append({
                    'broj_parova_mean':self.noneEncapsulator(row['broj_parova_mean']),
                    'broj_tiketa':self.noneEncapsulator(row['broj_tiketa']),
                    'kvota_linija_mean':self.noneEncapsulator(row['kvota_linija_mean']),
                    'kvota_tiketa_mean':self.noneEncapsulator(row['kvota_tiketa_mean']),
                    'bet_mean':self.noneEncapsulator(row['bet_mean']),
                    'sum_bet':self.noneEncapsulator(row['sum_bet']),
                    'sum_win':self.noneEncapsulator(row['sum_win']),
                    'profit':self.noneEncapsulator(row['sum_bet'])-self.noneEncapsulator(row['sum_win']),
                    'margin':(self.noneEncapsulator(row['sum_bet'])-self.noneEncapsulator(row['sum_win']))/self.noneEncapsulator(row['sum_bet']) if row['sum_bet'] else None
                    })
            return {
                    'tiket': podaci
                }
