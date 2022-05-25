import os
import sys
import dateparser
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json
import time
import mysql.connector
import os
from betradar_mapping import extractTotal, extractHandicap, extract1X2
from asian import oddsJson, calculateOddsDiff
import requests
from datetime import datetime,timedelta
from flask_socketio import SocketIO,emit
import threading
from threading import Thread
delta_hours = 2
mydb = mysql.connector.connect(
            host="10.0.90.252",
            user="statistic",
            password="Soccer123",
            database="lista",
            buffered=True
        )

betradardb = mysql.connector.connect(
            host="10.0.90.251",
            user="statistic",
            password="Soccer123",
            database="kladionica",
            buffered=True
        )

dir_path = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(dir_path, 'process_running.json')) as jsonfile:
    r = json.load(jsonfile)

if r['is_process_running']==0:
    try:
        url = "http://62.138.184.100/backend/export/oddsfeed.php?client=soccerbet"
        r = requests.get(url)
        json_asian = json.loads(r.content)
        #NEPOVEZANI MECEVI
        # mycursor = mydb.cursor()
        # m_check = "select DOMACIN as 'homeCompetitorName', GOST as 'awayCompetitorName', CONCAT(DATUM,' ',VREME) as 'startDate', SIFRA as 'Code', liga, vrsta as 'sport',infogram_mec_id as 'matchId', betradar_id from matches_old where vrsta='FD' and infogram_mec_id is not null and approved=1 and published=1 and (cast(CONCAT(DATUM,' ',VREME) as datetime) >= '"+str(datetime.now()+timedelta(hours=delta_hours))+"') order by DATUM asc"

        #PRODUKCIJA
        mycursor = mydb.cursor()
        m_check = "select DOMACIN as 'homeCompetitorName', GOST as 'awayCompetitorName', CONCAT(DATUM,' ',VREME) as 'startDate', SIFRA as 'Code', liga, vrsta as 'sport',infogram_mec_id as 'matchId', betradar_id from matches_old where vrsta='FD' and infogram_mec_id is not null and approved=1 and published=1 and (cast(CONCAT(DATUM,' ',VREME) as datetime) >= '"+str(datetime.now()+timedelta(hours=delta_hours))+"') order by DATUM asc"
        mycursor.execute(m_check)
        m_rows = mycursor.fetchall()
        m_keys = [column[0] for column in mycursor.description]
        mecevi = []
        for row in m_rows:
            mecevi.append(dict(zip(m_keys, row)))

        mycursor = mydb.cursor()
        k_check = "select SIFRA as 'code', CONCAT(DATUM,' ',VREME) as 'startDate',  infogram_mec_id as 'matchId', betradar_id,  `GH3+`, `GG&1T2+`, `1&1T2-3`, `GG1vGG2`, `GG1&3+`, `15M0+2+`, `1TM12`, `G2+`, `15K1`, `G5`, `G4`, `G3`, `2-2&4+`, `G1`, `1&3+`, `2-2&2TM2-3`, `1X-X`, `FG1&G4+`, `T2:4`, `2&2T2+`, `P1X&DX2`, `T2:1`, `T2:2`, `T2:3`, `G5+`, `GAP3+`, `30KX`, `GG`, `1X-1`, `1X-2`, `1&1T2+`, `GN`, `X-2&G36`, `X-2&G34`, `X-2&G35`, `GG&4+`, `DX2&I2+`, `1&I1+`, `1&I>II`, `2-2&2-3`, `1TMI2+&1TM3+`, `T4:2`, `T4:3`, `T4:0`, `T4:1`, `T4:4`, `GG&I1-2`, `II3+`, `GG&I1+`, `1-1&G03`, `1-1&G02`, `DS2`, `I1+&G2+`, `1TM13`, `2&GG2`, `2&GG1`, `X-2&G4+`, `GG&1+1+`, `I1+&II3+`, `P0:0`, `2&4+`, `GA2+`, `GHD1`, `2&I>II`, `nGG2+`, `GA23`, `G2`, `30K2`, `DX2&2+`, `GHD3+`, `2-2&G34`, `D12&GG`, `2-2&G36`, `2t1+2+`, `X-1X`, `GG1&GN2`, `1-1&GN`, `2T1+I&2T2+`, `2-2&I>II`, `D1X&2+`, `G1+`, `2TM13`, `GG2`, `X-1&G02`, `X-1&G03`, `2-2&GN`, `1-1&2+`, `X-X&G2+`, `GHP2+`, `GN1&GG2`, `I1-2&3+`, `2-2&GG`, `2-2&2+`, `FG1&G3+`, `DX2&G23`, `GG&II1+`, `X-12`, `P12&DX2`, `1-1&GG`, `D12&G3+`, `2&G5+`, `X&2+`, `D1X&G3-5`, `1-1&5+`, `D1X&I12`, `DPX`, `X-2&G03`, `X-2&G02`, `D1X&I1+`, `T2:0`, `2-1X`, `GN1&GN2`, `GAP01`, `D12&G4+`, `X-2&HP2`, `I1-3&II1-3`, `1&I2+`, `II1`, `II0`, `II3`, `II2`, `2-2&G45`, `2-2&G46`, `2-2&2TM3+`, `HS2`, `D1X&3+`, `DP2`, `DP1`, `II4+`, `I02`, `I01`, `2-12`, `X2-2`, `I2+vII2+`, `1-12`, `GG&2T2+`, `15M1+0`, `GA2-4`, `I1-2&II1-2`, `30MG1+`, `2&FG2`, `2&FG1`, `1-1&2-3`, `GAD3+`, `GH2+`, `30MG1`, `FG1`, `FG2`, `GG&II2+`, `D12&G3-5`, `D12&G3-6`, `I<II`, `GH23`, `P1:3`, `P1:2`, `P1:1`, `P1:0`, `P3:1`, `P3:0`, `P3:3`, `P3:2`, `2-2&II1+`, `D12&G4-6`, `1-1X`, `2&2T3+`, `G4+`, `DX2&I1+`, `X-X2`, `X2-X`, `1&1T3+`, `DX2&I12`, `GHP12`, `X&FG1`, `X&FG2`, `2-2&5+`, `2+2+`, `1TMI1+&1TM3+`, `1-1&GG1`, `1-1&GG2`, `30M2+0`, `GAD0`, `T0:4`, `X-1&G4+`, `T0:2`, `T0:3`, `T0:0`, `T0:1`, `D12&G03`, `D12&G02`, `1-1&1TM3+`, `15KX`, `I3+`, `D1X&GG`, `PFG2`, `PFG1`, `II02`, `I4+`, `II01`, `I1+&G3+`, `15MG1+`, `15M1+2+`, `X2-1`, `I1+&II2+`, `I>II`, `GA3+`, `D12&I1+II1+`, `DX2&I1+II1+`, `2&I2+`, `GHD2+`, `K2`, `K1`, `DX2&4+`, `ATX`, `T3:1`, `T3:0`, `DX2&3+`, `2-X`, `PD2`, `PD1`, `T3:2`, `2&2T2-3`, `I2+&II1+`, `2-2&G03`, `2-2&G02`, `2-2`, `D12&G2-4`, `AS1`, `D12&G2-6`, `DX2&G2-4`, `DX2&G2-5`, `DX2&G2-6`, `FG2&GG`, `2-1&G5+`, `GN1`, `30M0+1+`, `2TM02&01`, `2TM02&02`, `1-2&G5+`, `AT2`, `GHP1`, `GH2-4`, `KX`, `GAD01`, `D12&G2-5`, `2TM02`, `2TM03`, `AS2`, `X-1&G35`, `X-1&G34`, `X-1&G36`, `1&FG1`, `X-1&G3+`, `2-1`, `X-1&HP1`, `X-1&I2+`, `I2+vG4+`, `FG1&G2+`, `D12&I01`, `2t2+2+`, `2TM01&02`, `1&GG`, `1-1&4+`, `D1X&I2+`, `D1X&I01`, `1-1&I=II`, `GAP12`, `GAP1+`, `SW1`, `SW2`, `I1+`, `2&GG`, `DX2&G0-2`, `DX2&G0-3`, `15M0+1+`, `DX2&G3-5`, `DX2&G3-6`, `X-1&GG`, `DS1`, `P1X&D1X`, `GAP0`, `GAP1`, `12-X`, `15M1+1+`, `15MG2+`, `1-1&G26`, `1-1&G25`, `1-1&G24`, `P1X&D12`, `GG2&3+`, `DX2&G4-6`, `GA01`, `1-1&I<II`, `HS1`, `X-2&II2+`, `1&G5+`, `15MG1`, `15MG0`, `12-2`, `12-1`, `GG1&I3+`, `30MG01`, `GHD12`, `GG&G23`, `W2`, `W1`, `2-2&GG1`, `2-2&GG2`, `2TM4+`, `30K1`, `X-2&G24`, `D1X&G2-6`, `D1X&G2-5`, `D1X&G2-4`, `X-1`, `X-2`, `PX`, `30MGG`, `X-2&G23`, `1T01&01`, `X-1&II2+`, `P2`, `1-1&H1`, `P1`, `AT1`, `G7+`, `GHD0`, `DX2&I01`, `30MG0`, `GHP01`, `1&G2-5`, `1TM02&01`, `1TM02&02`, `GG2+`, `X-X&G0-2`, `X-X`, `1v3+`, `GG2&II3+`, `I23`, `2&I=II`, `I2+`, `FG2&G2+`, `1&GG1`, `1&GG2`, `1-1&I2+`, `II13`, `II12`, `2&G2-6`, `2&G2-4`, `2&G2-5`, `X-1&G24`, `2t2+1+`, `X-1&G25`, `II1+`, `X-1&G23`, `2&I1+`, `1-1&II2+`, `1-X2`, `2-2&II2+`, `1TM01&02`, `D1X`, `1&FG2`, `PX2&D1X`, `30M1+0`, `1&2-3`, `1t2+1+`, `2-X2`, `2-2&I=II`, `2HW2`, `2HW1`, `D1X&G3-6`, `2&2-3`, `D1X&G0-3`, `D1X&G0-2`, `I2+&G4+`, `1-X`, `GG1&GG2`, `GAD1+`, `I1`, `I0`, `I3`, `I2`, `15K2`, `D1X&4+`, `GG2&4+`, `GAD12`, `2-2&G35`, `GHD1+`, `1-1`, `1-2`, `1-1&II1+`, `I02&II01`, `I02&II03`, `I02&II02`, `P0:2`, `P0:3`, `G3+`, `P0:1`, `1TM03`, `1TM02`, `GN2`, `GHP0`, `D1X&G4-6`, `PX2&D12`, `1&4+`, `2T01&01`, `FG1&1T2+`, `2-2&H2`, `D12&I12`, `X-2&G2+`, `2-2&I<II`, `GAP2+`, `I1-2&4+`, `P12&D12`, `X-2&G25`, `D12&I1+`, `X-2&G26`, `2&G3-6`, `2&G3-5`, `2&G3-4`, `PX2&DX2`, `D12`, `GG&3+`, `X-1&G2+`, `X-1&G26`, `G1-6`, `G1-5`, `G1-4`, `G1-3`, `G1-2`, `GGvG3+`, `I01&II01`, `I01&II02`, `I01&II03`, `2&II1+`, `1&II2+`, `II2+`, `GG&I2+`, `1&I1-2`, `1&G-G`, `G2-4`, `G2-5`, `G2-6`, `II23`, `1-1&G34`, `1-1&G35`, `1-1&G36`, `P12&D1X`, `2&3+`, `2&G4-5`, `2&G4-6`, `2-2&I2+`, `1-1&1TM2-3`, `2&G0-2`, `2&G0-3`, `1&G3-6`, `1&G3-4`, `1&G3-5`, `DX2&GG`, `2TMI2+&2TM3+`, `GHD01`, `2-2&G26`, `2-2&G25`, `2-2&G24`, `1&G4-5`, `30M1+1+`, `1&G4-6`, `2&I1-2`, `GH01`, `1&I=II`, `1TM4+`, `1&G0-3`, `1&G0-2`, `G-G`, `1t2+2+`, `G2-3`, `G6+`, `GHP1+`, `FG2&2T2+`, `G4-6`, `G4-5`, `GHP3+`, `GAD1`, `1-1&3+`, `T1:3`, `T1:2`, `T1:1`, `T1:0`, `D12&G23`, `T1:4`, `GG1&4+`, `G0-2`, `G0-3`, `T3:3`, `G0-1`, `T3:4`, `G0-4`, `I=II`, `D12&G2+`, `D12&I2+`, `X&G0-2`, `I13`, `I12`, `FG2&G3+`, `1&I<II`, `2-2&3+`, `X-2&I2+`, `1-1&I>II`, `G3-5`, `G3-4`, `G3-6`, `1&G2-6`, `2&G-G`, `1&G2-4`, `I2+&II3+`, `FG2&G4+`, `2&I<II`, `DX2`, `GG1`, `1&II1+`, `DW2`, `DW1`, `D1X&I1+II1+`, `2TM12`, `2&II2+`, `1-1&G45`, `1-1&G46`, `P2:0`, `P2:1`, `P2:2`, `P2:3`, `30M2+1+`, `1t1+2+`, `1T1+I&1T2+`, `D1X&G23`, `2v3+`, `2TMI1+&2TM3+`, `I2+&G3+`, `3HW1`, `3HW2`, `GAD2+`, `XvG3+`, `X-2&G3+`, `FG1&GG`, `30MG2+`, `X-2&GG` from matches_old where vrsta='FD' and infogram_mec_id is not null and approved=1 and published=1 and (cast(CONCAT(DATUM,' ',VREME) as datetime) >= '"+str(datetime.now()+timedelta(hours=delta_hours))+"') order by DATUM asc"
        mycursor.execute(k_check)
        k_rows = mycursor.fetchall()
        k_keys = [column[0] for column in mycursor.description]
        kvote = []
        for row in k_rows:
            kvote.append(dict(zip(k_keys, row)))

        path = dir_path+"/data_prod.json"
        #stari podaci
        prod_file = open(path,'r')
        for i in list(range(1,20)):
            try:
                old_data = json.loads(prod_file.read())
                break
            except json.decoder.JSONDecodeError:
                time.sleep(3)

        #pronalazenje razlike
        razlika_prod = []
        for novo in kvote:
            for staro in old_data:
                #stari mecevi
                if novo['code'] == staro['code'] and dateparser.parse(staro['startDate'])>datetime.now()+timedelta(hours=delta_hours):
                    for key in k_keys:
                        if key!='matchId' and key!='betradar_id' and key!='startDate':
                            if novo[key] != staro[key]:
                                razlika_prod.append(novo)
                                break

        #mecevi izbaceni iz ponude
        codes_staro = list([i['code'] for i in old_data if i['code']])
        codes_novo = list([i['code'] for i in kvote if i['code']])
        with open(os.path.join(dir_path, 'aktuelni.json'),'w') as outfile:
            json.dump({"aktuelni":codes_novo}, outfile)

        razlika = set(codes_novo)-set(codes_staro)
        #novi mecevi
        for novo in kvote:
            for x in razlika:
                if novo['code'] != x:
                    razlika_prod.append(novo)
                    break
        # print("PROD RAZLIKA")
        # print(len(razlika_prod))

        #RAZLIKA razlika_prod

        #pisanje u fajl podataka iz liste
        with open(os.path.join(dir_path, 'data_prod.json'),'w') as outfile:
            json.dump(kvote, outfile)


        for kvota in razlika_prod:
            for key in razlika_prod[0].keys():
                if key!='code' and key!='matchId' and key!='betradar_id' and key!='startDate':
                    if isinstance(kvota[key],dict):
                        kvota[key] = {"production":kvota[key]['production']}
                    else:
                        kvota[key]={"production":kvota[key]}



        #pronalazenje betradar meceva na produkciji
        ids = [i for i in list(map(lambda x:x['betradar_id'], mecevi)) if i]
        ids_str = ""
        for ele in ids:
            ids_str+=str(ele)+","
        ids_str = ids_str[:-1]



        #NEPOVEZANi MECEVI
        #SELECT DOMACIN as 'homeCompetitorName', GOST as 'awayCompetitorName', CONCAT(DATUM,' ',VREME) as 'startDate', liga, K1, K2, KX, `G0-2`, `G3+` from matches_old where K1!=0 and vrsta="FD" and (infogram_mec_id is null or betradar_id is null)
        mycursor = mydb.cursor()
        m_check = "SELECT DOMACIN as 'homeCompetitorName', GOST as 'awayCompetitorName', CONCAT(DATUM,' ',VREME) as 'startDate', liga, K1, K2, KX, `G0-2`, `G3+` from matches_old where K1!=0 and vrsta='FD' and (infogram_mec_id is null or betradar_id is null) and (cast(CONCAT(DATUM,' ',VREME) as datetime) >= '"+str(datetime.now()+timedelta(hours=delta_hours))+"') and published=1 and approved=1 order by DATUM asc"
        mycursor.execute(m_check)
        n_rows = mycursor.fetchall()
        n_keys = [column[0] for column in mycursor.description]
        nepovezani = []
        for row in n_rows:
            nepovezani.append(dict(zip(n_keys, row)))
        path = dir_path+"/data_nepovezani.json"
        with open(os.path.join(dir_path, 'data_nepovezani.json'),'w') as outfile:
            json.dump({"mecevi":nepovezani}, outfile)



        #BETRADAR
        mycursor = betradardb.cursor()
        limit = "SET SESSION group_concat_max_len=4294967295;"
        mycursor.execute(limit)
        betradardb.commit()
        b_check = """SELECT result.matchId, GROUP_CONCAT(case when result.specialValue is not null then CONCAT(result.betGameOutcome,'_',result.specialValue,'_',result.prob) end) as 'Special', 
                GROUP_CONCAT(case when result.specialValue is null then CONCAT(result.betGameOutcome,'_',result.prob) end) as 'Regular'
                from(SELECT bp.match_id as 'matchId', special_value as 'specialValue', value as 'prob', CONCAT(`name`,'_',bot.betradar_name) as 'betGameOutcome' FROM `betradar_probability` bp inner join betradar_odd_type bot on bp.type_id = bot.id where match_id in
                ("""+ids_str+""")) as result group by result.matchId"""
        mycursor.execute(b_check)
        b_rows = mycursor.fetchall()
        b_keys = [column[0] for column in mycursor.description]

        betradar = []
        for row in b_rows:
            betradar.append(dict(zip(b_keys, row)))

        #stari podaci
        with open(os.path.join(dir_path, 'data_betradar.json')) as jsonfile:
            old_data = json.load(jsonfile)

        #pronalazenje razlike
        razlika_betradar = []
        for novo in betradar:
            for staro in old_data:
                if novo['matchId'] == staro['matchId']:
                    for key in b_keys:
                        #stari mecevi
                        if novo[key] != staro[key]:
                            razlika_betradar.append(novo)
                            break


        codes_novo = list([i['matchId'] for i in betradar if i['matchId']])
        codes_staro = list([i['matchId'] for i in old_data if i['matchId']])

        razlika = set(codes_novo)-set(codes_staro)

        #novi mecevi
        for novo in betradar:
            for x in razlika:
                if novo['matchId'] == x:
                    razlika_betradar.append(novo)
        # print("BETRADAR RAZLIKA")
        # print(len(razlika_betradar))
        #pisanje u fajl podataka iz liste
        with open(os.path.join(dir_path, 'data_betradar.json'),'w') as outfile:
            json.dump(betradar, outfile)


        for mec in razlika_betradar:
            mec["prob_total_under"]=None
            mec["total"]=None
            mec["handicap"]=None
            mec["prob_handicap"]=None
            mec["prob_x"]=None
            if mec["Regular"]:
                mec["prob_x"]=extract1X2('KX_3- Way', mec["Regular"])
            if mec["Special"]:
                total_data = extractTotal(mec["Special"])
                mec["prob_total_under"] = total_data["prob"]
                mec["total"] = total_data["total"]
            if mec["Special"]:
                handicap_data = extractHandicap(mec["Special"])
                mec["handicap"] = handicap_data["handicap"]
                mec["prob_handicap"] = handicap_data["prob"]
            del mec["Regular"]
            del mec["Special"]
                

            
        json_betradar = razlika_betradar

        key_list = ['FD'] #'KO' itd
        groupedBy = {key: {} for key in key_list}
        lige = list(set([e['liga'] for e in mecevi]))
        for elem in mecevi:
            if elem['sport'] == 'FD':
                for liga in lige:
                    if elem['liga'] in liga and not liga in groupedBy['FD']:
                        groupedBy['FD'][liga] = []

        for elem in mecevi:
            for gr_lige in groupedBy['FD']:
                if elem['liga'] == gr_lige and elem['sport']=="FD":
                    elem['odds']={}
                    for kvota in razlika_prod:
                        if kvota['code']==elem['Code']:
                            elem['odds'] = kvota
                            groupedBy['FD'][gr_lige].append(elem)

        json_lista = groupedBy
        oddsJson(json_asian,json_lista,json_betradar)
        #calculateOddsDiff(json_asian, json_lista, json_betradar,None)
    except Exception as e:
        with open(os.path.join(dir_path, 'error_log.txt'),'a') as err:
            err.write(str(e)+"-"+str(datetime.now())+"-type:decode\n")
