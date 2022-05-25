import mysql.connector
x = mysql.connector.connect(
            host="10.0.90.23",
            user="m.djacic",
            password="Soccer123",
            database="reporting",
            buffered=True,
            auth_plugin='mysql_native_password'
        )
od = "2021-10-01"
do = "2021-11-05"
slipType = 0
mycursor = x.cursor()
sql_data = '''SELECT username,
        sum(brojtiketa*brojparovamean)/sum(brojtiketa) as 'brojparovamean',
        sum(brojtiketa) as 'brojtiketa',
        sum(brojtiketa*brojparovamean*kvotalinijamean)/sum(brojtiketa*brojparovamean) as 'kvotalinijamean',
        sum(kvotatiketamean*brojtiketa) / sum(brojtiketa) as 'kvotatiketamean',
        sum(sumbet) / sum(brojtiketa) as 'betmean',
        sum(sumbet) as 'sumbet',
        sum(sumwin) as 'sumwin'
        from StatisticUserReportDefault where date>"'''+str(od)+'''" and date<"'''+str(do)+'''" and sliptype='''+str(slipType)+'''
        group by username;
        '''
print(sql_data)
mycursor.execute(sql_data)
result = mycursor.fetchall()
data = []
one = {}
for row in result:
    print(row)
    one["username"] = row[0]
    one["brojparovamean"] = float(row[1])
    one["brojtiketa"] = int(row[2])
    one["kvotalinijamean"] = float(row[3])
    one["kvotatiketamean"] = float(row[4])
    one["betmean"] = float(row[5])
    one["sumbet"] = float(row[6])
    one["sumwin"] = float(row[7])
    one["profit"] = float(row[6])-float(row[7])
    one["margin"] = float(row[6])-float(row[7])/float(row[6])
    data.append(one)
    one = {}
    
print(data)