import json
import dateparser
import os
import time
import copy
import sys
import threading
from datetime import datetime,timedelta
sys.path.append(os.path.dirname(os.path.realpath(__file__)).rsplit(os.path.sep, 1)[0])
from monitoring.models.fudbal import razrada_model
from monitoring.models.kosarka import kosarka
from monitoring.models.fudbal.map import base_to_code
from monitoring.models import obaranje

dir_path = os.path.dirname(os.path.realpath(__file__)) 
# with open(os.path.join(dir_path, 'lista_asian.json')) as jsonfile:
# 	js_asian = json.load(jsonfile)

# with open(os.path.join(dir_path, 'lista_prod.json')) as jsonfile:
# 	js_prod = json.load(jsonfile)

# with open(os.path.join(dir_path, 'lista_betradar.json')) as jsonfile:
# 	js_betradar = json.load(jsonfile)

sport_default = {'FD' : ['pinnacle', '188bet', 'mansion', 'sbobet', 'cmd'],
				"KO" : ['pinnacle', '188bet', 'mansion', 'sbobet', 'cmd']}
providers = {'pinnacle', '188bet', 'cmd', 'mansion', 'sbobet'}
groups = [['KI 1', 'KI X', 'KI 2'], ['UG 0-2', 'UG 3+']]

def calculate_exp(g1, g2, k1, k2, k3, k4):
	p1_real, p2_real = to_real_2(k1, k2)
	p3_real, p4_real = to_real_2(k3, k4)
	k1_real, k2_real, k3_real, k4_real = 1 / p1_real, 1 / p2_real, 1 / p3_real, 1 / p4_real
	x, y = abs((2 / k1_real) - 1), abs((2 / k3_real) - 1)
	z = g2 - g1
	g = (x / (x + y)) * z + g1

	return g

def to_real_2(k1, k2):
	k1, k2 = float(k1), float(k2)
	p1 = 1 / k1 - (1 / k1 + 1 / k2 - 1) / 2
	p2 = 1 / k2 - (1 / k1 + 1 / k2 - 1) / 2
	return 1/p1, 1/p2

def to_real_3(k1, kx, k2):
	k1, k2, kx = float(k1), float(k2), float(kx)
	p1 = 1 / k1 - (1 / k1 + 1 / k2 + 1 / kx - 1) / 3
	p2 = 1 / k2 - (1 / k1 + 1 / k2 + 1 / kx - 1) / 3
	px = 1 / kx - (1 / k1 + 1 / k2 + 1 / kx - 1) / 3
	return p1, px, p2

def egal(dct, param='handicap'):
	diff = 2
	value = ('H1', 'H2') if param == 'handicap' else ('under', 'over')
	for key in dct:
		razlika = abs(dct[key][value[0]] - dct[key][value[-1]])
		if razlika < diff:
			diff = razlika
			gran = key
	if param == 'total':
		prob = to_real_2(dct[gran][value[0]], dct[gran][value[-1]])[0]
	else:
		if float(gran) < 0:
			prob = to_real_2(dct[gran][value[0]], dct[gran][value[-1]])[0]
		else:
			prob = to_real_2(dct[gran][value[0]], dct[gran][value[-1]])[-1]
	return gran, 1 / prob


def extract_params(dct, provider):
	params = {}
	to_extract = dct[provider]
	if not (to_extract['total'] and to_extract['handicap']):
		return None
	if 'KI X' in to_extract.keys():
		params['prob_x'] = to_real_3(to_extract['KI 1'], to_extract['KI X'], to_extract['KI 2'])[1]
	params['total'], params['prob_total_under'] = egal(to_extract['total'], 'total')
	params['handicap'], params['prob_handicap'] = egal(to_extract['handicap'])
	return params

