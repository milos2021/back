import math
import numpy as np
import pickle
import joblib
import os
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
data3 = pickle.load(open(os.path.join(dir_path, 'pickles/data_dict_3.pickle'), 'rb'), encoding='bytes')
zaokruzivanje = pd.read_excel(open(os.path.join(dir_path, 'zaokruzivanje.xlsx'), 'rb'))

profiti = {0.03: 0.025, 0.05: 0.035, 0.075: 0.05, 0.085: 0.05, 0.1: 0.065}
limiti = {0.03: 0.74, 0.05: 0.822, 0.075: 0.845, 0.085: 0.877, 0.1: 0.857}
# format (profit, prob1, prob2): margina

obaranje_sabloni = {'param2': {'osnovne 3types': (0.02, 3), 'osnovne 2types': (0.05, 2), 
							   '2types': (0.05, 2), '3types': (0.075, 3), '4types': (0.1, 4),
							   '9types': (0.15, 9), 'Yes/No': (0.05, 2), 'Yes/No uk': (0.075, 2), 
							   '17types': (0.3, 17), '26types': (0.4, 26)},

					'param4': {'osnovne 3types': (0.04, 3), 'osnovne 2types': (0.05, 2), 
							   '2types': (0.05, 2), '3types': (0.075, 3), '4types': (0.1, 4),
							   '9types': (0.15, 9), 'Yes/No': (0.05, 2), 'Yes/No uk': (0.075, 2), 
							   '17types': (0.3, 17), '26types': (0.4, 26)},

					'param6': {'osnovne 3types': (0.06, 3), 'osnovne 2types': (0.075, 2), 
							   '2types': (0.075, 2), '3types': (0.075, 3), '4types': (0.12, 4),
							   '9types': (0.18, 9), 'Yes/No': (0.075, 2), 'Yes/No uk': (0.075, 2), 
							   '17types': (0.3, 17), '26types': (0.4, 26)},

					'param8': {'osnovne 3types': (0.08, 3), 'osnovne 2types': (0.075, 2), 
							   '2types': (0.075, 2), '3types': (0.1, 3), '4types': (0.12, 4),
							   '9types': (0.2, 9), 'Yes/No': (0.1, 2), 'Yes/No uk': (0.1, 2), 
							   '17types': (0.3, 17), '26types': (0.4, 26)},

					'param10': {'osnovne 3types': (0.1, 3), 'osnovne 2types': (0.075, 2), 
							   '2types': (0.075, 2), '3types': (0.12, 3), '4types': (0.15, 4),
							   '9types': (0.2, 9), 'Yes/No': (0.1, 2), 'Yes/No uk': (0.1, 2), 
							   '17types': (0.3, 17), '26types': (0.4, 26)}
							   }

def obaranje_formula(p, m=0.075, n=2):
	if p > 0:
		pz = 1 / math.exp(-math.log(n * (1 - m)) * math.log(1 / p) / math.log(n))
	else:
		pz = 0
	return pz


def obaranje_fiksiranje(prob_list, m):
	p1, p2 = prob_list[0], prob_list[1]
	if p1 > p2:
		o2 = obaranje_formula(p2, m, n=2)
		o1 = 1 / (1 / (1 - profiti[m]) - 1 / o2)
	else:
		o1 = obaranje_formula(p1, m, n=2)
		o2 = 1 / (1 / (1 - profiti[m]) - 1 / o1)

	return [round(o1, 2), round(o2, 2)]


def obaranje_po_ishodima(prob_list, m, n):
	if sum(prob_list) == 0:
		return prob_list
	'''
	prob_list - lista verovatnoca za obaranje na jedan set outcome-a koji cine celinu (primer k1, kx i k2), ona ne moze biti kraca od n - 1
	m - zeljeni profit
	n - broj ishoda 
	'''
	if n > len(prob_list) + 1:
		print('Broj prosledjenih verovatnoca je nedovoljan za uneseno n')
		return []

	if m == 0:
		oborene = [round(1 / prob, 2) for prob in prob_list]
		return oborene

	added = False
	if len(prob_list) < n:
		added_prob = 1 - sum(prob_list)
		prob_list.append(added_prob)
		added = True

	oborene = []
	if n == 2:
		if max(prob_list) > limiti[m]:
			oborene = obaranje_fiksiranje(prob_list, m)
		else:
			oborene = [round(obaranje_formula(prob, m, n), 2) for prob in prob_list]

	elif n == 3:
		sorted_inds = list(np.argsort(prob_list)[::-1])
		if prob_list[sorted_inds[0]] > 0.94:
			margina = 0.2
		else:
			dict_key = (round(m, 3), round(prob_list[sorted_inds[0]], 2), round(prob_list[sorted_inds[1]], 2))
			if dict_key[1]+dict_key[2] >= 1:
				dict_key_new = (dict_key[0], dict_key[1], round(dict_key[2]-0.01,2))
				margina = data3[dict_key_new]
			else:
				margina = data3[dict_key]
		oborene = [round(obaranje_formula(prob, margina, n), 2) for prob in prob_list]

	else:
		oborene = [round(obaranje_formula(prob, m, n), 2) for prob in prob_list]

	if added:
		oborene.pop(-1)

	oborene_zaok = []
	for od in oborene:
		df = zaokruzivanje[(od >= zaokruzivanje['Od']) & (od <= zaokruzivanje['Do'])]
		if not df.empty:
			od = df['Kvota'].values[0]
		oborene_zaok.append(od)
	return oborene_zaok


if __name__ == '__main__':
	# poziva se samo funkcija obaranje_po_ishodima, verovatnoce se prosledjuju u bilo kom redosledu
	# primer 3 ishoda
	p1, p2, p3 = 0.96, 0.03, 0.01
	print(obaranje_po_ishodima([p1, p2, p3], m=0.06, n=3))
	# primer 2 ishoda
	print(obaranje_po_ishodima([0.95, 0.05], m=0.075, n=2))
	# primer 2 ishoda u slucaju da nemamo kontru
	print(obaranje_po_ishodima([0.95], m=0.075, n=2))
	