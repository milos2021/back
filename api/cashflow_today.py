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
        self.db = Db()
        
    @staticmethod
    def noneEncapsulator(arg):
        return float(0) if not arg else float(arg)

    def post(self):
        data = request.get_json(force=True)
        yesterday = data['yesterday']
        
        sql_actual_date = 'select date from ActualDate'
        mycursor = self.mydb.cursor()
        mycursor.execute(sql_actual_date)
        actual_date = mycursor.fetchall()[0][0] #2021-10-01
        startDate = None
        endDate = None
        hours = (datetime.today()+timedelta(hours=2)).strftime('%H') #11
        minutes = (datetime.today()+timedelta(hours=2)).strftime('%M') #30
        lastMinute = False
        #ako je trenutno vreme izmedju ponoci i osam ujutru iduceg dana, dan pocetka je prethodni dan u 8 ujutru
        if time(0,0) <= (datetime.now()+timedelta(hours=2)).time() <= time(8,0):
            startDate = (datetime.today()+timedelta(hours=2)-timedelta(days=1)).strftime('%Y-%m-%d')+str(" 08:00:00")
        else:
            #ako nije, porede se aktuelni dan u bazi i trenutni dan, ako su isti pocetak je trenutni dan u 8 ujutru
            if datetime.strptime(actual_date, '%Y-%m-%d').day == (datetime.today()+timedelta(hours=2)).day:
                startDate = (datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+str(" 08:00:00")
                #u prvoj iteraciji novog dana, se osigurava da je prethodni zavrsen kako treba
                if (datetime.now()+timedelta(hours=2)).time().strftime('%H') == '08' and int((datetime.now()+timedelta(hours=2)).time().strftime('%M'))>1 and int((datetime.now()+timedelta(hours=2)).time().strftime('%M'))<8:
                    lastMinute = True
                    startDate = (datetime.today()+timedelta(hours=2)-timedelta(days=1)).strftime('%Y-%m-%d')+str(" 08:00:00")
                    endDate = (datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+str(" 07:59:59")
            else:
                #ako nisu isti, aktuelni dan se postavlja na trenutni dan
                sql_update_actual_date = "UPDATE ActualDate set date='"+(datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+"' where id=1"
                mycursor.execute(sql_update_actual_date)
                self.mydb.commit()
                startDate = (datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+str(" 08:00:00")
        if not lastMinute:
            endDate = (datetime.today()+timedelta(hours=2)-timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
        
        last_execution_time_sql = "select last_execution_time from ExecutionTimes where id=1"
        mycursor = self.mydb.cursor()
        mycursor.execute(last_execution_time_sql)
        last_execution_time = mycursor.fetchall()[0][0]
        last_execution_time = datetime.strptime(last_execution_time, '%Y-%m-%d %H:%M:%S')
        
        acceptable_next_execution = last_execution_time+timedelta(minutes=5)
        current_time = datetime.today()+timedelta(hours=2)
        if current_time >= acceptable_next_execution:
            with self.db.engine.begin() as conn:
                podaci = None
                result = conn.execute(
                'exec dbo.m_todayCashflow @from="'+str(startDate)+'", @to="'+str(endDate)+'"')
                self.db.__del__()
                if result is None:
                    result = []
                for obj in result:
                    podaci = {
                        'Datum':startDate,
                        'deposit_sum_all':self.noneEncapsulator(obj['deposit_sum_all']),
                        'deposit_users_all':self.noneEncapsulator(obj['deposit_users_all']),
                        'deposit_number_all':self.noneEncapsulator(obj['deposit_number_all']),
                        'deposit_sum_bank':self.noneEncapsulator(obj['deposit_sum_bank']),
                        'deposit_users_bank':self.noneEncapsulator(obj['deposit_users_bank']),
                        'deposit_number_bank':self.noneEncapsulator(obj['deposit_number_bank']),
                        'deposit_sum_cc':self.noneEncapsulator(obj['deposit_sum_cc']),
                        'deposit_users_cc':self.noneEncapsulator(obj['deposit_users_cc']),
                        'deposit_number_cc':self.noneEncapsulator(obj['deposit_number_cc']),
                        'deposit_sum_ipay':self.noneEncapsulator(obj['deposit_sum_ipay']),
                        'deposit_users_ipay':self.noneEncapsulator(obj['deposit_users_ipay']),
                        'deposit_number_ipay':self.noneEncapsulator(obj['deposit_number_ipay']),
                        'deposit_sum_komsija':self.noneEncapsulator(obj['deposit_sum_komsija']),
                        'deposit_users_komsija':self.noneEncapsulator(obj['deposit_users_komsija']),
                        'deposit_number_komsija':self.noneEncapsulator(obj['deposit_number_komsija']),
                        'deposit_sum_shops':self.noneEncapsulator(obj['deposit_sum_shops']),
                        'deposit_users_shops':self.noneEncapsulator(obj['deposit_users_shops']),
                        'deposit_number_shops':self.noneEncapsulator(obj['deposit_number_shops']),
                        'withdraw_sum_all':self.noneEncapsulator(obj['withdraw_sum_all']),
                        'withdraw_users_all':self.noneEncapsulator(obj['withdraw_users_all']),
                        'withdraw_number_all':self.noneEncapsulator(obj['withdraw_number_all']),
                        'withdraw_sum_bank':self.noneEncapsulator(obj['withdraw_sum_bank']),
                        'withdraw_users_bank':self.noneEncapsulator(obj['withdraw_users_bank']),
                        'withdraw_number_bank':self.noneEncapsulator(obj['withdraw_number_bank']),
                        'withdraw_sum_shops':self.noneEncapsulator(obj['withdraw_sum_shops']),
                        'withdraw_users_shops':self.noneEncapsulator(obj['withdraw_users_shops']),
                        'withdraw_number_shops':self.noneEncapsulator(obj['withdraw_number_shops']),
                        'promo_sum':self.noneEncapsulator(obj['promo_sum']),
                        'promo_users':self.noneEncapsulator(obj['promo_users']),
                        'promo_number':self.noneEncapsulator(obj['promo_number']),
                        'promo_cost':self.noneEncapsulator(obj['promo_cost']),
                        'actual_std_balance':self.noneEncapsulator(obj['actual_std_balance']),
                        'actual_promo_balance':self.noneEncapsulator(obj['actual_promo_balance']),
                        'actual_active_std_balance':self.noneEncapsulator(obj['actual_active_std_balance']),
                        'actual_active_promo_balance':self.noneEncapsulator(obj['actual_active_promo_balance']),
                        'permanently_reserved':self.noneEncapsulator(obj['permanently_reserved']),
                        'temporarely_reserved':self.noneEncapsulator(obj['temporarely_reserved']),
                        'na_per':self.noneEncapsulator(obj['na_per']),
                        'na_tem':self.noneEncapsulator(obj['na_tem']),
                        'execution_time':endDate
                    }
                    
            sql_update_actual_date = "UPDATE ExecutionTimes set last_execution_time='"+endDate+"' where id=1"
            mycursor.execute(sql_update_actual_date)
            self.mydb.commit()
            sql_insert_data = "insert into TodayData values('"+startDate+"',"+str(podaci['deposit_sum_all'])+","+str(podaci['deposit_users_all'])+","+str(podaci['deposit_number_all'])+","+str(podaci['deposit_sum_bank'])+","+str(podaci['deposit_users_bank'])+","+str(podaci['deposit_number_bank'])+","+str(podaci['deposit_sum_cc'])+","+str(podaci['deposit_users_cc'])+","+str(podaci['deposit_number_cc'])+","+str(podaci['deposit_sum_ipay'])+","+str(podaci['deposit_users_ipay'])+","+str(podaci['deposit_number_ipay'])+","+str(podaci['deposit_sum_komsija'])+","+str(podaci['deposit_users_komsija'])+","+str(podaci['deposit_number_komsija'])+","+str(podaci['deposit_sum_shops'])+","+str(podaci['deposit_users_shops'])+","+str(podaci['deposit_number_shops'])+","+str(podaci['withdraw_sum_all'])+","+str(podaci['withdraw_users_all'])+","+str(podaci['withdraw_number_all'])+","+str(podaci['withdraw_sum_bank'])+","+str(podaci['withdraw_users_bank'])+","+str(podaci['withdraw_number_bank'])+","+str(podaci['withdraw_sum_shops'])+","+str(podaci['withdraw_users_shops'])+","+str(podaci['withdraw_number_shops'])+","+str(podaci['promo_sum'])+","+str(podaci['promo_users'])+","+str(podaci['promo_number'])+","+str(podaci['promo_cost'])+","+str(podaci['actual_std_balance'])+","+str(podaci['actual_promo_balance'])+","+str(podaci['actual_active_std_balance'])+","+str(podaci['actual_active_promo_balance'])+","+str(podaci['permanently_reserved'])+","+str(podaci['temporarely_reserved'])+","+str(podaci['na_per'])+","+str(podaci['na_tem'])+","+"'"+podaci['execution_time']+"')"
            mycursor.execute(sql_insert_data)
            self.mydb.commit()     
        
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