def parseJson(js):
	dct = {}
	for match in js["data"]:
		if "clientId" not in js['data'][match]:
			continue
		matchId = js['data'][match]['clientId']
		dct[matchId] = {}
		for prov in providers:
			dct[matchId][prov] = {}
		for provider in js['data'][match]['odds']:
			dct[matchId][provider]['handicap'] = {}
			dct[matchId][provider]['total'] = {}
			for odds in js['data'][match]['odds'][provider]:
				if js['data'][match]['odds'][provider][odds]['bettype'] == '3way':
					dct[matchId][provider]['KI 1'] = js['data'][match]['odds'][provider][odds]['q1']
					dct[matchId][provider]['KI X'] = js['data'][match]['odds'][provider][odds]['qx']
					dct[matchId][provider]['KI 2'] = js['data'][match]['odds'][provider][odds]['q2']
				if js['data'][match]['odds'][provider][odds]['bettype'] == 'ou':
					if abs(js['data'][match]['odds'][provider][odds]['ou'] - int(js['data'][match]['odds'][provider][odds]['ou'])) == 0.5:
						dct[matchId][provider]['total'][str(js['data'][match]['odds'][provider][odds]['ou'])] = {"under" : js['data'][match]['odds'][provider][odds]['qu'], "over" : js['data'][match]['odds'][provider][odds]['qo']}		
				if js['data'][match]['odds'][provider][odds]['bettype'] == 'ahc':
					if abs(js['data'][match]['odds'][provider][odds]['hcp'] - int(js['data'][match]['odds'][provider][odds]['hcp'])) == 0.5:
						dct[matchId][provider]['handicap'][str(js['data'][match]['odds'][provider][odds]['hcp'])] = {"H1" : js['data'][match]['odds'][provider][odds]['q1'], "H2" : js['data'][match]['odds'][provider][odds]['q2']}
						if 'clientReverted' in js['data'][match].keys():
							dct[matchId][provider]['handicap'][str(js['data'][match]['odds'][provider][odds]['hcp'])] = {"H1" : js['data'][match]['odds'][provider][odds]['q2'], "H2" : js['data'][match]['odds'][provider][odds]['q1']}
	return dct

def paramsPrepare(d):
	for match in d:
		for provider in [p for p in d[match].keys()]:
			if d[match][provider]:
				d[match][provider] = extract_params(d[match], provider)
	return d

def calculateOdds(params, sport='FD', cov=None):
	x = None
	if sport == 'FD':
		if cov is not None:
			x, odds = razrada_model.real_time_calculation(float(params['total']), 
														 float(params['handicap']), 
											 			 float(params['prob_total_under']), 
									 					 float(params['prob_handicap']),
						 								 cov=cov)
		else:
			x, odds = razrada_model.real_time_calculation(float(params['total']), 
														 float(params['handicap']), 
											 			 float(params['prob_total_under']), 
									 					 float(params['prob_handicap']),
														 float(params['prob_x']))
		
	elif sport == "KO":
		odds = kosarka.real_time_calculation(float(params['total']), 
											float(params['handicap']), 
											float(params['prob_total_under']))
	return x, odds 


def getDiffAsian(json_asian):
	providers=['pinnacle', '188bet']
	diffs = []
	with open(os.path.join(dir_path, 'asian_prepared_stari.json')) as jsonfile:
		asian_prepared = json.load(jsonfile)
	for new in json_asian:
		if new in asian_prepared:
			for prov in providers:
				if json_asian[new][prov] != asian_prepared[new][prov]:
					asian_prepared[new][prov] = json_asian[new][prov]
					diffs.append(new)
		else:
			asian_prepared[new] = json_asian[new]
			diffs.append(new)
	for i in list(asian_prepared.keys()):
		if i not in json_asian:
			asian_prepared.pop(i, None)
	with open(os.path.join(dir_path, 'asian_prepared.json'), 'w') as outfile:
		json.dump(asian_prepared, outfile)
	return list(set(diffs))

