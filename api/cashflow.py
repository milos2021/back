from flask import request
from flask_restful import Resource
import json
import mysql.connector
import os




class Cashflow(Resource):

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
        od = data["from"]
        do = data["to"]
        balanceOd = data['balanceOd']
        balanceDo = data['balanceDo']
        period = data["period"]
        month = data["month"]
        year = data["year"]
        payment_method = data["method"]
        novi = data['novi']
        out = None
        mycursor = self.mydb.cursor()
        if novi:
            #balansi
            sql_data = 'SELECT cast(BalanceDate as date) as "balance_date", UserStandardBalance, UserPromoBalance FROM `UserBalances` where RemoteLocationId = "NULL" and cast(BalanceDate as date)>="'+str(balanceOd)+'" and cast(BalanceDate as date)<="'+str(balanceDo)+'"'
            mycursor.execute(sql_data)
            result3 = mycursor.fetchall()
            balances = []
            balancesObj = {}
            for row in result3:
                balancesObj['balance_date'] = str(row[0])
                balancesObj['std'] = float(row[1])
                balancesObj['prm'] = float(row[2])
                balances.append(balancesObj)
                balancesObj={}
            sql_data = "SELECT * FROM CashflowDataNew where datum>='"+str(od)+"' and datum<='"+str(do)+"'"
            mycursor.execute(sql_data)
            result = mycursor.fetchall()
            data = []
            dataObj = {}
            for row in result:
                dataObj['datum'] = str(row[0])
                dataObj['deposit_sum_all'] = str(row[1])
                dataObj['deposit_users_all'] = str(row[2])
                dataObj['deposit_number_all'] = str(row[3])
                dataObj['deposit_sum_bank'] = str(row[4])
                dataObj['deposit_users_bank'] = str(row[5])
                dataObj['deposit_number_bank'] = str(row[6])
                dataObj['deposit_sum_cc'] = str(row[7])
                dataObj['deposit_users_cc'] = str(row[8])
                dataObj['deposit_number_cc'] = str(row[9])
                dataObj['deposit_sum_ipay'] = str(row[10])
                dataObj['deposit_users_ipay'] = str(row[11])
                dataObj['deposit_number_ipay'] = str(row[12])
                dataObj['deposit_sum_komsija'] = str(row[13])
                dataObj['deposit_users_komsija'] = str(row[14])
                dataObj['deposit_number_komsija'] = str(row[15])
                dataObj['deposit_sum_shops'] = str(row[16])
                dataObj['deposit_users_shops'] = str(row[17])
                dataObj['deposit_number_shops'] = str(row[18])
                dataObj['withdraw_sum_all'] = str(row[19])
                dataObj['withdraw_users_all'] = str(row[20])
                dataObj['withdraw_number_all'] = str(row[21])
                dataObj['withdraw_sum_bank'] = str(row[22])
                dataObj['withdraw_users_bank'] = str(row[23])
                dataObj['withdraw_number_bank'] = str(row[24])
                dataObj['withdraw_sum_shops'] = str(row[25])
                dataObj['withdraw_users_shops'] = str(row[26])
                dataObj['withdraw_number_shops'] = str(row[27])
                dataObj['promo_sum'] = str(row[28])
                dataObj['promo_users'] = str(row[29])
                dataObj['promo_number'] = str(row[30])
                dataObj['promo_cost'] = str(row[31])
                dataObj['mesec'] = str(row[32])
                dataObj['deposit_users_all_month'] = str(row[33])
                dataObj['withdraw_users_all_month'] = str(row[34])
                dataObj['deposit_users_shops_month'] = str(row[35])
                dataObj['withdraw_users_shops_month'] = str(row[36])
                dataObj['deposit_users_bank_month'] = str(row[37])
                dataObj['withdraw_users_bank_month'] = str(row[38])
                dataObj['deposit_users_cc_month'] = str(row[39])
                dataObj['deposit_users_ipay_month'] = str(row[40])
                dataObj['deposit_users_komsija_month'] = str(row[41])
                dataObj['promo_users_month'] = str(row[42])
                dataObj['godina'] = str(row[43])
                dataObj['deposit_users_all_year'] = str(row[44])
                dataObj['withdraw_users_all_year'] = str(row[45])
                dataObj['deposit_users_shops_year'] = str(row[46])
                dataObj['withdraw_users_shops_year'] = str(row[47])
                dataObj['deposit_users_bank_year'] = str(row[48])
                dataObj['withdraw_users_bank_year'] = str(row[49])
                dataObj['deposit_users_cc_year'] = str(row[50])
                dataObj['deposit_users_ipay_year'] = str(row[51])
                dataObj['deposit_users_komsija_year'] = str(row[52])
                dataObj['promo_users_year'] = str(row[53])
                data.append(dataObj)
                dataObj={}
                
            out = {
                'data':data,
                'balances':balances
            }
        else:
            if period == 3:
                sql_data = "SELECT * from CashflowCombinations where period="+str(period)+" and `month`="+str(month)+" and `year`="+str(year)+" and payment_method="+str(payment_method)
            else:
                sql_data = "SELECT * from CashflowCombinations where period="+str(period)+" and `year`="+str(year)+" and payment_method="+str(payment_method)
            
            mycursor.execute(sql_data)
            result = mycursor.fetchall()
            comb_id = None
            podaci = []
            for row in result:
                comb_id = row[0]
            if comb_id is None:
                podaci = []
            else:
                sql_data = "SELECT * from CashflowData where comb_id="+str(comb_id)
                mycursor.execute(sql_data)
                result = mycursor.fetchall()
                podaci = []
                obj = {}
                if period == 3:
                    for row in result:
                        obj['datum'] = str(row[2])
                        obj['deposit_users'] = row[3]
                        obj['deposit_number'] = row[4]
                        obj['deposit_sum'] = row[5]
                        obj['withdraw_users'] = row[6]
                        obj['withdraw_number'] = row[7]
                        obj['withdraw_sum'] = row[8]
                        obj['diff_sum'] = row[9]
                        obj['diff_margin'] = row[10]
                        podaci.append(obj)
                        obj={}
                        
                    #balansi
                    sql_data = 'SELECT cast(BalanceDate as date) as "balance_date", UserStandardBalance, UserPromoBalance FROM `UserBalances` where RemoteLocationId = "NULL" and cast(BalanceDate as date)>="'+str(balanceOd)+'" and cast(BalanceDate as date)<="'+str(balanceDo)+'"'
                    mycursor.execute(sql_data)
                    result = mycursor.fetchall()
                    balances = []
                    balancesObj = {}
                    for row in result:
                        balancesObj['balance_date'] = str(row[0])
                        balancesObj['std'] = float(row[1])
                        balancesObj['prm'] = float(row[2])
                        balances.append(balancesObj)
                        balancesObj={}
                    #podaci,balances till
                    
                    #broj usera mesecno (dep,wdr)
                    sql_data = "SELECT * from CashflowCombinations where period=2 and `month`=0 and `year`="+str(year)+" and payment_method="+str(payment_method)
                    mycursor.execute(sql_data)
                    result = mycursor.fetchall()
                    for row in result:
                        comb_id = row[0]
                    if comb_id is not None:
                        sql_data = "SELECT * from CashflowData where comb_id="+str(comb_id)
                        mycursor.execute(sql_data)
                        result = mycursor.fetchall()
                    users = {}
                    
                    for row in result:
                        if str(row[2])==str(month):
                            users['deposit_users'] = float(row[3])
                            users['withdraw_users'] = float(row[6])
                    #promo
                    sql_promo = '''select case when datum = 'NULL' then datum_cost else datum end as 'datum', promo_sum, promo_users, promo_number, promo_cost, case when datum_cost = 'NULL' then datum else datum_cost end as 'datum_cost' from PromoData where (datum>="'''+str(od)+'''" and datum<="'''+str(do)+'''") or (datum_cost>="'''+str(od)+'''" and datum_cost<="'''+str(do)+'''") order by datum'''
                    mycursor.execute(sql_promo)
                    result_promo = mycursor.fetchall()
                    promo = []
                    promoObj = {}
                    for row in result_promo:
                        promoObj['datum'] = row[0]
                        promoObj['promo_sum'] = float(row[1])
                        promoObj['promo_users'] = row[2]
                        promoObj['promo_number'] = row[3]
                        promoObj['promo_cost'] = float(row[4])
                        promo.append(promoObj)
                        promoObj={}
                    
                    #podaci,balances,promo till
                    
                    #promo mesecno
                    sql_promo = '''select promo_users from PromoData where mesec='''+str(month)+''' and godina='''+str(year)
                    mycursor.execute(sql_promo)
                    result_promo = mycursor.fetchall()
                    promoMonthly = []
                    promoObj = {}
                    for row in result_promo:
                        promoObj['promo_users'] = float(row[0])
                        promoMonthly.append(promoObj)
                        promoObj={}
                        
                    #podaci,balances,promo,promoMonthly till
                    
                    

                    #podaci,balances,promo,promoMonthly,users(monthly)
                    out = {
                        'mainData':podaci,
                        'mainDataMonthly':users,
                        'promoData':promo,
                        'promoMonthlyData':promoMonthly,
                        'balances':balances
                    }
                if period == 2:
                    sql_data = '''select month(datum) as 'datum', sum(deposit_number) as 'deposit_number', sum(deposit_sum) as 'deposit_sum', sum(withdraw_number) as 'withdraw_number', sum(withdraw_sum) as 'withdraw_sum', sum(diff_sum) as 'diff_sum', (sum(deposit_sum)-sum(withdraw_sum))/sum(deposit_sum) as 'diff_margin' from CashflowData
    where datum>="'''+str(od)+'''" and datum<="'''+str(do)+'''" and comb_id in (
    select id from CashflowCombinations where period=3 and month!=0 and year='''+str(year)+''' and payment_method='''+str(payment_method)+''') group by month(datum)'''
                    mycursor.execute(sql_data)
                    result2 = mycursor.fetchall()
                    for row in result:
                        obj['datum'] = str(row[2])
                        obj['deposit_users'] = row[3] 
                        obj['withdraw_users'] = row[6] 
                        for row2 in result2:
                            if str(row[2])==str(row2[0]):
                                obj['deposit_number'] = float(row2[1])
                                obj['deposit_sum'] = row2[2] if isinstance(row2[2], float) else 0
                                obj['withdraw_number'] = float(row2[3])
                                obj['withdraw_sum'] = row2[4] if isinstance(row2[4], float) else 0
                                obj['diff_sum'] = row2[5] if isinstance(row2[5], float) else 0
                                obj['diff_margin'] = row2[6] if isinstance(row2[6], float) else 0
                        podaci.append(obj)
                        obj={}
                        
                    #balansi
                    sql_data = 'SELECT cast(BalanceDate as date) as "balance_date", UserStandardBalance, UserPromoBalance FROM `UserBalances` where RemoteLocationId = "NULL" and cast(BalanceDate as date)>="'+str(balanceOd)+'" and cast(BalanceDate as date)<="'+str(balanceDo)+'"'
                    mycursor.execute(sql_data)
                    result3 = mycursor.fetchall()
                    balances = []
                    balancesObj = {}
                    for row in result3:
                        balancesObj['balance_date'] = str(row[0])
                        balancesObj['std'] = float(row[1])
                        balancesObj['prm'] = float(row[2])
                        balances.append(balancesObj)
                        balancesObj={}
                    #podaci, balances till
                    
                    year_data = "SELECT * from CashflowCombinations where period=1 and month=0 and `year`="+str(year)+" and payment_method="+str(payment_method)
                    mycursor.execute(year_data)
                    result = mycursor.fetchall()
                    year_comb_id = result[0][0] #id year kombinacije
                    
                    sql_data = "SELECT * from CashflowData where comb_id="+str(year_comb_id)
                    mycursor.execute(sql_data)
                    result = mycursor.fetchall()
                    yearUsers = []
                    yearObj = {}
                    for row in result:
                        yearObj['deposit_users'] = float(row[3])
                        yearObj['withdraw_users'] = float(row[6])
                        yearUsers.append(yearObj)
                        yearObj={}
                    
                    #promo
                    sql_promo = "SELECT mesec, promo_users FROM PromoData where godina="+str(year)+" and mesec!=0"
                    mycursor.execute(sql_promo)
                    result = mycursor.fetchall()
                    promo = []
                    promoObj = {}
                    
                    sql_promo = '''select month(datum) as 'datum', sum(promo_sum) as 'promo_sum', sum(promo_number) as 'promo_number', sum(promo_cost) as 'promo_cost' from PromoData
    where datum>="'''+str(od)+'''" and datum<="'''+str(do)+'''" group by month(datum)'''
                    mycursor.execute(sql_promo)
                    result2 = mycursor.fetchall()

                    for row in result:
                        promoObj['datum'] = str(row[0])
                        promoObj['promo_users'] = float(row[1] if row[1] else 0) 
                        for row2 in result2:
                            if str(row[0])==str(row2[0]):
                                promoObj['promo_sum'] = row2[1] if isinstance(row2[1], float) else 0
                                promoObj['promo_number'] = float(row2[2])
                                promoObj['promo_cost'] = row2[3] if isinstance(row2[3], float) else 0
                        promo.append(promoObj)
                        promoObj={}
                    
                    #promo godisnji
                    sql_promo = "SELECT promo_users FROM PromoData where godina="+str(year)+" and mesec=0"
                    mycursor.execute(sql_promo)
                    result = mycursor.fetchall()
                    promoYearlyUsers = float(result[0][0])
                    
                    out = {
                        'mainData':podaci,
                        'mainDataYearly':yearUsers,
                        'promoData':promo,
                        'promoYearlyData':promoYearlyUsers,
                        'balances':balances
                    }
                
        return {"data":out}, 200
