# -*- coding: utf-8 -*-
from __future__ import division
import os
import numpy as np
import time
import warnings
import operator as op
import math
from scipy.stats import poisson
import pickle
from joblib import load
from map import mapping

# from parametar_tenis.models import Zaokruzivanje
warnings.filterwarnings("ignore")

'''
Ova skripta sluzi za racunanje celokupne ponude u rukometu. Jedina funkcija koja je vama bitna je real_time_calculation (objasnjenja imate u funkciji).
Ostale sluze samo kako bi ih ona pozivala. U prilogu dobijate i 4 joblib file-a neophodna za racunicu. Prebaceno na .python 3.6
'''


def poisson_probs(lam):
    s = 0
    for x in range(int(2*lam)):
        s += poisson.pmf(x, lam, loc=0)
        

def eval_sample(granica_ou, granica_hd):
    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    model_1 = load(os.path.join(dir_path, 'model_1.joblib'))
    model_x =load(os.path.join(dir_path, 'model_x.joblib'))
    scaler =load(os.path.join(dir_path, 'scaler.joblib'))

    sample = np.array([granica_ou, granica_hd]).reshape(1, -1)
    sample = scaler.transform(sample)
    real_probs_1 = model_1.predict_proba(sample)
    real_probs_x = model_x.predict_proba(sample)

    p1, px = real_probs_1[0, 1], real_probs_x[0, 1]
    if p1 + px >= 1:
        px = (1 - p1) / 2
        p2 = px
    else: 
        p2 = 1 - p1 - px
    return p1, px, p2


def eval_prelazi(granica_ou, granica_hd):
    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    model = load(os.path.join(dir_path, 'model_prelazi.joblib'))
    class_map = {'1-1': 0, '1-X': 1, '1-2': 2, 'X-1':3, 'X-X': 4, 'X-2': 5, '2-1': 6, '2-X': 7, '2-2': 8}

    id_map = {class_map[key]: key for key in class_map}
    sample = np.array([granica_ou, granica_hd]).reshape(1, -1)
    real_probs = model.predict_proba(sample).reshape(-1, 1)

    odds_prelazi = {}
    for i in range(real_probs.shape[0]):
        odds_prelazi[id_map[i]] = real_probs[i][0]

    return odds_prelazi


def create_matrix(lam1, lam2, num):
    x = np.arange(0, num, 1)
    y = np.arange(0, num, 1)
    poisson1 =  poisson.pmf(x, lam1, loc=0)
    poisson2 =  poisson.pmf(y, lam2, loc=0)
    final = np.outer(poisson1, poisson2)
    return final


def nck(n, r):
    r = min(r, n-r)
    if r == 0:
        return 1
    numer = reduce(op.mul, xrange(n, n - r, -1))
    denom = reduce(op.mul, xrange(1, r + 1))
    return numer//denom


def create_matrix_bin(lam1, lam2, n):
    num = int(n)
    p1 = float(lam1) / num
    p2 = float(lam2) / num
    bin1 = np.array([nck(num, k) * (p1 ** float(k)) * ((1 - p1) ** float(num - k)) for k in range(num)])
    bin2 = np.array([nck(num, k) * (p2 ** float(k)) * ((1 - p2) ** float(num - k)) for k in range(num)])
    final = np.outer(bin1, bin2)
    return final


def to_real_3(k1, kx, k2):
    k1, k2, kx = float(k1), float(k2), float(kx)
    p1 = 1 / k1 - (1 / k1 + 1 / k2 + 1 / kx - 1) / 3
    p2 = 1 / k2 - (1 / k1 + 1 / k2 + 1 / kx - 1) / 3
    px = 1 / kx - (1 / k1 + 1 / k2 + 1 / kx - 1) / 3
    return p1, px, p2


def get_exps(gran_ou, hend):
    lam1 = gran_ou / 2 + hend / 2
    lam2 = gran_ou / 2 - hend / 2
    return lam1, lam2


def to_real_2(k1, k2):
    k1, k2 = float(k1), float(k2)
    p1 = 1 / k1 - (1 / k1 + 1 / k2 - 1) / 2
    p2 = 1 / k2 - (1 / k1 + 1 / k2 - 1) / 2
    return p1, p2


