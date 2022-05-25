from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import create_engine, MetaData
import urllib


class DbLand():

    def __init__(self):
        # db_url = "mssql+pymssql://milos:Soccer123!@10.0.160.136/BetModel_PROD" #1443
        # self.engine = create_engine(db_url)
        params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"  
                                 "SERVER=87.237.207.202;"
                                 "DATABASE=BetModel_PROD;"
                                 "UID=mdjacic;"
                                 "PWD=byMJnUT>KhIAaLkQ;"
                                 "ApplicationIntent=readonly")       
        self.engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
        # self.engine = create_engine(db_url)
        self.connection = self.engine.connect()
        ## db_url = "mssql+pymssql://ro_prod:44CTMCqprABGuLQgrn@10.252.0.200/BetModel_PROD" #1443
    def __del__(self):
        self.connection.close()

    def clean_select_row(self, row, keys):
        try:
            clean_row = [str(field) if isinstance(field, datetime) or isinstance(
                field, Decimal) or isinstance(field, date) else field for field in list(row)]
            current_row = {}
            for i in range(len(keys)):
                current_row[keys[i]] = clean_row[i]
            return current_row
        except:
            return None

    def clean_select_results(self, data, keys):
        if len(data) == 0:
            return {}
        result_data = []
        for row in data:
            result_data.append(self.clean_select_row(row, keys))
        return result_data
