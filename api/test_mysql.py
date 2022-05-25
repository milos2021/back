from db import Db
from db_land import DbLand
from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
from datetime import datetime, timedelta
import json
import mysql.connector
import os
import pandas as pd
import numpy as np
db = Db()
with db.engine.begin() as conn:
	query = "SELECT top(5) CompetitionName from Competitions"
	result = db.engine.execute(query)
	rows = result.fetchall()
	keys = list(result.keys())
	data = db.clean_select_results(rows, keys)
	s = [x for x in data]
	db.__del__()
	print(s[0]['CompetitionName'])
