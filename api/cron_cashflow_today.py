from db import Db
from flask import request
from flask_restful import Resource
import json
import mysql.connector
import os
from datetime import datetime, time, timedelta

def noneEncapsulator(arg):
    return float(0) if not arg else float(arg)

with open(os.path.join(dir_path, 'cashflow_process.json')) as jsonfile:
    r = json.load(jsonfile)

if r['is_process_running']==0:
    with open(os.path.join(dir_path, 'cashflow_process.json'), 'w') as outfile:
        json.dump({"is_process_running":1}, outfile)
    db = Db()
    mydb = mysql.connector.connect(
            host="localhost",
            user="m.djacic",
            password="Soccer123",
            database="reporting",
            buffered=True,
            auth_plugin='mysql_native_password'
    )


    sql_actual_date = 'select date from ActualDate'
    mycursor = mydb.cursor()
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
            mydb.commit()
            startDate = (datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+str(" 08:00:00")

    if not lastMinute:
        endDate = (datetime.today()+timedelta(hours=2)-timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
        

    if lastMinute:
        with db.engine.begin() as conn:
            podaci = None
            result = conn.execute(
            'exec dbo.m_todayCashflow @from="'+str(startDate)+'", @to="'+str(endDate)+'"')
            db.__del__()
            if result is None:
                result = []
            for obj in result:
                podaci = {
                    'Datum':startDate,
                    'deposit_sum_all':noneEncapsulator(obj['deposit_sum_all']),
                    'deposit_users_all':noneEncapsulator(obj['deposit_users_all']),
                    'deposit_number_all':noneEncapsulator(obj['deposit_number_all']),
                    'deposit_sum_bank':noneEncapsulator(obj['deposit_sum_bank']),
                    'deposit_users_bank':noneEncapsulator(obj['deposit_users_bank']),
                    'deposit_number_bank':noneEncapsulator(obj['deposit_number_bank']),
                    'deposit_sum_cc':noneEncapsulator(obj['deposit_sum_cc']),
                    'deposit_users_cc':noneEncapsulator(obj['deposit_users_cc']),
                    'deposit_number_cc':noneEncapsulator(obj['deposit_number_cc']),
                    'deposit_sum_ipay':noneEncapsulator(obj['deposit_sum_ipay']),
                    'deposit_users_ipay':noneEncapsulator(obj['deposit_users_ipay']),
                    'deposit_number_ipay':noneEncapsulator(obj['deposit_number_ipay']),
                    'deposit_sum_komsija':noneEncapsulator(obj['deposit_sum_komsija']),
                    'deposit_users_komsija':noneEncapsulator(obj['deposit_users_komsija']),
                    'deposit_number_komsija':noneEncapsulator(obj['deposit_number_komsija']),
                    'deposit_sum_shops':noneEncapsulator(obj['deposit_sum_shops']),
                    'deposit_users_shops':noneEncapsulator(obj['deposit_users_shops']),
                    'deposit_number_shops':noneEncapsulator(obj['deposit_number_shops']),
                    'withdraw_sum_all':noneEncapsulator(obj['withdraw_sum_all']),
                    'withdraw_users_all':noneEncapsulator(obj['withdraw_users_all']),
                    'withdraw_number_all':noneEncapsulator(obj['withdraw_number_all']),
                    'withdraw_sum_bank':noneEncapsulator(obj['withdraw_sum_bank']),
                    'withdraw_users_bank':noneEncapsulator(obj['withdraw_users_bank']),
                    'withdraw_number_bank':noneEncapsulator(obj['withdraw_number_bank']),
                    'withdraw_sum_shops':noneEncapsulator(obj['withdraw_sum_shops']),
                    'withdraw_users_shops':noneEncapsulator(obj['withdraw_users_shops']),
                    'withdraw_number_shops':noneEncapsulator(obj['withdraw_number_shops']),
                    'promo_sum':noneEncapsulator(obj['promo_sum']),
                    'promo_users':noneEncapsulator(obj['promo_users']),
                    'promo_number':noneEncapsulator(obj['promo_number']),
                    'promo_cost':noneEncapsulator(obj['promo_cost']),
                    'actual_std_balance':noneEncapsulator(obj['actual_std_balance']),
                    'actual_promo_balance':noneEncapsulator(obj['actual_promo_balance']),
                    'actual_active_std_balance':noneEncapsulator(obj['actual_active_std_balance']),
                    'actual_active_promo_balance':noneEncapsulator(obj['actual_active_promo_balance']),
                    'permanently_reserved':noneEncapsulator(obj['permanently_reserved']),
                    'temporarely_reserved':noneEncapsulator(obj['temporarely_reserved']),
                    'na_per':noneEncapsulator(obj['na_per']),
                    'na_tem':noneEncapsulator(obj['na_tem']),
                    'execution_time':endDate
                }

            sql_update_actual_date = "UPDATE ExecutionTimes set last_execution_time='"+endDate+"' where id=1"
            mycursor.execute(sql_update_actual_date)
            mydb.commit()
            sql_insert_data = "insert into TodayData values('"+startDate+"',"+str(podaci['deposit_sum_all'])+","+str(podaci['deposit_users_all'])+","+str(podaci['deposit_number_all'])+","+str(podaci['deposit_sum_bank'])+","+str(podaci['deposit_users_bank'])+","+str(podaci['deposit_number_bank'])+","+str(podaci['deposit_sum_cc'])+","+str(podaci['deposit_users_cc'])+","+str(podaci['deposit_number_cc'])+","+str(podaci['deposit_sum_ipay'])+","+str(podaci['deposit_users_ipay'])+","+str(podaci['deposit_number_ipay'])+","+str(podaci['deposit_sum_komsija'])+","+str(podaci['deposit_users_komsija'])+","+str(podaci['deposit_number_komsija'])+","+str(podaci['deposit_sum_shops'])+","+str(podaci['deposit_users_shops'])+","+str(podaci['deposit_number_shops'])+","+str(podaci['withdraw_sum_all'])+","+str(podaci['withdraw_users_all'])+","+str(podaci['withdraw_number_all'])+","+str(podaci['withdraw_sum_bank'])+","+str(podaci['withdraw_users_bank'])+","+str(podaci['withdraw_number_bank'])+","+str(podaci['withdraw_sum_shops'])+","+str(podaci['withdraw_users_shops'])+","+str(podaci['withdraw_number_shops'])+","+str(podaci['promo_sum'])+","+str(podaci['promo_users'])+","+str(podaci['promo_number'])+","+str(podaci['promo_cost'])+","+str(podaci['actual_std_balance'])+","+str(podaci['actual_promo_balance'])+","+str(podaci['actual_active_std_balance'])+","+str(podaci['actual_active_promo_balance'])+","+str(podaci['permanently_reserved'])+","+str(podaci['temporarely_reserved'])+","+str(podaci['na_per'])+","+str(podaci['na_tem'])+","+"'"+podaci['execution_time']+"')"
            mycursor.execute(sql_insert_data)
            mydb.commit()
            with open(os.path.join(dir_path, 'cashflow_process.json'), 'w') as outfile:
                json.dump({"is_process_running":0}, outfile)
else:
    with open(os.path.join(dir_path, 'procedure_log.txt'), 'a') as outfile:
        outfile.write("Pokusaj duplog pokretanja")
