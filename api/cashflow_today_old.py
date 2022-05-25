from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
import json
import mysql.connector
import os
from datetime import datetime, time, timedelta




class CashflowToday(Resource):

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

    def post(self):
        data = request.get_json(force=True)
        yesterday = data['yesterday']
        if not yesterday:
            sql_data = 'SELECT * FROM `TodayData` order by execution_time desc limit 1'
        else:
            if time(0,0) <= (datetime.now()+timedelta(hours=2)).time() <= time(8,0):
                juce = (datetime.today()+timedelta(hours=2)-timedelta(days=2)).strftime('%Y-%m-%d')+str(" 08:00:00")
            else:
                juce = (datetime.today()+timedelta(hours=2)-timedelta(days=1)).strftime('%Y-%m-%d')+str(" 08:00:00")
            sql_data = 'SELECT * FROM `TodayData` where Datum="'+str(juce)+'" order by execution_time desc limit 1'
        mycursor = self.mydb.cursor()
        mycursor.execute(sql_data)
        result = mycursor.fetchall()
        data = []
        one = {}
        for obj in result:
            podaci = {
                'Datum':obj[0],
                'deposit_sum_all':self.noneEncapsulator(obj[1]),
                'deposit_users_all':self.noneEncapsulator(obj[2]),
                'deposit_number_all':self.noneEncapsulator(obj[3]),
                'deposit_sum_bank':self.noneEncapsulator(obj[4]),
                'deposit_users_bank':self.noneEncapsulator(obj[5]),
                'deposit_number_bank':self.noneEncapsulator(obj[6]),
                'deposit_sum_cc':self.noneEncapsulator(obj[7]),
                'deposit_users_cc':self.noneEncapsulator(obj[8]),
                'deposit_number_cc':self.noneEncapsulator(obj[9]),
                'deposit_sum_ipay':self.noneEncapsulator(obj[10]),
                'deposit_users_ipay':self.noneEncapsulator(obj[11]),
                'deposit_number_ipay':self.noneEncapsulator(obj[12]),
                'deposit_sum_komsija':self.noneEncapsulator(obj[13]),
                'deposit_users_komsija':self.noneEncapsulator(obj[14]),
                'deposit_number_komsija':self.noneEncapsulator(obj[15]),
                'deposit_sum_shops':self.noneEncapsulator(obj[16]),
                'deposit_users_shops':self.noneEncapsulator(obj[17]),
                'deposit_number_shops':self.noneEncapsulator(obj[18]),
                'withdraw_sum_all':self.noneEncapsulator(obj[19]),
                'withdraw_users_all':self.noneEncapsulator(obj[20]),
                'withdraw_number_all':self.noneEncapsulator(obj[21]),
                'withdraw_sum_bank':self.noneEncapsulator(obj[22]),
                'withdraw_users_bank':self.noneEncapsulator(obj[23]),
                'withdraw_number_bank':self.noneEncapsulator(obj[24]),
                'withdraw_sum_shops':self.noneEncapsulator(obj[25]),
                'withdraw_users_shops':self.noneEncapsulator(obj[26]),
                'withdraw_number_shops':self.noneEncapsulator(obj[27]),
                'promo_sum':self.noneEncapsulator(obj[28]),
                'promo_users':self.noneEncapsulator(obj[29]),
                'promo_number':self.noneEncapsulator(obj[30]),
                'promo_cost':self.noneEncapsulator(obj[31]),
                'actual_std_balance':self.noneEncapsulator(obj[32]),
                'actual_promo_balance':self.noneEncapsulator(obj[33]),
                'actual_active_std_balance':self.noneEncapsulator(obj[34]),
                'actual_active_promo_balance':self.noneEncapsulator(obj[35]),
                'permanently_reserved':self.noneEncapsulator(obj[36]),
                'temporarely_reserved':self.noneEncapsulator(obj[37]),
                'na_per':self.noneEncapsulator(obj[38]),
                'na_tem':self.noneEncapsulator(obj[39]),
                'execution_time':obj[40]
            }
            data.append(podaci)
                
        return {"data":data}, 200