def oddsJson(json_asian, json_prod, json_betradar):
	d_asian = parseJson(json_asian)
	all_prepared_asian = paramsPrepare(d_asian)
	for sport in json_prod:
		for competition in json_prod[sport]:
			for match in json_prod[sport][competition]:
				match['provider'] = None
				match['level_betradar'], match['level_asian'] = 0, 0
				match['num_outcomes_betradar'], match['num_outcomes_asian'] = 0, 0
				odds_betradar, odds_asian = None, None
				betradar = [x for x in json_betradar if str(x['matchId']) == str(match['betradar_id'])]
				match['odds'] = {base_to_code[k]:match['odds'][k] for k in match['odds'] if k != 'code' and k!='matchId' and k!='startDate' and k!='betradar_id'}
				if betradar and betradar[0]['total'] and betradar[0]['handicap'] and betradar[0]['prob_total_under'] and betradar[0]['prob_handicap'] and betradar[0]['prob_x']:
					cov, odds_betradar = calculateOdds(betradar[0], sport)
					if str(match['matchId']) in all_prepared_asian.keys():
						for prov in sport_default['FD']:
							if all_prepared_asian[str(match['matchId'])][prov]:
								_, odds_asian = calculateOdds(all_prepared_asian[str(match['matchId'])][prov], sport, cov=cov)
								match['provider'] = prov
								break
				else:
					if str(match['matchId']) in all_prepared_asian.keys():
						for prov in sport_default['FD']:
							if all_prepared_asian[str(match['matchId'])][prov] and "KI X" in all_prepared_asian[str(match['matchId'])][prov].keys():
								_, odds_asian = calculateOdds(all_prepared_asian[str(match['matchId'])][prov], sport)
								match['provider'] = prov
								break
				for k in match['odds']:
					match['odds'][k]['betradar'] = 0
					match['odds'][k]['asian'] = 0
					match['odds'][k]['betradar_difference'] = 0
					match['odds'][k]['asian_difference'] = 0
					match['odds'][k]['obaranje'] = {str(k): 0 for k in obaranje.profiti.keys()}
				if odds_betradar:
					for k in odds_betradar:
						match['odds'][k]['betradar'] = round(1 / odds_betradar[k], 2) if odds_betradar[k] else 0
						match['odds'][k]['betradar_difference'] = 0
						for group in groups:
							if k in group:
								ind = group.index(k)
								for profit in match['odds'][k]['obaranje']:
									if len(group) == 2:
										oborene = obaranje.obaranje_po_ishodima([odds_betradar[group[0]], odds_betradar[group[-1]]], m=float(profit), n=2)
									elif len(group) == 3:
										oborene = obaranje.obaranje_po_ishodima([odds_betradar[group[0]], odds_betradar[group[1]],odds_betradar[group[-1]]], m=float(profit), n=3)
									match['odds'][k]['obaranje'][profit] = oborene[ind]
						if match['odds'][k]['production']:
							match['odds'][k]['betradar_difference'] = 1 - match['odds'][k]['production']/match['odds'][k]['betradar'] if match['odds'][k]['betradar'] else 0
							if match['odds'][k]['betradar_difference'] < 0:
								match['level_betradar'] += match['odds'][k]['betradar_difference']
								match['num_outcomes_betradar'] += 1
				if odds_asian:
					for k in odds_asian:
						match['odds'][k]['asian'] = round(1 / odds_asian[k], 2)
						match['odds'][k]['asian_difference'] = 0
						if match['odds'][k]['production']:
							match['odds'][k]['asian_difference'] = 1 - match['odds'][k]['production']/match['odds'][k]['asian']
							if match['odds'][k]['asian_difference'] < 0:
								 match['level_asian'] += match['odds'][k]['asian_difference']
								 match['num_outcomes_asian'] += 1

	for i in list(range(1,16)):
		try:
			with open(os.path.join(dir_path, 'data.json'),'w') as jsonfile:
				json.dump(json_prod, jsonfile)
				break
		except:
			time.sleep(3)
	else:
		with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
			err.write("[A] Main data write error - "+str(datetime.datetime.now())+"\n")
	return json_prod

