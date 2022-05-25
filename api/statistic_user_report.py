from flask import request
from flask_restful import Resource
import json
import mysql.connector
import os




class StatisticUserReport(Resource):

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="m.djacic",
            password="Soccer123",
            database="reporting",
            buffered=True,
            auth_plugin='mysql_native_password'
        )


    def post(self):
        data = request.get_json(force=True)
        od = data["from"]
        do = data["to"]
        slipType = data["slipType"]
        tip = data['type']
        mycursor = self.mydb.cursor()
        if not tip:
            sql_data = '''SELECT username,
            sum(brojtiketa*brojparovamean)/sum(brojtiketa) as 'brojparovamean',
            sum(brojtiketa) as 'brojtiketa',
            sum(brojtiketa*brojparovamean*kvotalinijamean)/sum(brojtiketa*brojparovamean) as 'kvotalinijamean',
            sum(kvotatiketamean*brojtiketa) / sum(brojtiketa) as 'kvotatiketamean',
            sum(sumbet) / sum(brojtiketa) as 'betmean',
            sum(sumbet) as 'sumbet',
            sum(sumwin) as 'sumwin',
            SlipUserId
            from StatisticUserReportDefault where date>="'''+str(od)+'''" and date<="'''+str(do)+'''" and sliptype='''+str(slipType)+'''
            group by username, slipuserid;
            '''
            mycursor.execute(sql_data)
            result = mycursor.fetchall()
            data = []
            one = {}
            for row in result:
                print(row)
                one["username"] = row[0]
                one["brojparovamean"] = round(float(row[1]),2)
                one["brojtiketa"] = int(row[2])
                one["kvotalinijamean"] = round(float(row[3]),2)
                one["kvotatiketamean"] = round(float(row[4]),2)
                one["betmean"] = round(float(row[5]),2)
                one["sumbet"] = round(float(row[6]),2)
                one["sumwin"] = round(float(row[7]),2)
                one["profit"] = round(float(row[6])-float(row[7]),2)
                one["margin"] = round((float(row[6])-float(row[7]))/float(row[6]),2)
                one['slipuserid'] = row[8]
                data.append(one)
                one = {}
        else:
            columns = []
            if 1 in tip:
                columns.append('sum(case when fudbalsumbet>0 then fudbalsumbet else 0 end) fudbalsumbet')
                columns.append('sum(case when fudbalsumwin>0 then fudbalsumwin else 0 end) fudbalsumwin')
                columns.append('sum(case when fudbalbrojtiketa>0 then fudbalbrojtiketa else 0 end) fudbalbrojtiketa')
            if 2 in tip:
                columns.append('sum(case when kosarkasumbet>0 then kosarkasumbet else 0 end) kosarkasumbet')
                columns.append('sum(case when kosarkasumwin>0 then kosarkasumwin else 0 end) kosarkasumwin')
                columns.append('sum(case when kosarkabrojtiketa>0 then kosarkabrojtiketa else 0 end) kosarkabrojtiketa')
            if 3 in tip:
                columns.append('sum(case when tenissumbet>0 then tenissumbet else 0 end) tenissumbet')
                columns.append('sum(case when tenissumwin>0 then tenissumwin else 0 end) tenissumwin')
                columns.append('sum(case when tenisbrojtiketa>0 then tenisbrojtiketa else 0 end) tenisbrojtiketa')
            if 12 in tip:
                columns.append('sum(case when igracispecijalsumbet>0 then igracispecijalsumbet else 0 end) igracispecijalsumbet')
                columns.append('sum(case when igracispecijalsumwin>0 then igracispecijalsumwin else 0 end) igracispecijalsumwin')
                columns.append('sum(case when igracispecijalbrojtiketa>0 then igracispecijalbrojtiketa else 0 end) igracispecijalbrojtiketa')
            if 123 in tip:
                columns.append('sum(case when ostalosumbet>0 then ostalosumbet else 0 end) ostalosumbet')
                columns.append('sum(case when ostalosumwin>0 then ostalosumwin else 0 end) ostalosumwin')
                columns.append('sum(case when ostalobrojtiketa>0 then ostalobrojtiketa else 0 end) ostalobrojtiketa')
            columnsString = ','.join(columns)
            sql_data = '''SELECT username, slipuserid, sum(numlines) as 'numlines', sum(brojtiketa) as 'brojtiketa', '''+columnsString+'''
            from StatisticUserReportFiltered where date>="'''+str(od)+'''" and date<="'''+str(do)+'''" and sliptype='''+str(slipType)+'''
            group by username, slipuserid;'''
            dir_path = os.path.dirname(os.path.realpath(__file__))
            mycursor.execute(sql_data)
            result = mycursor.fetchall()
            field_names = [i[0] for i in mycursor.description]
            data = []
            one = {}
            betindex = None
            winindex = None
            slipnumindex = None
            for row in result:
                one["username"] = row[0]
                one["slipuserid"] = row[1]
                one["numlines"] = int(row[2]),
                one["brojtiketa"] = int(row[3]),
                if 1 in tip:
                    betindex = field_names.index("fudbalsumbet")
                    winindex = field_names.index("fudbalsumwin")
                    slipnumindex = field_names.index("fudbalbrojtiketa")
                    if row[betindex] == 0:
                        continue
                    one["fudbalsumbet"] = float(row[betindex])
                    one["fudbalsumwin"] = float(row[winindex])
                    one["fudbalbrojtiketa"] = float(row[slipnumindex])
                    one["profitfudbal"] = float(row[betindex]) - float(row[winindex])
                    one["marginfudbal"] = (float(row[betindex]) - float(row[winindex])) / float(row[betindex]) if float(row[betindex]) else 0
                if 2 in tip:
                    betindex = field_names.index("kosarkasumbet")
                    winindex = field_names.index("kosarkasumwin")
                    slipnumindex = field_names.index("kosarkabrojtiketa")
                    if row[betindex] == 0:
                        continue
                    one["kosarkasumbet"] = float(row[betindex])
                    one["kosarkasumwin"] = float(row[winindex])
                    one["kosarkabrojtiketa"] = float(row[slipnumindex])
                    one["profitkosarka"] = float(row[betindex]) - float(row[winindex])
                    one["marginkosarka"] = (float(row[betindex]) - float(row[winindex])) / float(row[betindex]) if float(row[betindex]) else 0
                if 3 in tip:
                    betindex = field_names.index("tenissumbet")
                    winindex = field_names.index("tenissumwin")
                    slipnumindex = field_names.index("tenisbrojtiketa")
                    if row[betindex] == 0:
                        continue
                    one["tenissumbet"] = float(row[betindex])
                    one["tenissumwin"] = float(row[winindex])
                    one["tenisbrojtiketa"] = float(row[slipnumindex])
                    one["profittenis"] = float(row[betindex]) - float(row[winindex])
                    one["margintenis"] = (float(row[betindex]) - float(row[winindex])) / float(row[betindex]) if float(row[betindex]) else 0
                if 12 in tip:
                    betindex = field_names.index("igracispecijalsumbet")
                    winindex = field_names.index("igracispecijalsumwin")
                    slipnumindex = field_names.index("igracispecijalbrojtiketa")
                    if row[betindex] == 0:
                        continue
                    one["igracispecijalsumbet"] = float(row[betindex])
                    one["igracispecijalsumwin"] = float(row[winindex])
                    one["igracispecijalbrojtiketa"] = float(row[slipnumindex])
                    one["profitigracispecijal"] = float(row[betindex]) - float(row[winindex])
                    one["marginigracispecijal"] = (float(row[betindex]) - float(row[winindex])) / float(row[betindex]) if float(row[betindex]) else 0
                if 123 in tip:
                    betindex = field_names.index("ostalosumbet")
                    winindex = field_names.index("ostalosumwin")
                    slipnumindex = field_names.index("ostalobrojtiketa")
                    if row[betindex] == 0:
                        continue
                    one["ostalosumbet"] = float(row[betindex])
                    one["ostalosumwin"] = float(row[winindex])
                    one["ostalobrojtiketa"] = float(row[slipnumindex])
                    one["profitostalo"] = float(row[betindex]) - float(row[winindex])
                    one["marginostalo"] = (float(row[betindex]) - float(row[winindex])) / float(row[betindex]) if float(row[betindex]) else 0
                betindex = None
                winindex = None
                slipnumindex = None
                data.append(one)
                one = {}
        return {"data":data}, 200
        
