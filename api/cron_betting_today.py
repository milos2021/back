from db import Db
from flask import request
from flask_restful import Resource
import json
import mysql.connector
import os
from datetime import datetime, time, timedelta


def noneEncapsulator(arg):
    return float(0) if not arg else float(arg)

with open(os.path.join(dir_path, 'betting_process.json')) as jsonfile:
    r = json.load(jsonfile)

if r['is_process_running']==0:
    with open(os.path.join(dir_path, 'betting_process.json'), 'w') as outfile:
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
    
    sql_actual_date = 'select date from ActualBettingDate'
    mycursor = mydb.cursor()
    mycursor.execute(sql_actual_date)
    actual_date = mycursor.fetchall()[0][0] #2021-10-01
    startDate = None
    endDate = None
    yesterday = None
    hours = (datetime.today()+timedelta(hours=2)).strftime('%H') #11
    minutes = (datetime.today()+timedelta(hours=2)).strftime('%M') #30
    lastMinute = False
    #ako je trenutno vreme izmedju ponoci i osam ujutru iduceg dana, dan pocetka je prethodni dan u 8 ujutru
    if time(0,0) <= (datetime.now()+timedelta(hours=2)).time() <= time(8,0):
        startDate = (datetime.today()+timedelta(hours=2)-timedelta(days=1)).strftime('%Y-%m-%d')+str(" 08:00:00")
        yesterday = (datetime.today()+timedelta(hours=2)-timedelta(days=2)).strftime('%Y-%m-%d')+str(" 08:00:00")
    else:
        #ako nije, porede se aktuelni dan u bazi i trenutni dan, ako su isti pocetak je trenutni dan u 8 ujutru
        if datetime.strptime(actual_date, '%Y-%m-%d').day == (datetime.today()+timedelta(hours=2)).day:
            startDate = (datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+str(" 08:00:00")
            yesterday = (datetime.today()+timedelta(hours=2)-timedelta(days=1)).strftime('%Y-%m-%d')+str(" 08:00:00")
            #u prvoj iteraciji novog dana, se osigurava da je prethodni zavrsen kako treba
            if (datetime.now()+timedelta(hours=2)).time().strftime('%H') == '08' and int((datetime.now()+timedelta(hours=2)).time().strftime('%M'))>1 and int((datetime.now()+timedelta(hours=2)).time().strftime('%M'))<8:
                lastMinute = True
                startDate = (datetime.today()+timedelta(hours=2)-timedelta(days=1)).strftime('%Y-%m-%d')+str(" 08:00:00")
                yesterday = (datetime.today()+timedelta(hours=2)-timedelta(days=2)).strftime('%Y-%m-%d')+str(" 08:00:00")
                endDate = (datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+str(" 07:59:59")
        else:
            #ako nisu isti, aktuelni dan se postavlja na trenutni dan
            sql_update_actual_date = "UPDATE ActualBettingDate set date='"+(datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+"' where id=1"
            mycursor.execute(sql_update_actual_date)
            mydb.commit()
            startDate = (datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+str(" 08:00:00")
            yesterday = (datetime.today()+timedelta(hours=2)-timedelta(days=1)).strftime('%Y-%m-%d')+str(" 08:00:00")

    if not lastMinute:
        endDate = (datetime.today()+timedelta(hours=2)-timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')

    if lastMinute:
        with db.engine.begin() as conn:
            podaci = None
            result = conn.execute(
            'exec dbo.m_bettingToday @today="'+str(startDate)+'", @yesterday="'+str(yesterday)+'", @tomorrow="'+str(endDate)+'"')
            db.__del__()
            if result is None:
                result = []
            for obj in result:
                podaci = {
                    'datum':startDate,
                    'turnover_overall_users':noneEncapsulator(obj['turnover_overall_users']),
                    'turnover_overall_num_bet':noneEncapsulator(obj['turnover_overall_num_bet']),
                    'turnover_overall_sum_bet':noneEncapsulator(obj['turnover_overall_sum_bet']),
                    'turnover_prematch_users':noneEncapsulator(obj['turnover_prematch_users']),
                    'turnover_prematch_num_bet':noneEncapsulator(obj['turnover_prematch_num_bet']),
                    'turnover_prematch_sum_bet':noneEncapsulator(obj['turnover_prematch_sum_bet']),
                    'turnover_live_users':noneEncapsulator(obj['turnover_live_users']),
                    'turnover_live_num_bet':noneEncapsulator(obj['turnover_live_num_bet']),
                    'turnover_live_sum_bet':noneEncapsulator(obj['turnover_live_sum_bet']),
                    'turnover_mixed_users':noneEncapsulator(obj['turnover_mixed_users']),
                    'turnover_mixed_num_bet':noneEncapsulator(obj['turnover_mixed_num_bet']),
                    'turnover_mixed_sum_bet':noneEncapsulator(obj['turnover_mixed_sum_bet']),
                    'turnover_outright_users':noneEncapsulator(obj['turnover_outright_users']),
                    'turnover_outright_num_bet':noneEncapsulator(obj['turnover_outright_num_bet']),
                    'turnover_outright_sum_bet':noneEncapsulator(obj['turnover_outright_sum_bet']),
                    'active_turnover_overall_users':noneEncapsulator(obj['active_turnover_overall_users']),
                    'active_turnover_overall_num_bet':noneEncapsulator(obj['active_turnover_overall_num_bet']),
                    'active_turnover_overall_sum_bet':noneEncapsulator(obj['active_turnover_overall_sum_bet']),
                    'active_turnover_users_today':noneEncapsulator(obj['active_turnover_users_today']),
                    'active_turnover_users_yesterday':noneEncapsulator(obj['active_turnover_users_yesterday']),
                    'active_turnover_users_two_plus':noneEncapsulator(obj['active_turnover_users_two_plus']),
                    'active_turnover_num_bet_today':noneEncapsulator(obj['active_turnover_num_bet_today']),
                    'active_turnover_num_bet_yesterday':noneEncapsulator(obj['active_turnover_num_bet_yesterday']),
                    'active_turnover_num_bet_two_plus':noneEncapsulator(obj['active_turnover_num_bet_two_plus']),
                    'active_turnover_sum_bet_today':noneEncapsulator(obj['active_turnover_sum_bet_today']),
                    'active_turnover_sum_bet_yesterday':noneEncapsulator(obj['active_turnover_sum_bet_yesterday']),
                    'active_turnover_sum_bet_two_plus':noneEncapsulator(obj['active_turnover_sum_bet_two_plus']),
                    'active_turnover_users_prematch':noneEncapsulator(obj['active_turnover_users_prematch']),
                    'active_turnover_users_live':noneEncapsulator(obj['active_turnover_users_live']),
                    'active_turnover_users_mixed':noneEncapsulator(obj['active_turnover_users_mixed']),
                    'active_turnover_users_outright':noneEncapsulator(obj['active_turnover_users_outright']),
                    'active_turnover_num_bet_prematch':noneEncapsulator(obj['active_turnover_num_bet_prematch']),
                    'active_turnover_num_bet_live':noneEncapsulator(obj['active_turnover_num_bet_live']),
                    'active_turnover_num_bet_mixed':noneEncapsulator(obj['active_turnover_num_bet_mixed']),
                    'active_turnover_num_bet_outright':noneEncapsulator(obj['active_turnover_num_bet_outright']),
                    'active_turnover_sum_bet_prematch':noneEncapsulator(obj['active_turnover_sum_bet_prematch']),
                    'active_turnover_sum_bet_live':noneEncapsulator(obj['active_turnover_sum_bet_live']),
                    'active_turnover_sum_bet_mixed':noneEncapsulator(obj['active_turnover_sum_bet_mixed']),
                    'active_turnover_sum_bet_outright':noneEncapsulator(obj['active_turnover_sum_bet_outright']),
                    'winnings_overall_users':noneEncapsulator(obj['winnings_overall_users']),
                    'winnings_overall_num_bet':noneEncapsulator(obj['winnings_overall_num_bet']),
                    'winnings_overall_sum_bet':noneEncapsulator(obj['winnings_overall_sum_bet']),
                    'winnings_users_prematch':noneEncapsulator(obj['winnings_users_prematch']),
                    'winnings_num_bet_prematch':noneEncapsulator(obj['winnings_num_bet_prematch']),
                    'winnings_sum_bet_prematch':noneEncapsulator(obj['winnings_sum_bet_prematch']),
                    'winnings_users_live':noneEncapsulator(obj['winnings_users_live']),
                    'winnings_num_bet_live':noneEncapsulator(obj['winnings_num_bet_live']),
                    'winnings_sum_bet_live':noneEncapsulator(obj['winnings_sum_bet_live']),
                    'winnings_users_mixed':noneEncapsulator(obj['winnings_users_mixed']),
                    'winnings_num_bet_mixed':noneEncapsulator(obj['winnings_num_bet_mixed']),
                    'winnings_sum_bet_mixed':noneEncapsulator(obj['winnings_sum_bet_mixed']),
                    'winnings_users_outright':noneEncapsulator(obj['winnings_users_outright']),
                    'winnings_num_bet_outright':noneEncapsulator(obj['winnings_num_bet_outright']),
                    'winnings_sum_bet_outright':noneEncapsulator(obj['winnings_sum_bet_outright']),
                    'today_win':noneEncapsulator(obj['today_win']),
                    'today_win_prematch':noneEncapsulator(obj['today_win_prematch']),
                    'today_win_live':noneEncapsulator(obj['today_win_live']),
                    'today_win_mixed':noneEncapsulator(obj['today_win_mixed']),
                    'today_win_outright':noneEncapsulator(obj['today_win_outright']),
                    'execution_time':endDate
                }

        sql_update_actual_date = "UPDATE BettingExecutionTimes set last_execution_time='"+endDate+"' where id=1"
        mycursor.execute(sql_update_actual_date)
        mydb.commit()
        sql_insert_data = "insert into TodayBettingData values("+str(podaci['turnover_overall_users'])+","+str(podaci['turnover_overall_num_bet'])+","+str(podaci['turnover_overall_sum_bet'])+","+str(podaci['turnover_prematch_users'])+","+str(podaci['turnover_prematch_num_bet'])+","+str(podaci['turnover_prematch_sum_bet'])+","+str(podaci['turnover_live_users'])+","+str(podaci['turnover_live_num_bet'])+","+str(podaci['turnover_live_sum_bet'])+","+str(podaci['turnover_mixed_users'])+","+str(podaci['turnover_mixed_num_bet'])+","+str(podaci['turnover_mixed_sum_bet'])+","+str(podaci['turnover_outright_users'])+","+str(podaci['turnover_outright_num_bet'])+","+str(podaci['turnover_outright_sum_bet'])+","+str(podaci['active_turnover_overall_users'])+","+str(podaci['active_turnover_overall_num_bet'])+","+str(podaci['active_turnover_overall_sum_bet'])+","+str(podaci['active_turnover_users_today'])+","+str(podaci['active_turnover_users_yesterday'])+","+str(podaci['active_turnover_users_two_plus'])+","+str(podaci['active_turnover_num_bet_today'])+","+str(podaci['active_turnover_num_bet_yesterday'])+","+str(podaci['active_turnover_num_bet_two_plus'])+","+str(podaci['active_turnover_sum_bet_today'])+","+str(podaci['active_turnover_sum_bet_yesterday'])+","+str(podaci['active_turnover_sum_bet_two_plus'])+","+str(podaci['active_turnover_users_prematch'])+","+str(podaci['active_turnover_users_live'])+","+str(podaci['active_turnover_users_mixed'])+","+str(podaci['active_turnover_users_outright'])+","+str(podaci['active_turnover_num_bet_prematch'])+","+str(podaci['active_turnover_num_bet_live'])+","+str(podaci['active_turnover_num_bet_mixed'])+","+str(podaci['active_turnover_num_bet_outright'])+","+str(podaci['active_turnover_sum_bet_prematch'])+","+str(podaci['active_turnover_sum_bet_live'])+","+str(podaci['active_turnover_sum_bet_mixed'])+","+str(podaci['active_turnover_sum_bet_outright'])+","+str(podaci['winnings_overall_users'])+","+str(podaci['winnings_overall_num_bet'])+","+str(podaci['winnings_overall_sum_bet'])+","+str(podaci['winnings_users_prematch'])+","+str(podaci['winnings_num_bet_prematch'])+","+str(podaci['winnings_sum_bet_prematch'])+","+str(podaci['winnings_users_live'])+","+str(podaci['winnings_num_bet_live'])+","+str(podaci['winnings_sum_bet_live'])+","+str(podaci['winnings_users_mixed'])+","+str(podaci['winnings_num_bet_mixed'])+","+str(podaci['winnings_sum_bet_mixed'])+","+str(podaci['winnings_users_outright'])+","+str(podaci['winnings_num_bet_outright'])+","+str(podaci['winnings_sum_bet_outright'])+","+str(podaci['today_win'])+","+str(podaci['today_win_prematch'])+","+str(podaci['today_win_live'])+","+str(podaci['today_win_mixed'])+","+str(podaci['today_win_outright'])+","+"'"+podaci['datum']+"',"+"'"+podaci['execution_time']+"')"
        mycursor.execute(sql_insert_data)
        mydb.commit()
        with open(os.path.join(dir_path, 'betting_process.json'), 'w') as outfile:
            json.dump({"is_process_running":0}, outfile)
else:
    with open(os.path.join(dir_path, 'procedure_log.txt'), 'a') as outfile:
        outfile.write("Pokusaj duplog pokretanja")