def writeProdChanges(json_prod_changes=None):
	l_rem = ['code', 'matchId', 'betradar_id','startDate']
	for i in list(range(1,11)):
		try:
			with open(os.path.join(dir_path, 'data.json')) as jsonfile:
				json_prod = json.load(jsonfile)
				break
		except:
			time.sleep(3)
	else:
		with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
			err.write("[A] Main data read error - "+str(datetime.datetime.now())+"\n")
	match_ids_prod = []
	for comp in json_prod['FD']:
		for match in json_prod['FD'][comp]:
				match_ids_prod.append(str(match['matchId']))
				prod_changes = []
				if comp in json_prod_changes['FD'].keys():
					prod_changes = [m for m in json_prod_changes['FD'][comp] if str(match['matchId']) == str(m['matchId'])]
				if prod_changes:
					m = prod_changes[0]
					json_prod_changes['FD'][comp].remove(m)

					match['level_betradar'], match['level_asian'] = 0, 0
					match['num_outcomes_betradar'], match['num_outcomes_asian'] = 0, 0
					match['provider'] = None

					for od in m['odds']:
						if od not in l_rem:
							odd = base_to_code[od]
							if match['odds'][odd]['production']:
								match['odds'][odd]['production'] = m['odds'][od]['production']
								match['odds'][odd]['betradar_difference'] = 1 - match['odds'][odd]['production']/match['odds'][odd]['betradar'] if match['odds'][odd]['betradar'] > 0 else 0
								match['odds'][odd]['asian_difference'] = 1 - match['odds'][odd]['production']/match['odds'][odd]['asian'] if match['odds'][odd]['asian'] > 0 else 0
								if match['odds'][odd]['betradar_difference'] < 0:
									match['num_outcomes_betradar'] += 1
									match['level_betradar'] += match['odds'][odd]['betradar_difference']
								if match['odds'][odd]['asian_difference'] < 0:
									match['num_outcomes_asian'] += 1
									match['level_asian'] += match['odds'][odd]['asian_difference']

	for comp in json_prod_changes['FD']:
		for m in json_prod_changes['FD'][comp]:
			if str(m['matchId']) not in match_ids_prod:
				new = {}
				for key in m['odds'].keys():
					if key!='code' and key!='matchId' and key!='betradar_id' and key!='startDate':
						new[base_to_code[key]] = m['odds'][key]
				
				m['odds'] = new
				# m['odds'] = {base_to_code[k]:m['odds'][k] for k in m['odds'].keys() if k != 'code' and k!='matchId' and k!='betradar_id'}
				for k in m['odds']:
					m['odds'][k]['betradar'] = 0
					m['odds'][k]['asian'] = 0
					m['odds'][k]['betradar_difference'] = 0
					m['odds'][k]['asian_difference'] = 0
					m['odds'][k]['obaranje'] = {str(k): 0 for k in obaranje.profiti.keys()}
				m['level_betradar'], m['level_asian'] = 0, 0
				m['num_outcomes_betradar'], m['num_outcomes_asian'] = 0, 0
				m['provider'] = None
				if comp not in json_prod['FD'].keys():
					json_prod['FD'][comp] = []
				json_prod['FD'][comp].append(m)
	with open(os.path.join(dir_path, 'aktuelni.json')) as jsonfile:
		codes_novo = json.load(jsonfile)['aktuelni']

	for comp in json_prod['FD']:
		for match in json_prod['FD'][comp]:
			if match['Code'] not in codes_novo:
				json_prod['FD'][comp].remove(match)

	for i in list(range(1,11)):
		try:
			with open(os.path.join(dir_path, 'data.json'), 'w') as outfile:
				json.dump(json_prod, outfile)
				break
		except:
			time.sleep(3)
	else:
		with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
			err.write("[A] Main data write error - "+str(datetime.datetime.now())+"\n")

	return json_prod

def setInterval(func,time):
	e = threading.Event()
	while not e.wait(time):
		func()

