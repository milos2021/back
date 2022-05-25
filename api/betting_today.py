from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
import json
import mysql.connector
import os
from datetime import datetime, time, timedelta




class BettingToday(Resource):

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
        yesterday_flag = data['yesterday']
        
        sql_actual_date = 'select date from ActualBettingDate'
        mycursor = self.mydb.cursor()
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
                self.mydb.commit()
                startDate = (datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+str(" 08:00:00")
                yesterday = (datetime.today()+timedelta(hours=2)-timedelta(days=1)).strftime('%Y-%m-%d')+str(" 08:00:00")

        if not lastMinute:
            endDate = (datetime.today()+timedelta(hours=2)-timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
        
        last_execution_time_sql = "select last_execution_time from BettingExecutionTimes where id=1"
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
                'exec dbo.m_bettingToday @today="'+str(startDate)+'", @yesterday="'+str(yesterday)+'", @tomorrow="'+str(endDate)+'"')
                self.db.__del__()
                if result is None:
                    result = []
                for obj in result:
                    podaci = {
                        'datum':startDate,
                        'turnover_overall_users':self.noneEncapsulator(obj['turnover_overall_users']),
                        'turnover_overall_num_bet':self.noneEncapsulator(obj['turnover_overall_num_bet']),
                        'turnover_overall_sum_bet':self.noneEncapsulator(obj['turnover_overall_sum_bet']),
                        'turnover_prematch_users':self.noneEncapsulator(obj['turnover_prematch_users']),
                        'turnover_prematch_num_bet':self.noneEncapsulator(obj['turnover_prematch_num_bet']),
                        'turnover_prematch_sum_bet':self.noneEncapsulator(obj['turnover_prematch_sum_bet']),
                        'turnover_live_users':self.noneEncapsulator(obj['turnover_live_users']),
                        'turnover_live_num_bet':self.noneEncapsulator(obj['turnover_live_num_bet']),
                        'turnover_live_sum_bet':self.noneEncapsulator(obj['turnover_live_sum_bet']),
                        'turnover_mixed_users':self.noneEncapsulator(obj['turnover_mixed_users']),
                        'turnover_mixed_num_bet':self.noneEncapsulator(obj['turnover_mixed_num_bet']),
                        'turnover_mixed_sum_bet':self.noneEncapsulator(obj['turnover_mixed_sum_bet']),
                        'turnover_outright_users':self.noneEncapsulator(obj['turnover_outright_users']),
                        'turnover_outright_num_bet':self.noneEncapsulator(obj['turnover_outright_num_bet']),
                        'turnover_outright_sum_bet':self.noneEncapsulator(obj['turnover_outright_sum_bet']),
                        'active_turnover_overall_users':self.noneEncapsulator(obj['active_turnover_overall_users']),
                        'active_turnover_overall_num_bet':self.noneEncapsulator(obj['active_turnover_overall_num_bet']),
                        'active_turnover_overall_sum_bet':self.noneEncapsulator(obj['active_turnover_overall_sum_bet']),
                        'active_turnover_users_today':self.noneEncapsulator(obj['active_turnover_users_today']),
                        'active_turnover_users_yesterday':self.noneEncapsulator(obj['active_turnover_users_yesterday']),
                        'active_turnover_users_two_plus':self.noneEncapsulator(obj['active_turnover_users_two_plus']),
                        'active_turnover_num_bet_today':self.noneEncapsulator(obj['active_turnover_num_bet_today']),
                        'active_turnover_num_bet_yesterday':self.noneEncapsulator(obj['active_turnover_num_bet_yesterday']),
                        'active_turnover_num_bet_two_plus':self.noneEncapsulator(obj['active_turnover_num_bet_two_plus']),
                        'active_turnover_sum_bet_today':self.noneEncapsulator(obj['active_turnover_sum_bet_today']),
                        'active_turnover_sum_bet_yesterday':self.noneEncapsulator(obj['active_turnover_sum_bet_yesterday']),
                        'active_turnover_sum_bet_two_plus':self.noneEncapsulator(obj['active_turnover_sum_bet_two_plus']),
                        'active_turnover_users_prematch':self.noneEncapsulator(obj['active_turnover_users_prematch']),
                        'active_turnover_users_live':self.noneEncapsulator(obj['active_turnover_users_live']),
                        'active_turnover_users_mixed':self.noneEncapsulator(obj['active_turnover_users_mixed']),
                        'active_turnover_users_outright':self.noneEncapsulator(obj['active_turnover_users_outright']),
                        'active_turnover_num_bet_prematch':self.noneEncapsulator(obj['active_turnover_num_bet_prematch']),
                        'active_turnover_num_bet_live':self.noneEncapsulator(obj['active_turnover_num_bet_live']),
                        'active_turnover_num_bet_mixed':self.noneEncapsulator(obj['active_turnover_num_bet_mixed']),
                        'active_turnover_num_bet_outright':self.noneEncapsulator(obj['active_turnover_num_bet_outright']),
                        'active_turnover_sum_bet_prematch':self.noneEncapsulator(obj['active_turnover_sum_bet_prematch']),
                        'active_turnover_sum_bet_live':self.noneEncapsulator(obj['active_turnover_sum_bet_live']),
                        'active_turnover_sum_bet_mixed':self.noneEncapsulator(obj['active_turnover_sum_bet_mixed']),
                        'active_turnover_sum_bet_outright':self.noneEncapsulator(obj['active_turnover_sum_bet_outright']),
                        'winnings_overall_users':self.noneEncapsulator(obj['winnings_overall_users']),
                        'winnings_overall_num_bet':self.noneEncapsulator(obj['winnings_overall_num_bet']),
                        'winnings_overall_sum_bet':self.noneEncapsulator(obj['winnings_overall_sum_bet']),
                        'winnings_users_prematch':self.noneEncapsulator(obj['winnings_users_prematch']),
                        'winnings_num_bet_prematch':self.noneEncapsulator(obj['winnings_num_bet_prematch']),
                        'winnings_sum_bet_prematch':self.noneEncapsulator(obj['winnings_sum_bet_prematch']),
                        'winnings_users_live':self.noneEncapsulator(obj['winnings_users_live']),
                        'winnings_num_bet_live':self.noneEncapsulator(obj['winnings_num_bet_live']),
                        'winnings_sum_bet_live':self.noneEncapsulator(obj['winnings_sum_bet_live']),
                        'winnings_users_mixed':self.noneEncapsulator(obj['winnings_users_mixed']),
                        'winnings_num_bet_mixed':self.noneEncapsulator(obj['winnings_num_bet_mixed']),
                        'winnings_sum_bet_mixed':self.noneEncapsulator(obj['winnings_sum_bet_mixed']),
                        'winnings_users_outright':self.noneEncapsulator(obj['winnings_users_outright']),
                        'winnings_num_bet_outright':self.noneEncapsulator(obj['winnings_num_bet_outright']),
                        'winnings_sum_bet_outright':self.noneEncapsulator(obj['winnings_sum_bet_outright']),
                        'today_win':self.noneEncapsulator(obj['today_win']),
                        'today_win_prematch':self.noneEncapsulator(obj['today_win_prematch']),
                        'today_win_live':self.noneEncapsulator(obj['today_win_live']),
                        'today_win_mixed':self.noneEncapsulator(obj['today_win_mixed']),
                        'today_win_outright':self.noneEncapsulator(obj['today_win_outright']),
                        'execution_time':endDate
                    }

            sql_update_actual_date = "UPDATE BettingExecutionTimes set last_execution_time='"+endDate+"' where id=1"
            mycursor.execute(sql_update_actual_date)
            self.mydb.commit()
            sql_insert_data = "insert into TodayBettingData values("+str(podaci['turnover_overall_users'])+","+str(podaci['turnover_overall_num_bet'])+","+str(podaci['turnover_overall_sum_bet'])+","+str(podaci['turnover_prematch_users'])+","+str(podaci['turnover_prematch_num_bet'])+","+str(podaci['turnover_prematch_sum_bet'])+","+str(podaci['turnover_live_users'])+","+str(podaci['turnover_live_num_bet'])+","+str(podaci['turnover_live_sum_bet'])+","+str(podaci['turnover_mixed_users'])+","+str(podaci['turnover_mixed_num_bet'])+","+str(podaci['turnover_mixed_sum_bet'])+","+str(podaci['turnover_outright_users'])+","+str(podaci['turnover_outright_num_bet'])+","+str(podaci['turnover_outright_sum_bet'])+","+str(podaci['active_turnover_overall_users'])+","+str(podaci['active_turnover_overall_num_bet'])+","+str(podaci['active_turnover_overall_sum_bet'])+","+str(podaci['active_turnover_users_today'])+","+str(podaci['active_turnover_users_yesterday'])+","+str(podaci['active_turnover_users_two_plus'])+","+str(podaci['active_turnover_num_bet_today'])+","+str(podaci['active_turnover_num_bet_yesterday'])+","+str(podaci['active_turnover_num_bet_two_plus'])+","+str(podaci['active_turnover_sum_bet_today'])+","+str(podaci['active_turnover_sum_bet_yesterday'])+","+str(podaci['active_turnover_sum_bet_two_plus'])+","+str(podaci['active_turnover_users_prematch'])+","+str(podaci['active_turnover_users_live'])+","+str(podaci['active_turnover_users_mixed'])+","+str(podaci['active_turnover_users_outright'])+","+str(podaci['active_turnover_num_bet_prematch'])+","+str(podaci['active_turnover_num_bet_live'])+","+str(podaci['active_turnover_num_bet_mixed'])+","+str(podaci['active_turnover_num_bet_outright'])+","+str(podaci['active_turnover_sum_bet_prematch'])+","+str(podaci['active_turnover_sum_bet_live'])+","+str(podaci['active_turnover_sum_bet_mixed'])+","+str(podaci['active_turnover_sum_bet_outright'])+","+str(podaci['winnings_overall_users'])+","+str(podaci['winnings_overall_num_bet'])+","+str(podaci['winnings_overall_sum_bet'])+","+str(podaci['winnings_users_prematch'])+","+str(podaci['winnings_num_bet_prematch'])+","+str(podaci['winnings_sum_bet_prematch'])+","+str(podaci['winnings_users_live'])+","+str(podaci['winnings_num_bet_live'])+","+str(podaci['winnings_sum_bet_live'])+","+str(podaci['winnings_users_mixed'])+","+str(podaci['winnings_num_bet_mixed'])+","+str(podaci['winnings_sum_bet_mixed'])+","+str(podaci['winnings_users_outright'])+","+str(podaci['winnings_num_bet_outright'])+","+str(podaci['winnings_sum_bet_outright'])+","+str(podaci['today_win'])+","+str(podaci['today_win_prematch'])+","+str(podaci['today_win_live'])+","+str(podaci['today_win_mixed'])+","+str(podaci['today_win_outright'])+","+"'"+podaci['datum']+"',"+"'"+podaci['execution_time']+"')"
            mycursor.execute(sql_insert_data)
            self.mydb.commit()
            
        if not yesterday_flag:
            sql_data = 'SELECT * FROM `TodayBettingData` order by execution_time desc limit 1'
        else:
            if time(0,0) <= (datetime.now()+timedelta(hours=2)).time() <= time(8,0):
                juce = (datetime.today()+timedelta(hours=2)-timedelta(days=2)).strftime('%Y-%m-%d')+str(" 08:00:00")
            else:
                juce = (datetime.today()+timedelta(hours=2)-timedelta(days=1)).strftime('%Y-%m-%d')+str(" 08:00:00")
            sql_data = 'SELECT * FROM `TodayBettingData` where datum="'+str(juce)+'" order by execution_time desc limit 1'
        mycursor = self.mydb.cursor()
        mycursor.execute(sql_data)
        result = mycursor.fetchall()
        data = []
        one = {}
        for obj in result:
            podaci = {
                'turnover_overall_users':self.noneEncapsulator(obj[0]),
                'turnover_overall_num_bet':self.noneEncapsulator(obj[1]),
                'turnover_overall_sum_bet':self.noneEncapsulator(obj[2]),
                'turnover_prematch_users':self.noneEncapsulator(obj[3]),
                'turnover_prematch_num_bet':self.noneEncapsulator(obj[4]),
                'turnover_prematch_sum_bet':self.noneEncapsulator(obj[5]),
                'turnover_live_users':self.noneEncapsulator(obj[6]),
                'turnover_live_num_bet':self.noneEncapsulator(obj[7]),
                'turnover_live_sum_bet':self.noneEncapsulator(obj[8]),
                'turnover_mixed_users':self.noneEncapsulator(obj[9]),
                'turnover_mixed_num_bet':self.noneEncapsulator(obj[10]),
                'turnover_mixed_sum_bet':self.noneEncapsulator(obj[11]),
                'turnover_outright_users':self.noneEncapsulator(obj[12]),
                'turnover_outright_num_bet':self.noneEncapsulator(obj[13]),
                'turnover_outright_sum_bet':self.noneEncapsulator(obj[14]),
                'active_turnover_overall_users':self.noneEncapsulator(obj[15]),
                'active_turnover_overall_num_bet':self.noneEncapsulator(obj[16]),
                'active_turnover_overall_sum_bet':self.noneEncapsulator(obj[17]),
                'active_turnover_users_today':self.noneEncapsulator(obj[18]),
                'active_turnover_users_yesterday':self.noneEncapsulator(obj[19]),
                'active_turnover_users_two_plus':self.noneEncapsulator(obj[20]),
                'active_turnover_num_bet_today':self.noneEncapsulator(obj[21]),
                'active_turnover_num_bet_yesterday':self.noneEncapsulator(obj[22]),
                'active_turnover_num_bet_two_plus':self.noneEncapsulator(obj[23]),
                'active_turnover_sum_bet_today':self.noneEncapsulator(obj[24]),
                'active_turnover_sum_bet_yesterday':self.noneEncapsulator(obj[25]),
                'active_turnover_sum_bet_two_plus':self.noneEncapsulator(obj[26]),
                'active_turnover_users_prematch':self.noneEncapsulator(obj[27]),
                'active_turnover_users_live':self.noneEncapsulator(obj[28]),
                'active_turnover_users_mixed':self.noneEncapsulator(obj[29]),
                'active_turnover_users_outright':self.noneEncapsulator(obj[30]),
                'active_turnover_num_bet_prematch':self.noneEncapsulator(obj[31]),
                'active_turnover_num_bet_live':self.noneEncapsulator(obj[32]),
                'active_turnover_num_bet_mixed':self.noneEncapsulator(obj[33]),
                'active_turnover_num_bet_outright':self.noneEncapsulator(obj[34]),
                'active_turnover_sum_bet_prematch':self.noneEncapsulator(obj[35]),
                'active_turnover_sum_bet_live':self.noneEncapsulator(obj[36]),
                'active_turnover_sum_bet_mixed':self.noneEncapsulator(obj[37]),
                'active_turnover_sum_bet_outright':self.noneEncapsulator(obj[38]),
                'winnings_overall_users':self.noneEncapsulator(obj[39]),
                'winnings_overall_num_bet':self.noneEncapsulator(obj[40]),
                'winnings_overall_sum_bet':self.noneEncapsulator(obj[41]),
                'winnings_users_prematch':self.noneEncapsulator(obj[42]),
                'winnings_num_bet_prematch':self.noneEncapsulator(obj[43]),
                'winnings_sum_bet_prematch':self.noneEncapsulator(obj[44]),
                'winnings_users_live':self.noneEncapsulator(obj[45]),
                'winnings_num_bet_live':self.noneEncapsulator(obj[46]),
                'winnings_sum_bet_live':self.noneEncapsulator(obj[47]),
                'winnings_users_mixed':self.noneEncapsulator(obj[48]),
                'winnings_num_bet_mixed':self.noneEncapsulator(obj[49]),
                'winnings_sum_bet_mixed':self.noneEncapsulator(obj[50]),
                'winnings_users_outright':self.noneEncapsulator(obj[51]),
                'winnings_num_bet_outright':self.noneEncapsulator(obj[52]),
                'winnings_sum_bet_outright':self.noneEncapsulator(obj[53]),
                'today_win':self.noneEncapsulator(obj[54]),
                'today_win_prematch':self.noneEncapsulator(obj[55]),
                'today_win_live':self.noneEncapsulator(obj[56]),
                'today_win_mixed':self.noneEncapsulator(obj[57]),
                'today_win_outright':self.noneEncapsulator(obj[58]),
                'datum':obj[59],
                'execution_time':obj[60]
                
            }
            data.append(podaci)
                
        return {"data":data}, 200
