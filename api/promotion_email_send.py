import xlsxwriter
from db_land import DbLand
from flask import request
from flask_restful import Resource
import json
import mysql.connector
import os
from datetime import datetime, time, timedelta

db = DbLand()

startDate="2022-04-04 09:00:00.000"
endDate=(datetime.today()+timedelta(hours=2)).strftime('%Y-%m-%d')+str(" 09:00:00")

with db.engine.begin() as conn:
    podaci = None
    data = (
        ['Na broj poena utiču:', 'br. ukupno otkucanih tiketa, br. otkucanih tiketa za promociju i prosečna uplata tiketa za promociju'],
        ['Lokacija', 'Broj Poena']
    )
    result = conn.execute(
    'exec dbo.m_locationRankingPromotion @from="'+str(startDate)+'", @to="'+str(endDate)+'"')
    db.__del__()
    if result is None:
        result = []
    for obj in result:
        podaci = [
            obj['Lokacija'],
            obj['Broj Poena']
        ]
        data += (podaci,)
        
workbook = xlsxwriter.Workbook('rang_lista_zakljucno_sa_jucerasnjim_danom.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0

for item, podatak in (data):
    worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, podatak)
    row += 1

workbook.close()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
dir_path = os.path.dirname(os.path.realpath(__file__)) 
filename = os.path.join(dir_path, "rang_lista_zakljucno_sa_jucerasnjim_danom.xlsx")

sender = "m.djacic@soccerbet.rs"
# receiver = "m.djacic@soccerbet.rs"
# cc = 'desetrepova@gmail.com,milos3773@gmail.com'
receiver = "m.zec@soccerbet.rs"
cc = 't.stefanov@soccerbet.rs,i.igrutinovic@soccerbet.rs,n.stanojkovic@soccerbet.rs,b.pantic@soccerbet.rs,m.mitrovic@soccerbet.rs,m.djacic@soccerbet.rs'
msg = MIMEMultipart()
msg['From'] = "Soccerbet Liga Miliona<noreply@soccerbet.rs>"
msg['To'] = receiver
msg['Cc'] = cc
msg['Date'] = formatdate(localtime = True)
msg['Subject'] = "Rang lista poslovnica sortiranih po uspešnosti"
text = "<p style='color:indianred'>Dobro jutro,</p>U prilogu se nalazi rang lista koja se generiše svakog jutra i sadrži akumulirane poene za svaku od poslovnica od početka promocije do tekućeg dana u 9h.<br/></br>Na broj poena utiču: br. ukupno otkucanih tiketa, br. otkucanih tiketa za promociju i prosečna uplata tiketa za promociju!<br/></br>Ovaj email je automatski i na njega ne treba odgovarati."

part = MIMEBase('application', "octet-stream")
part.set_payload(open(filename, "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="rang_lista_zakljucno_sa_jucerasnjim_danom.xlsx"')
msg.attach(part)
part2 = MIMEText(text, 'html')
msg.attach(part2)
rcpt = cc.split(",") + [receiver]


try:
   password='Sisarka123!'
   smtpserver=smtplib.SMTP("mail.soccerbet.rs",587)
   smtpserver.ehlo()
   smtpserver.starttls()
   smtpserver.ehlo
   smtpserver.login(sender,password)
   smtpserver.sendmail(sender,rcpt,msg.as_string())
   print('Sent')
   smtpserver.close()
   os.remove(os.path.join(dir_path, "rang_lista_zakljucno_sa_jucerasnjim_danom.xlsx"))
except Exception as e:
   print(e)
