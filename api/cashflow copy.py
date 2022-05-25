from db import Db
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json


class Cashflow(Resource):

	def __init__(self):
		self.db = Db()

	@staticmethod
	def switchLocation(arg):
		switcher = {
			1: "10001",
			#2: "1 AND 7999",
			3: "10000",
			4: "10000",
			5: "10000"
		}
		return switcher.get(arg, "Invalid location")
	
	@staticmethod
	def switchPaymentMethod(arg):
		switcher = {
			1:3,
			2:2,
			3:5,
			4:7,
			5:3
		}
		return switcher.get(arg, "Invalid payment type")

	def post(self):
		data = request.get_json(force=True)
		paymentMethod = data['paymentMethod']
		#mapping
		location = 0
		method = 0
		#where avoidance
		destinationPaymentMethods = [2,5,0] 
		#dates range string
		datesRangeQuery = ""
		if paymentMethod!=0: # and paymentMethod!=2
			location = self.switchLocation(paymentMethod)
			method = self.switchPaymentMethod(paymentMethod)
		
		if data['dates']:
			result = data['dates']
			for index in range(len(result)):
				if index==len(result)-1:
					datesRangeQuery+="mix.OpsegGodina='"+str(result[index])+"' "
				else:
					datesRangeQuery+="mix.OpsegGodina='"+str(result[index])+"' OR "
		if data['monthFrom']:
			monthFrom = data['monthFrom']
			monthTo = data['monthTo']
		if data['year']:
			year = data['year']
		period = data['period']
		query = ""
		if period == 0:
			query = """select mix.OpsegGodina as 'Opseg', sum(mix.TransactionAmount) as 'deposit_sum', count(distinct(mix.UserId)) as 'deposit_users', count(mix.UserId) as 'deposit_number' into #dep from 
					(select case when (DATEPART(DAY,Tr.TransactionDate)=1 AND DATEPART(MONTH,Tr.TransactionDate)=1 AND cast(Tr.TransactionDate as time) < '08:00:00.000') 
					then YEAR(CAST(DATEADD(year,-1,Tr.TransactionDate) as DATE))
					else YEAR(CAST(Tr.TransactionDate as DATE))
					end as OpsegGodina, Tr.TransactionAmount as TransactionAmount, tr.UserId as UserId from Transactions tr inner join Users us on tr.UserId = us.UserId
					where tr.DestinationPaymentType=0 
					and tr.IsConfirmed = 1
					and tr.IsCanceled = 0
					and tr.TransactionType in (2,11)"""
			if paymentMethod == 2:
				query+= " and Tr.RemoteLocationID BETWEEN 1 AND 7999"
			elif paymentMethod != 0 and paymentMethod!=2:
				query += " and Tr.RemoteLocationID = '"+str(location)+"'"
			if paymentMethod!=0:
				query += " and Tr.SourcePaymentType = '"+str(method)+"'"
			else:
				query += " and Tr.SourcePaymentType IN (2,3,5,7)"
			query+=") as mix "
			query+="where mix.OpsegGodina = "+str(year)
			query+="group by mix.OpsegGodina "
			
			if paymentMethod in destinationPaymentMethods:
				query+="""select mix.OpsegGodina as 'Opseg', sum(mix.TransactionAmount) as 'withdraw_sum', count(distinct(mix.UserId)) as 'withdraw_users', count(mix.UserId) as 'withdraw_number' into #wdr from 
						(select case when (DATEPART(DAY,Tr.TransactionDate)=1 AND DATEPART(MONTH,Tr.TransactionDate)=1 AND cast(Tr.TransactionDate as time) < '08:00:00.000') 
						then YEAR(CAST(DATEADD(year,-1,Tr.TransactionDate) as DATE))
						else YEAR(CAST(Tr.TransactionDate as DATE))
						end as OpsegGodina, Tr.TransactionAmount as TransactionAmount, tr.UserId as UserId from Transactions tr inner join Users us on tr.UserId = us.UserId
						where tr.SourcePaymentType = 0
						and tr.IsConfirmed = 1
						and tr.IsCanceled = 0
						and tr.TransactionType = 1"""
				if paymentMethod == 2:
					query+= " and Tr.RemoteLocationID BETWEEN 1 AND 7999"
				elif paymentMethod != 0 and paymentMethod!=2:
					query += " and Tr.RemoteLocationID = '"+str(location)+"'"
			
				if paymentMethod!=0:
					query += " and Tr.DestinationPaymentType = '"+str(method)+"'"
				else:
					query += " and Tr.DestinationPaymentType IN (2,3)"
				query+=") as mix "
				query+="where mix.OpsegGodina = "+str(year)
				query+="group by mix.OpsegGodina "
			
			#promo
			query+="""select 
  mix.OpsegGodina as 'Opseg', 
  sum(mix.TransactionAmount) as 'promo_sum', 
  count(
    distinct(mix.UserId)
  ) as 'promo_users', 
  count(mix.UserId) as 'promo_number' into #pro from
  (
    select 
      case when (DATEPART(DAY,Tr.TransactionDate)=1 AND DATEPART(MONTH,Tr.TransactionDate)=1 AND cast(Tr.TransactionDate as time) < '08:00:00.000') 
						then YEAR(CAST(DATEADD(year,-1,Tr.TransactionDate) as DATE))
						else YEAR(CAST(Tr.TransactionDate as DATE)) end as OpsegGodina, 
      Tr.TransactionAmount as TransactionAmount, 
      tr.UserId as UserId 
    from 
      Transactions tr 
      inner join Users us on tr.UserId = us.UserId 
    where 
      tr.DestinationPaymentType = 0 
      and tr.IsConfirmed = 1 
      and tr.IsCanceled = 0 
      and tr.TransactionType = 2
      and Tr.SourcePaymentType = 6
	  and Tr.DestinationPaymentType = 1
	  and Tr.GameSystem = 1
  ) as mix where mix.OpsegGodina="""+str(year)
			query+="group by mix.OpsegGodina "

			if paymentMethod in destinationPaymentMethods:
				query+="""select d.Opseg, d.deposit_sum, d.deposit_users, d.deposit_number, w.withdraw_sum, w.withdraw_users, w.withdraw_number,coalesce(p.promo_sum,0) as 'promo_sum', coalesce(p.promo_users,0) as 'promo_users', coalesce(p.promo_number,0) as 'promo_number' from #dep d left join #wdr w on d.Opseg=w.Opseg left join #pro p on d.Opseg=p.Opseg order by d.Opseg"""
			else: 
				query+="""select d.Opseg, d.deposit_sum, d.deposit_users, d.deposit_number, 0.00 as 'withdraw_sum', 0 as 'withdraw_users', 0 as 'withdraw_number', coalesce(p.promo_sum,0) as 'promo_sum', coalesce(p.promo_users,0) as 'promo_users', coalesce(p.promo_number,0) as 'promo_number' from #dep d left join #pro p on d.Opseg=p.Opseg order by d.Opseg"""
		if period == 1:
			query = """select mix.OpsegGodina as 'Opseg', sum(mix.TransactionAmount) as 'deposit_sum', count(distinct(mix.UserId)) as 'deposit_users', count(mix.UserId) as 'deposit_number' into #dep from 
					(select case when cast(Tr.TransactionDate as time) < '08:00:00.000' and cast(Tr.TransactionDate as time) >= '00:00:00.000'
					then MONTH(CAST(DATEADD(day,-1,Tr.TransactionDate) as DATE))
					else MONTH(CAST(Tr.TransactionDate as DATE))
					end as OpsegGodina, Tr.TransactionAmount as TransactionAmount, CONVERT(varchar, Tr.TransactionDate, 23) as TransactionDate, tr.UserId as UserId from Transactions tr inner join Users us on tr.UserId = us.UserId
					where tr.DestinationPaymentType=0 
					and tr.IsConfirmed = 1
					and tr.IsCanceled = 0
					and tr.TransactionType in (2,11)"""
			if paymentMethod == 2:
				query+= " and Tr.RemoteLocationID BETWEEN 1 AND 7999"
			elif paymentMethod != 0 and paymentMethod!=2:
				query += " and Tr.RemoteLocationID = '"+str(location)+"'"
			if paymentMethod!=0:
				query += " and Tr.SourcePaymentType = '"+str(method)+"'"
			else:
				query += " and Tr.SourcePaymentType IN (2,3,5,7)"
			query+=") as mix "
			query+="where mix.TransactionDate >= '"+str(monthFrom)+"' and mix.TransactionDate <= '"+str(monthTo)+"'"
			query+="group by mix.OpsegGodina "
			
			if paymentMethod in destinationPaymentMethods:
				query+="""select mix.OpsegGodina as 'Opseg', sum(mix.TransactionAmount) as 'withdraw_sum', count(distinct(mix.UserId)) as 'withdraw_users', count(mix.UserId) as 'withdraw_number' into #wdr from 
						(select case when cast(Tr.TransactionDate as time) < '08:00:00.000' and cast(Tr.TransactionDate as time) >= '00:00:00.000'
						then MONTH(CAST(DATEADD(day,-1,Tr.TransactionDate) as DATE))
						else MONTH(CAST(Tr.TransactionDate as DATE))
						end as OpsegGodina, Tr.TransactionAmount as TransactionAmount, CONVERT(varchar, Tr.TransactionDate, 23) as TransactionDate, tr.UserId as UserId from Transactions tr inner join Users us on tr.UserId = us.UserId
						where tr.SourcePaymentType = 0
						and tr.IsConfirmed = 1
						and tr.IsCanceled = 0
						and tr.TransactionType = 1"""
				if paymentMethod == 2:
					query+= " and Tr.RemoteLocationID BETWEEN 1 AND 7999"
				elif paymentMethod != 0 and paymentMethod!=2:
					query += " and Tr.RemoteLocationID = '"+str(location)+"'"
			
				if paymentMethod!=0:
					query += " and Tr.DestinationPaymentType = '"+str(method)+"'"
				else:
					query += " and Tr.DestinationPaymentType IN (2,3)"
				query+=") as mix "
				query+="where mix.TransactionDate >= '"+str(monthFrom)+"' and mix.TransactionDate <= '"+str(monthTo)+"'"
				query+="group by mix.OpsegGodina "

						#promo
			query+="""select 
  mix.OpsegGodina as 'Opseg', 
  sum(mix.TransactionAmount) as 'promo_sum', 
  count(
    distinct(mix.UserId)
  ) as 'promo_users', 
  count(mix.UserId) as 'promo_number' into #pro from
  (
    select 
      case when cast(Tr.TransactionDate as time) < '08:00:00.000' and cast(Tr.TransactionDate as time) >= '00:00:00.000'
						then MONTH(CAST(DATEADD(day,-1,Tr.TransactionDate) as DATE))
						else MONTH(CAST(Tr.TransactionDate as DATE)) end as OpsegGodina, 
      Tr.TransactionAmount as TransactionAmount, 
	  CONVERT(varchar, Tr.TransactionDate, 23) as TransactionDate,
      tr.UserId as UserId 
    from 
      Transactions tr 
      inner join Users us on tr.UserId = us.UserId 
    where 
      tr.DestinationPaymentType = 0 
      and tr.IsConfirmed = 1 
      and tr.IsCanceled = 0 
      and tr.TransactionType = 2
      and Tr.SourcePaymentType = 6
	  and Tr.DestinationPaymentType = 1
	  and Tr.GameSystem = 1
  ) as mix where mix.TransactionDate >= '"""+str(monthFrom)+"' and mix.TransactionDate <= '"+str(monthTo)+"'"""
			query+="group by mix.OpsegGodina "

			if paymentMethod in destinationPaymentMethods:
				query+="""select d.Opseg, d.deposit_sum, d.deposit_users, d.deposit_number, w.withdraw_sum, w.withdraw_users, w.withdraw_number,coalesce(p.promo_sum,0) as 'promo_sum', coalesce(p.promo_users,0) as 'promo_users', coalesce(p.promo_number,0) as 'promo_number' from #dep d left join #wdr w on d.Opseg=w.Opseg left join #pro p on d.Opseg=p.Opseg order by d.Opseg"""
			else: 
				query+="""select d.Opseg, d.deposit_sum, d.deposit_users, d.deposit_number, 0.00 as 'withdraw_sum', 0 as 'withdraw_users', 0 as 'withdraw_number', coalesce(p.promo_sum,0) as 'promo_sum', coalesce(p.promo_users,0) as 'promo_users', coalesce(p.promo_number,0) as 'promo_number' from #dep d left join #pro p on d.Opseg=p.Opseg order by d.Opseg"""
		if period == 2:
			query = """select mix.OpsegGodina as 'Opseg', sum(mix.TransactionAmount) as 'deposit_sum', count(distinct(mix.UserId)) as 'deposit_users', count(mix.UserId) as 'deposit_number' into #dep from 
					(select case when cast(Tr.TransactionDate as time) < '08:00:00.000' and cast(Tr.TransactionDate as time) >= '00:00:00.000'
					then CAST(DATEADD(day,-1,Tr.TransactionDate) as DATE)
					else CAST(Tr.TransactionDate as DATE)
					end as OpsegGodina, Tr.TransactionAmount as TransactionAmount, tr.UserId as UserId from Transactions tr inner join Users us on tr.UserId = us.UserId
					where tr.DestinationPaymentType=0 
					and tr.IsConfirmed = 1
					and tr.IsCanceled = 0
					and tr.TransactionType in (2,11)"""
			if paymentMethod == 2:
				query+= " and Tr.RemoteLocationID BETWEEN 1 AND 7999"
			elif paymentMethod != 0 and paymentMethod!=2:
				query += " and Tr.RemoteLocationID = '"+str(location)+"'"
			if paymentMethod!=0:
				query += " and Tr.SourcePaymentType = '"+str(method)+"'"
			else:
				query += " and Tr.SourcePaymentType IN (2,3,5,7)"
			query+=") as mix "
			query+="""where """+datesRangeQuery+""
			query+="""group by mix.OpsegGodina """
			
			if paymentMethod in destinationPaymentMethods:
				query+="""select mix.OpsegGodina as 'Opseg', sum(mix.TransactionAmount) as 'withdraw_sum', count(distinct(mix.UserId)) as 'withdraw_users', count(mix.UserId) as 'withdraw_number' into #wdr from
				    (select case when cast(Tr.TransactionDate as time) < '08:00:00.000' and cast(Tr.TransactionDate as time) >= '00:00:00.000'
					then CAST(DATEADD(day,-1,Tr.TransactionDate) as DATE)
					else CAST(Tr.TransactionDate as DATE)
					end as OpsegGodina, Tr.TransactionAmount as TransactionAmount, tr.UserId as UserId from Transactions tr inner join Users us on tr.UserId = us.UserId
					where tr.SourcePaymentType = 0
					and tr.IsConfirmed = 1
					and tr.IsCanceled = 0
					and tr.TransactionType = 1"""
				if paymentMethod == 2:
					query+= " and Tr.RemoteLocationID BETWEEN 1 AND 7999"
				elif paymentMethod != 0 and paymentMethod!=2:
					query += " and Tr.RemoteLocationID = '"+str(location)+"'"
			
				if paymentMethod!=0:
					query += " and Tr.DestinationPaymentType = '"+str(method)+"'"
				else:
					query += " and Tr.DestinationPaymentType IN (2,3)"
				query+=") as mix "
				query+="""where """+datesRangeQuery+""
				query+="""group by mix.OpsegGodina """

				#promo
			query+="""select 
  mix.OpsegGodina as 'Opseg', 
  sum(mix.TransactionAmount) as 'promo_sum', 
  count(
    distinct(mix.UserId)
  ) as 'promo_users', 
  count(mix.UserId) as 'promo_number' into #pro from
  (
    select 
      case when cast(Tr.TransactionDate as time) < '08:00:00.000' 
      and cast(Tr.TransactionDate as time) >= '00:00:00.000' then CAST(
        DATEADD(day,-1, Tr.TransactionDate) as DATE
      ) else CAST(Tr.TransactionDate as DATE) end as OpsegGodina, 
      Tr.TransactionAmount as TransactionAmount, 
      tr.UserId as UserId 
    from 
      Transactions tr 
      inner join Users us on tr.UserId = us.UserId 
    where 
      tr.DestinationPaymentType = 0 
      and tr.IsConfirmed = 1 
      and tr.IsCanceled = 0 
      and tr.TransactionType = 2
      and Tr.SourcePaymentType = 6
	  and Tr.DestinationPaymentType = 1
	  and Tr.GameSystem = 1
  ) as mix where """+datesRangeQuery+""
			query+="group by mix.OpsegGodina "
			if paymentMethod in destinationPaymentMethods:
				query+="""select d.Opseg, d.deposit_sum, d.deposit_users, d.deposit_number, w.withdraw_sum, w.withdraw_users, w.withdraw_number,coalesce(p.promo_sum,0) as 'promo_sum', coalesce(p.promo_users,0) as 'promo_users', coalesce(p.promo_number,0) as 'promo_number' from #dep d left join #wdr w on d.Opseg=w.Opseg left join #pro p on d.Opseg=p.Opseg order by d.Opseg"""
			else: 
				query+="""select d.Opseg, d.deposit_sum, d.deposit_users, d.deposit_number, 0.00 as 'withdraw_sum', 0 as 'withdraw_users', 0 as 'withdraw_number', coalesce(p.promo_sum,0) as 'promo_sum', coalesce(p.promo_users,0) as 'promo_users', coalesce(p.promo_number,0) as 'promo_number' from #dep d left join #pro p on d.Opseg=p.Opseg order by d.Opseg"""
			print(query)
		if period == 3:
			query = ""
		result = self.db.engine.execute(query)
		rows = result.fetchall()
		keys = result.keys()
		tiket = self.db.clean_select_results(rows, keys)
		return {
				'tiket': tiket
			}

  