def egal(odds, k):
    diff = 1
    gran = 0
    for key in odds:
        razlika = abs(odds[key][k] - 0.5)
        if razlika < diff:
            diff = razlika
            gran = key
    return gran, odds[gran]


def calc_game(mat1, mat2):
    mask = np.multiply(mat1, mat2)
    mask[mask > 0] = 1
    return np.sum(np.multiply(mat1, mask))


def calc_over(final, n):
    overs = {}
    
    for i in range(int(n)):
        gran1 = n + i + 0.5
        gran2 = n - i - 0.5
        under1 = np.sum(np.triu(np.fliplr(final), k=-i-1))
        under2 = np.sum(np.triu(np.fliplr(final), k=i))
        overs[gran1] = {'+': 1 - under1, '-': under1}
        overs[gran2] = {'+': 1 - under2, '-': under2}
    return overs


def calc_hend(final, n):
    hends = {}

    for i in range(int(n)):
        gran1 = i + 0.5
        gran2 = - i - 0.5
        h1 = np.sum(np.tril(final, k=i))
        h2 = np.sum(np.triu(final, k=-i))
        hends[gran1] = {'h1': h1, 'h2': 1 - h1}
        hends[gran2] = {'h1': 1 - h2, 'h2': h2}

    return hends


def create1x2(mat):
    k2 = np.triu(mat, k=1)
    k1 = np.tril(mat, k=-1)
    tmp1 = np.sum(k1)
    tmp2 = np.sum(k2)
    kx = np.diag(mat)
    tmpX = np.sum(kx)
    return tmp1, tmpX, tmp2


def calculate_odds_different(p, m=0.075, n=2):
    if p > 0:
        pz = 1 / math.exp(-math.log(n * (1 - m)) * math.log(1 / p) / math.log(n))
    else:
        pz = 0
    return pz


def find_closest(lam, mat, tip):
    gran_1, gran_2, gran_3 = round(lam) + 0.5, round(lam) - 0.5, round(lam) + 1.5
    if tip == 'prvi':
        tm = {gran_1: np.sum(mat[(int(round(lam)) + 1):, 0:]), gran_2: np.sum(mat[(int(round(lam))):, 0:]), gran_3: np.sum(mat[(int(round(lam)) + 2):, 0:])}
    else:
        tm = {gran_1: np.sum(mat[0:, (int(round(lam)) + 1):]), gran_2: np.sum(mat[0:, (int(round(lam))):]), gran_3: np.sum(mat[0:,(int(round(lam)) + 2):])}
    
    grantm, vredtm = min(tm.items(), key=lambda v: abs(v[1] - 0.5))
    return grantm, vredtm


def alternative(odds, num_gran, granica, full, base):
    if 'H' in base[0]:
        parts = ('h1', 'h2')
        str_gran = 'granica_hd'
    else:
        str_gran = 'granica_ou'
        parts = ('+', '-')

    for i in range(num_gran):
        if i == 0:
            ext = ''
        else:
            ext = str(i)
        odds[ext + base[0]] = {str_gran: granica - (num_gran - 1) / 2 + i, 'vrednost': full[granica - (num_gran - 1) / 2 + i][parts[0]]}
        odds[ext + base[1]] = {str_gran: granica - (num_gran - 1) / 2 + i, 'vrednost': full[granica - (num_gran - 1) / 2 + i][parts[1]]}
        

def both_teams(mat):
    tm1_tm2 = {}
    for i in range(0, 80):
        gran = i + 0.5
        over = np.sum(mat[(i):, (i):])
        tm1_tm2[gran] = {'over': over, 'under': 1 - over}
    gran_over_oba, otp = egal(tm1_tm2, 'over')
    
    return gran_over_oba, otp


