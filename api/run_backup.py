from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api
from views import Tiket
from cashflow import Cashflow
from sport import Sport
from betgame import BetGame
from betgameoutcome import BetGameOutcome
from competition import Competition
from sport_report import SportReport
from rep_stats import RepStats
from slip_detailed_preview import SlipDetailedPreview
from session_manager import SessionManager
from advanced_statistic_for_period import AdvancedStatisticForPeriod
from monitoring.local import TestGet
from user_report_3 import UserReport3
from statistic_user_report import StatisticUserReport
from statistic_user_data import StatisticUserData
from ludi_tiketi import LudiTiketi
from cashflow_today import CashflowToday
from prematch_load import PrematchLoad
from slip_view import SlipView

# import os

# dir_path = os.path.dirname(os.path.realpath(__file__))
# monitoring_path = os.path.join(dir_path, 'monitoring')


def create_app():
	app = Flask(__name__)
	app.secret_key = "TWlzYURva3Rvcg==" 
	CORS(app, support_credentials=True)
	api = Api(app)
	#simple api
	api.add_resource(Sport, '/api/Sport')
	api.add_resource(Competition, '/api/Competition')
	api.add_resource(BetGame, '/api/BetGame')
	api.add_resource(BetGameOutcome, '/api/BetGameOutcome')
	#section api
	api.add_resource(Tiket,'/api/Tiket')
	api.add_resource(RepStats,'/api/RepStats')
	api.add_resource(Cashflow,'/api/Cashflow')
	api.add_resource(SportReport, '/api/SportReport')
	api.add_resource(AdvancedStatisticForPeriod, '/api/AdvancedStatisticForPeriod')
	api.add_resource(SlipDetailedPreview, '/api/SlipDetailedPreview')
	#session
	api.add_resource(SessionManager, '/api/session')
	#user_reporting
	api.add_resource(UserReport3, '/api/UserReport3')
	api.add_resource(StatisticUserReport, '/api/StatisticUserReport')
	api.add_resource(StatisticUserData, '/api/StatisticUserData')
	api.add_resource(LudiTiketi, '/api/LudiTiketi')
	#today
	api.add_resource(CashflowToday, '/api/CashflowToday')
	api.add_resource(PrematchLoad, '/api/PrematchLoad')
	api.add_resource(SlipView, '/api/SlipView')
	return app
