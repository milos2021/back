from flask import request, Flask, jsonify
from flask_restful import Resource
from sqlalchemy import text as sql_text
import json
import mysql.connector
import os
from monitoring.betradar_mapping import extractTotal, extractHandicap, extract1X2
from monitoring.asian import oddsJson, calculateOddsDiff
import requests
from datetime import datetime

class TestGet(Resource):

    def __init__(self):
        print("init")

    def get(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) 
        
        with open(os.path.join(dir_path, 'data.json')) as jsonfile:
            result = json.load(jsonfile)

        
        return result


        

   

        

   