def calculateOddsDiff(json_asian, json_prod_changes, json_betradar, mode):
	with open(os.path.join(dir_path, 'process_running.json')) as jsonfile:
		r = json.load(jsonfile)
	if r['is_process_running'] == 0:
		with open(os.path.join(dir_path, 'process_running.json'), 'w') as outfile:
				json.dump({"is_process_running":1}, outfile)
		json_prod_changes_cpy = copy.deepcopy(json_prod_changes)
		d_asian = parseJson(json_asian)
		all_prepared_asian = paramsPrepare(d_asian)
		diffs = getDiffAsian(all_prepared_asian)
		diffs_cov = [[d, 0.1] for d in diffs]
		with open(os.path.join(dir_path, 'asian_prepared_stari.json')) as jsonfile:
			asian_prepared = json.load(jsonfile)
		json_prod = writeProdChanges(json_prod_changes)
		matches = []
		comps = []
		for m in json_betradar: 
			if m['total'] and m['handicap'] and m['prob_total_under'] and m['prob_handicap'] and m['prob_x']:
				for comp in json_prod['FD']:
					for match in json_prod['FD'][comp]:
						cov = 0.1
						if str(match['betradar_id']) == str(m['matchId']):
							cov, odds_betradar = calculateOdds(m)
							match['level_betradar'] = 0
							match['num_outcomes_betradar'] = 0
							for k in odds_betradar:
								if k not in match['odds'].keys() and k not in ['PD 1', 'PD 2']:
									match['odds'][k] = {"production": 0, "betradar_difference":0, "asian_difference":0, "betradar":0, "asian":0}
								match['odds'][k]['betradar'] = round(1 / odds_betradar[k], 2) if odds_betradar[k] else 0
								match['odds'][k]['betradar_difference'] = 0
								match['odds'][k]['obaranje'] = {str(k): 0 for k in obaranje.profiti.keys()}
								for group in groups:
									if k in group:
										ind = group.index(k)
										for profit in match['odds'][k]['obaranje']:
											if len(group) == 2:
												oborene = obaranje.obaranje_po_ishodima([odds_betradar[group[0]], odds_betradar[group[-1]]], m=float(profit), n=2)
											elif len(group) == 3:
												oborene = obaranje.obaranje_po_ishodima([odds_betradar[group[0]], odds_betradar[group[1]],odds_betradar[group[-1]]], m=float(profit), n=3)
											match['odds'][k]['obaranje'][profit] = oborene[ind]
								if match['odds'][k]['production']:
									match['odds'][k]['betradar_difference'] = 1 - match['odds'][k]['production']/match['odds'][k]['betradar'] if match['odds'][k]['betradar'] else 0
									if match['odds'][k]['betradar_difference'] < 0:
										match['level_betradar'] += match['odds'][k]['betradar_difference']
										match['num_outcomes_betradar'] += 1

							asian_match = [d for d in diffs_cov if str(d[0]) == str(match['matchId'])]
							if asian_match:
								diffs_cov[diffs_cov.index(asian_match[0])] = [asian_match[0][0], cov]
							if mode is None:
								matches.append(str(match['matchId']))
							break
			else:
				for comp in json_prod['FD']:
					for match in json_prod['FD'][comp]:
						if str(match['betradar_id']) == str(m['matchId']):
							for odd in match['odds'].keys():
								if odd != 'code' and odd!='matchId' and odd!='startDate' and odd!='betradar_id':
									match['odds'][odd]['betradar'] = 0
									match['odds'][odd]['betradar_difference'] = 0
									match['odds'][odd]['obaranje'] = {"0.03": 0, "0.05": 0, "0.075": 0, "0.1": 0}
									match['level_betradar'] = 0
									match['num_outcomes_betradar'] = 0

		# for m in diffs_cov:
		# 	for comp in json_prod['FD']:
		# 		for match in json_prod['FD'][comp]:
		# 				if str(match['matchId']) == str(m[0]):
		# 					for prov in sport_default['FD']:
		# 						if asian_prepared[str(match['matchId'])][prov]:
		# 							_, odds_asian = calculateOdds(asian_prepared[str(match['matchId'])][prov], cov=m[-1])
		# 							match['provider'] = prov
		# 							match['level_asian'] = 0
		# 							match['num_outcomes_asian'] = 0
		# 							for k in odds_asian:
		# 								match['odds'][k]['asian'] = round(1 / odds_asian[k], 2)
		# 								match['odds'][k]['asian_difference'] = 0
		# 								if match['odds'][k]['production']:
		# 									match['odds'][k]['asian_difference'] = 1 - match['odds'][k]['production']/match['odds'][k]['asian']
		# 									if match['odds'][k]['asian_difference'] < 0:
		# 										match['level_asian'] += match['odds'][k]['asian_difference']
		# 										match['num_outcomes_asian'] += 1
		# 						if mode is None:
		# 							matches.append(int(match['matchId']))
		# 					break
		if mode is None:
			matches = list(set(matches))
			for compet in json_prod_changes_cpy['FD']:
				for mat in json_prod_changes_cpy['FD'][compet]:
					if str(mat['matchId']) not in matches:
						matches.append(str(mat['matchId']))
			final = {"FD":{}}
			for comp in json_prod['FD']:
				for m in json_prod['FD'][comp]:
					if str(m['matchId']) in matches:
						if comp not in final['FD'].keys():
							final['FD'][comp] = []
						final['FD'][comp].append(m)
			
			for i in list(range(1,11)):
				try:
					with open(os.path.join(dir_path, 'razlika.json'), 'w') as outfile:
						json.dump(final, outfile)
					break
				except:
					time.sleep(3)
			else:
				with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
					err.write("[A] Razlika write error - "+str(datetime.datetime.now())+"\n")
				with open(os.path.join(dir_path, 'process_running.json'), 'w') as outfile:
					json.dump({"is_process_running":0}, outfile)
			#setInterval(exec(open(dir_path+'/lista.py').read()), 30)
			for i in list(range(1,16)):
				try:
					with open(os.path.join(dir_path, 'data.json'), 'w') as outfile:
						json.dump(json_prod, outfile)
						break
				except:
					time.sleep(3)
			else:
				with open(os.path.join(dir_path, 'monitoring/error_log.txt'),'a') as err:
					err.write("[A] Main data write error - "+str(datetime.datetime.now())+"\n")
			with open(os.path.join(dir_path, 'process_running.json'), 'w') as outfile:
				json.dump({"is_process_running":0}, outfile)
		else:
			return json_prod


if __name__ == '__main__':
	#son_prod = oddsJson(js_asian, js_prod, js_betradar)
	#asianDiff = getDiffAsian()
	with open(os.path.join(dir_path, 'betradardiff.json')) as jsonfile:
		betDiff = json.load(jsonfile)


	calculateOddsDiff(js_asian, js_prod, betDiff)
	#writeProdChanges({"FD": {"Srbija 1":[]}})