def create_line(lam1, lam2):
    odds = {}
    n = 50
    final = create_matrix(lam1, lam2, n)
    first = create_matrix(lam1 / 2, lam2 / 2, int(n / 2))
    k1, k2 = np.tril(final, k=-1), np.triu(final, k=1)
    k1_first, k2_first = np.tril(first, k=-1), np.triu(first, k=1)

    odds['KI 1'], odds['KI 2'], odds['KI X'] = np.sum(k1), np.sum(k2), np.sum(np.diag(final))
    odds['Ipol 1'], odds['Ipol 2'], odds['Ipol X'] = np.sum(k1_first), np.sum(k2_first), np.sum(np.diag(first))

    odds['DP 1'] = odds['Ipol 1'] ** 2
    odds['DP 2'] = odds['Ipol 2'] ** 2
    overs = calc_over(final, n)
    granica_ou, over = egal(overs, '+')
    odds['|+|'] = {'granica_ou': granica_ou, 'vrednost': overs[granica_ou]['+']}
    odds['|-|'] = {'granica_ou': granica_ou, 'vrednost': overs[granica_ou]['-']}

    overs_first = calc_over(first, n/2)
    granica_ou_first, over_first = egal(overs_first, '+')
    odds['Ipol |+|'] = {'granica_ou': granica_ou_first, 'vrednost': overs_first[granica_ou_first]['+']}
    odds['Ipol |-|'] = {'granica_ou': granica_ou_first, 'vrednost': overs_first[granica_ou_first]['-']}
    odds['IIpol |+|'] = odds['Ipol |+|']
    odds['IIpol |-|'] = odds['Ipol |-|']

    hends = calc_hend(final)
    gran_hend, hend = egal(hends, 'h1')
    odds['H1'] = {'granica_hd': -gran_hend, 'vrednost': hends[gran_hend]['h1']}
    odds['H2'] = {'granica_hd': gran_hend, 'vrednost': hends[gran_hend]['h2']}

    hends_first = calc_hend(first)
    gran_hend_first, hend_first = egal(hends_first, 'h1')
    odds['Ipol H1'] = {'granica_hd': -gran_hend_first, 'vrednost': hends[gran_hend_first]['h1']}
    odds['Ipol H2'] = {'granica_hd': gran_hend_first, 'vrednost': hends[gran_hend_first]['h2']}

    return odds


def prelazi(first, rest, odds, n):
    odds_prelazi = {'1-1': 0, '1-2': 0, '2-1': 0, '2-2': 0, '1-X': 0, '2-X': 0}

    for i in range(1, n + 1):
        odds_prelazi['1-1'] += np.sum(np.diag(first, k=-i)) * np.sum(np.tril(rest, k=i-1))
        odds_prelazi['2-2'] += np.sum(np.diag(first, k=i)) * np.sum(np.triu(rest, k=1-i))
        odds_prelazi['1-2'] += np.sum(np.diag(first, k=-i)) * np.sum(np.triu(rest, k=(i+1)))
        odds_prelazi['2-1'] += np.sum(np.diag(first, k=i)) * np.sum(np.tril(rest, k=-(i+1)))
        odds_prelazi['1-X'] += np.sum(np.diag(first, k=-i)) * np.sum(np.diag(rest, k=i))
        odds_prelazi['2-X'] += np.sum(np.diag(first, k=i)) * np.sum(np.diag(rest, k=-i))

    odds_prelazi['X-1'] = np.sum(np.diag(first)) * np.sum(np.tril(rest, k=-1))
    odds_prelazi['X-2'] = np.sum(np.diag(first)) * np.sum(np.triu(rest, k=1))
    odds_prelazi['X-X'] = np.sum(np.diag(first)) * np.sum(np.diag(rest))

    odds.update(odds_prelazi)


def lin_inc(start, end, x):
    a = (end[1] - start[1]) / (end[0] - start[0])
    b = start[1] - a * start[0]
    y = a * x + b
    return y


def real_time_obaranje(odds, margin=0.075):
    # to do
    return odds


def odds_correction(odds, final):
    k1, k2, kx = np.sum(np.tril(final, k=-1)), np.sum(np.triu(final, k=1)), np.sum(np.diag(final))
    diff1, diffX, diff2 = k1 - odds['K1'], kx - odds['KX'], k2 - odds['K2']

    odds['1&-']['vrednost'] -= diff1 / 2
    odds['1&+']['vrednost'] -= diff1 / 2
    odds['2&-']['vrednost'] -= diff2 / 2
    odds['2&+']['vrednost'] -= diff2 / 2
    


def real_time_calculation(gran, hend, gran_first=None, hend_first=None, n=80, margin=0.075, model=1, real_probs=False):
    '''
    gran - granica over/under full time (obavezan parametar)
    hend - granica hendikep full time (obavezan parametar)
    gran_first, hend_first - granice over/under i hendikep poluvreme. Ovi parametri nisu obavezni i samo ako postoje oba prosledjuju se funkciji
    n - velicina matrice, za sada ne menjati vrednost
    margin - zeljena zarada. Trenutno postoje varijante za 0.05, 0.075 i 0.1
    model - u ovom slucaju, moguce vrednosti su 1 i 2
    real_probs - True vraca realne verovatnoce, a False produkcijske kvote

    Parametri n, margin i model ce biti definisani zavisno od takmicenja ili po mecu na neki nacin. Za potrebe testiranja ih drzati na default-nim vrednostima. 
    Parametar real_probs za potrebe testiranja drzati na True. Zahteva citanje iz tabele Zaokruzivanje koju sada ne prosledjujemo. 
    Dole je primer jednog poziva funkcije koji vraca realne verovatnoce.
    '''

    reverse = False
    if hend > 0:
        reverse = True
    
    hend = abs(hend)
    if hend_first:
        hend_first = abs(hend_first)

    lam1, lam2 = get_exps(gran, hend)
    gran, hend = float(gran), float(hend)
    n_first = n / 2
    n_sec = n / 2
    if gran_first and hend_first:
        lam1_first, lam2_first = get_exps(gran_first, hend_first)
    else:
        lam1_first, lam2_first = 0.493 * lam1, 0.493 * lam2
        gran_first, hend_first = gran*0.493, hend*0.493
    lam1_sec, lam2_sec = lam1 - lam1_first, lam2 - lam2_first
    
    final = create_matrix(lam1, lam2, n)
    first = create_matrix(lam1_first, lam2_first, n_first)
    sec = create_matrix(lam1_sec, lam2_sec, n_sec)

    pol2 = np.sum(np.triu(first, k=1))
    pol1 = np.sum(np.tril(first, k=-1))
    polx = 1 - pol1 - pol2

    dpol2 = np.sum(np.triu(sec, k=1))
    dpol1 = np.sum(np.tril(sec, k=-1))
    dpolx = 1 - dpol1 - dpol2 

    odds = {}
    p1, px, p2 = eval_sample(gran, hend)
    odds_prelazi = eval_prelazi(gran, hend)
    odds['K1'], odds['KX'], odds['K2'] = p1, px, p2
    if model == 2:
        if odds['K1'] < 0.92:
            odds['K1'] *= 1.05
            odds['KX'] *= 1.15
            odds['K2'] = 1 - odds['K1'] - odds['KX']
    
    p1, px, p2 = eval_sample(gran_first, hend_first)
    gran_ou_sec, gran_hend_sec = gran - gran_first, hend - hend_first
    dp1, dpx, dp2 = eval_sample(gran_ou_sec, gran_hend_sec)
    
    if hend < 1.5:
        odds['P1'], odds['PX'], odds['P2'] = pol1, polx, pol2
        odds['DP1'], odds['DPX'], odds['DP2'] = dpol1, dpolx, dpol2
    else:
        odds['P1'], odds['PX'], odds['P2'] = p1, px, p2
        odds['DP1'], odds['DPX'], odds['DP2'] = dp1, dpx, dp2
    
    odds['W1'], odds['W2'] = (1 / (1 - odds['KX'])) * odds['K1'], (1 / (1 - odds['KX'])) * odds['K2']
    odds['D1X'], odds['DX2'], odds['D12'] = odds['K1'] + odds['KX'], odds['K2'] + odds['KX'], odds['K1'] + odds['K2']
    odds['DW1'] = odds['P1'] * odds['DP1']
    odds['DW2'] = odds['P2'] * odds['DP2']

    overs, overs_first = calc_over(final, n), calc_over(first, n_first)
    granica_ou, over = egal(overs, '+')
    gran_over = granica_ou
    alternative(odds, 3, granica_ou, overs, ('|+|', '|-|'))

    gran_ou_first, over_first = egal(overs_first, '+')
    odds['FH+'] = {'granica_ou':gran_ou_first, 'vrednost':overs_first[gran_ou_first]['+']}
    odds['FH-'] = {'granica_ou':gran_ou_first, 'vrednost':overs_first[gran_ou_first]['-']}
    
    overs_sec = calc_over(sec, n_sec)
    gran_ou_sec, over_sec = egal(overs_sec, '+')
    odds['SH+'] = {'granica_ou':gran_ou_sec, 'vrednost':overs_sec[gran_ou_sec]['+']}
    odds['SH-'] = {'granica_ou':gran_ou_sec, 'vrednost':overs_sec[gran_ou_sec]['-']}

    hends = calc_hend(final, n)
    gran_hend, hend = egal(hends, 'h1')
    alternative(odds, 3, gran_hend, hends, ('H1', 'H2'))
    odds['H2']['vrednost'] *= 1.075
    odds['H1']['vrednost'] = 1 - odds['H2']['vrednost']

    hends_first = calc_hend(first, n_first)
    gran_hend_first, hend_first = egal(hends_first, 'h1')
    odds['HP1'] = {'granica_hd':gran_hend_first, 'vrednost':hends_first[gran_hend_first]['h1']}
    odds['HP2'] = {'granica_hd':gran_hend_first, 'vrednost':hends_first[gran_hend_first]['h2']}

    hends_sec = calc_hend(sec, n_sec)
    gran_hend_sec, hend_sec = egal(hends_sec, 'h1')
    odds['HDP1'] = {'granica_hd':gran_hend_sec, 'vrednost':hends_sec[gran_hend_sec]['h1']}
    odds['HDP2'] = {'granica_hd':gran_hend_sec, 'vrednost':hends_sec[gran_hend_sec]['h2']}

    mat1 = np.fliplr(np.triu(np.fliplr(final), k=n - gran_over - 0.5))
    mat2 = np.tril(final, k=-1)
    odds['1&-'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou}

    mat2 = np.triu(final, k=1)
    odds['2&-'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou}

    mat1 = np.fliplr(np.tril(np.fliplr(final), k=n - gran_over - 1.5))
    mat2 = np.tril(final, k=-1)
    odds['1&+'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou}

    mat2 = np.triu(final, k=1)
    odds['2&+'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou}

    mat1 = np.fliplr(np.triu(np.fliplr(final), k=n - gran_over - 0.5))
    mat2 = np.triu(final, k=gran_hend + 0.5)
    
    odds['H2&-'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou, 'granica_hd': gran_hend}
    mat1 = np.fliplr(np.tril(np.fliplr(final), k=n - gran_over - 1.5))
    
    odds['H2&+'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou, 'granica_hd': gran_hend}
    mat1 = np.fliplr(np.tril(np.fliplr(final), k=n - gran_over - 1.5))
    mat2 = np.tril(final, k=gran_hend - 0.5)
    
    odds['H1&+'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou, 'granica_hd': gran_hend}
    odds['H1&-'] = {'vrednost': 1 - odds['H2&-']['vrednost'] - odds['H2&+']['vrednost'] - odds['H1&+']['vrednost'], 'granica_ou': granica_ou, 'granica_hd': gran_hend}
    
    gran1, vred1 = find_closest(lam1, final, 'prvi')
    gran2, vred2 = find_closest(lam2, final, 'drugi')
    to_add = {'1TM+': {'granica_ou': gran1, 'vrednost': vred1}, '1TM-': {'granica_ou': gran1, 'vrednost': 1 - vred1},
              '2TM+': {'granica_ou': gran2, 'vrednost': vred2}, '2TM-': {'granica_ou': gran2, 'vrednost': 1 - vred2}}
    odds.update(to_add)
    gran1_I, vred1_I = find_closest(lam1_first, first, 'prvi')
    gran2_I, vred2_I = find_closest(lam2_first, first, 'drugi')
    to_add = {'1TM+PP': {'granica_ou': gran1_I, 'vrednost': vred1_I}, '1TM-PP': {'granica_ou': gran1_I, 'vrednost': 1 - vred1_I},
              '2TM+PP': {'granica_ou': gran2_I, 'vrednost': vred2_I}, '2TM-PP': {'granica_ou': gran2_I, 'vrednost': 1 - vred2_I}}
    odds.update(to_add)

    gran1_II, vred1_II = find_closest(lam1_sec, sec, 'prvi')
    gran2_II, vred2_II = find_closest(lam2_sec, sec, 'drugi')
    to_add = {'1TM+DP': {'granica_ou': gran1_II, 'vrednost': vred1_II}, '1TM-DP': {'granica_ou': gran1_II, 'vrednost': 1 - vred1_II},
              '2TM+DP': {'granica_ou': gran2_II, 'vrednost': vred2_II}, '2TM-DP': {'granica_ou': gran2_II, 'vrednost': 1 - vred2_II}}
    odds.update(to_add)

    gran_oba, otp = both_teams(final)
    odds['OT|+|'] = {'vrednost': otp['over'], 'granica_ou': gran_oba}
    odds['OT|-|'] = {'vrednost': otp['under'], 'granica_ou': gran_oba}
    odds['EV'], odds['ODD'] = 0.5, 0.5
    
    gran_oba, otp = both_teams(first)
    odds['OT|+|PP'] = {'vrednost': otp['over'], 'granica_ou': gran_oba}
    odds['OT|-|PP'] = {'vrednost': otp['under'], 'granica_ou': gran_oba}

    gran_oba, otp = both_teams(sec)
    odds['OT|+|DP'] = {'vrednost': otp['over'], 'granica_ou': gran_oba}
    odds['OT|-|DP'] = {'vrednost': otp['under'], 'granica_ou': gran_oba}

    turned = np.fliplr(first)
    turned_sec = np.fliplr(sec)

    odds['I=II'], odds['I>II'] = 0, 0
    for i in range(-turned.shape[0], turned.shape[0]):
        odds['I>II'] += np.sum(np.diag(turned, i)) * np.sum(np.triu(turned_sec, i + 1))
        odds['I=II'] += np.sum(np.diag(turned, i)) * np.sum(np.diag(turned_sec, i))
    odds['I<II'] = 1 - odds['I=II'] - odds['I>II']

    odds.update(odds_prelazi)
    odds_correction(odds, final)
    if odds['2&+']['vrednost'] < 0:
        odds['2&+']['vrednost'] = 1e-7
    if odds['2&-']['vrednost'] < 0:
        odds['2&-']['vrednost'] = 1e-7
    odds['1-1&+'] = {'vrednost': odds['1-1']*over['+'], 'granica_ou':gran_over}
    odds['1-1&-'] = {'vrednost': odds['1-1']*(1 - over['+']), 'granica_ou':gran_over}
    odds['1-2&+'] = {'vrednost': odds['1-2']*over['+'], 'granica_ou':gran_over}
    odds['1-2&-'] = {'vrednost': odds['1-2']*(1 - over['+']), 'granica_ou':gran_over}
    odds['2-1&+'] = {'vrednost': odds['2-1']*over['+'], 'granica_ou':gran_over}
    odds['2-1&-'] = {'vrednost': odds['2-1']*(1 - over['+']), 'granica_ou':gran_over}
    odds['2-2&+'] = {'vrednost': odds['2-2']*over['+'], 'granica_ou':gran_over}
    odds['2-2&-'] = {'vrednost': odds['2-2']*(1 - over['+']), 'granica_ou':gran_over}

    if reverse:
        odds = invert(odds)

    if not real_probs:
        odds = real_time_obaranje(odds, margin=margin)
    
    return odds


def invert(odds):
    for key in odds:
        if key in mapping.keys():
            odds[mapping[key]], odds[key] = odds[key], odds[mapping[key]]
    return odds


if __name__ == '__main__':
    # primer poziva sa hendikepom -4.5 (domacin favorit)
    odds = real_time_calculation(52.5, -4.5, model=1, margin=0.075, real_probs=True)
    print(odds['K1'], odds['KX'], odds['K2'])
    print(odds['P1'], odds['PX'], odds['P2'])
    print(odds['DP1'], odds['DPX'], odds['DP2'])
    print(odds['1-1'], odds['2-2'])
    # primer poziva sa hendikepom 4.5 (gost favorit)
    odds = real_time_calculation(52.5, 4.5, model=1, margin=0.075, real_probs=True)
    

    