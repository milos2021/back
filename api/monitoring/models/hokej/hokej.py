import os
import math
import numpy as np
from scipy.special import factorial
import operator as op
from scipy.stats import nbinom
import scipy
from map import base_to_code, mapping

def poisson(lam, k):
    return pow(lam, k) * math.exp(-lam) / math.factorial(k)


def create_matrix(lam1, lam2, num):
    lam1 = np.full([num, ], lam1)
    lam2 = np.full([num, ], lam2)
    y = np.arange(0, num, 1)
    y_h = np.arange(0, num / 2, 0.5)
    power1 = np.power(lam1, y_h)
    expon1 = np.exp(-lam1)
    faktor = factorial(y)
    power2 = np.power(lam2, y_h)
    expon2 = np.exp(-lam2)
    poisson1 = expon1 / faktor
    poisson1 = power1 * poisson1 * power1
    poisson2 = expon2 / faktor
    poisson2 = power2 * poisson2 * power2
    final = np.outer(poisson1, poisson2)
    return final

def create_matrix_full(lam1, lam2, num):
    lam1 = np.full([num, ], lam1)
    lam2 = np.full([num, ], lam2)
    y = np.arange(0, num, 1)

    power1 = np.power(lam1, y)
    power2 = np.power(lam2, y)
    faktor = factorial(y)

    poisson1 = np.exp(-lam1) * power1 / faktor
    poisson2 = np.exp(-lam2) * power2 / faktor

    final = np.outer(poisson1, poisson2)

    return final


def calc_hend(final):
    hends = {}

    for i in range(5):
        gran1 = i + 0.5
        gran2 = -i + 0.5
        h2_1 = np.sum(np.triu(final, k=-i))
        h2_2 = np.sum(np.triu(final, k=i))
        hends[-gran1] = {'h1': 1 - h2_1, 'h2': h2_1}
        hends[-gran2] = {'h1': 1 - h2_2, 'h2': h2_2}

    return hends


def nck(n, r):
    r = min(r, n-r)
    if r == 0:
        return 1
    numer = reduce(op.mul, xrange(n, n - r, -1))
    denom = reduce(op.mul, xrange(1, r + 1))
    return numer//denom


def to_real_3(k1, kx, k2):
    k1, k2, kx = float(k1), float(k2), float(kx)
    p1 = 1 / k1 - (1 / k1 + 1 / k2 + 1 / kx - 1) / 3
    p2 = 1 / k2 - (1 / k1 + 1 / k2 + 1 / kx - 1) / 3
    px = 1 / kx - (1 / k1 + 1 / k2 + 1 / kx - 1) / 3
    return p1, px, p2


def get_exps(gran_ou, hend):
    gran_ou, hend = float(gran_ou), float(hend)
    lam1 = gran_ou / 2 + hend / 2
    lam2 = gran_ou / 2 - hend / 2
    return lam1, lam2


def to_real_2(k1, k2):
    k1, k2 = float(k1), float(k2)
    p1 = 1 / k1 - (1 / k1 + 1 / k2 - 1) / 2
    p2 = 1 / k2 - (1 / k1 + 1 / k2 - 1) / 2
    return p1, p2


def get_exps_with_odds(over, under, gran_ou, k1, kX, k2, gran_hd):
    # h1_real, h2_real = to_real_2(h1, h2)
    x = kX * gran_ou
    lam1 = k1 * gran_ou
    lam2 = k2 * gran_ou + x

    # lam1, lam2 = get_exps(temp_gran_ou, gran)
    print (lam1, lam2, x)
    return lam1, lam2


def egal(odds, k='h1'):
    diff = 1
    gran = 0
    for key in odds:
        razlika = abs(odds[key][k] - 0.5)
        if razlika < diff:
            diff = razlika
            gran = key
    return gran, odds[gran]


def calc_over(final, n, rng=10):
    overs = {}
    for i in range(rng):
        gran1 = n + i - 0.5 # povedi racuna
        gran2 = n - i - 0.5
        under1 = np.sum(np.triu(np.fliplr(final), k=-i))
        under2 = np.sum(np.triu(np.fliplr(final), k=i))
        overs[gran1] = {'+': 1 - under1, '-': under1}   
        overs[gran2] = {'+': 1 - under2, '-': under2}
    overs_fin = {key: overs[key] for key in overs if key > 0 and key < 12}
    return overs_fin


def create1x2(mat):
    k2 = np.triu(mat, k=1)
    k1 = np.tril(mat, k=-1)
    tmp1 = np.sum(k1)
    tmp2 = np.sum(k2)
    tmpX = 1 - tmp1 - tmp2
    return tmp1, tmpX, tmp2

def calc_goal_combs(overs, odds, limit=8, mode='full'):
    limits = {}
    for i in range(limit):
        for j in range(i + 1, limit + 1):
            if mode == 'full':
                key = 'G' + str(i) + '-' + str(j)
            elif mode == 'first':
                key = 'I' + str(i) + str(j)
            if i != 0:
                limits[key] = overs[j + 0.5]['-'] - overs[i - 0.5]['-']
            else:
                limits[key] = overs[j + 0.5]['-']
    for key in overs:
        if mode == 'full':
            new_key = 'G' + str(int(math.ceil(key))) + '+'
        elif mode =='first':
            new_key = 'I' + str(int(math.ceil(key))) + '+'
        odds[new_key] = overs[key]['+']
    odds.update(limits)


def both_teams(mat, odds, limit=3, prefix=''):
    tm1_tm2 = {}
    pre = ''
    for i in range(0, limit):
        over = np.sum(mat[(i + 1):, (i + 1):])
        if i > 0:
            pre = str(i + 1)
        tm1_tm2[prefix + pre + 'GG'] = over
        tm1_tm2[prefix + pre + 'NG'] = 1 - over
    odds.update(tm1_tm2)

    tm1_tm2['GG'], tm1_tm2['GG2+'] = np.sum(mat[1:, 1:]), np.sum(mat[2:, 2:])
    tm1_tm2['NG'], tm1_tm2['nGG2+'] = 1 - tm1_tm2['GG'], 1 - tm1_tm2['GG2+']


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


def goals_one_team(mat, mat_first, odds):
    odds['HS2'], odds['GH01'], odds['1TM02'] = np.sum(mat[0, :]), np.sum(mat[:2, :]), np.sum(mat[:3, :])
    odds['1TM03'], odds['HS1'], odds['GH2+'] = np.sum(mat[0:4, :]), np.sum(mat[1:, :]), np.sum(mat[2:, :])
    odds['GH3+'], odds['1TM4+'], odds['1TM12'] = np.sum(mat[3:, :]), np.sum(mat[4:, :]), np.sum(mat[1:3, :])
    odds['1TM13'], odds['GH23'], odds['GH24'] = np.sum(mat[1:4, :]), np.sum(mat[2:4, :]), np.sum(mat[2:5, :])
    odds['GH34'] = np.sum(mat[3:5, :])

    odds['AS2'], odds['GA01'], odds['2TM02'] = np.sum(mat[:, 0]), np.sum(mat[:, :2]), np.sum(mat[:, :3])
    odds['2TM03'], odds['AS1'], odds['GA2+'] = np.sum(mat[:, :4]), np.sum(mat[:, 1:]), np.sum(mat[:, 2:])
    odds['GA3+'], odds['2TM4+'], odds['2TM12'] = np.sum(mat[:, 3:]), np.sum(mat[:, 4:]), np.sum(mat[:, 1:3])
    odds['2TM13'], odds['GA23'], odds['GA24'] = np.sum(mat[:, 1:4]), np.sum(mat[:, 2:4]), np.sum(mat[:, 2:5])
    odds['GA34'] = np.sum(mat[:, 3:5])

    odds['GHP0'], odds['GHP01'], odds['GHP02'] = np.sum(mat_first[0, :]), np.sum(mat_first[:2, :]), np.sum(mat_first[:3, :])
    odds['GHP1+'], odds['GHP2+'], odds['GHP3+'] = np.sum(mat_first[1:, :]), np.sum(mat_first[2:, :]), np.sum(mat_first[3:, :])
    odds['GHP12'], odds['GHP23'] = np.sum(mat_first[1:3, :]), np.sum(mat_first[2:4, :])

    odds['GAP0'], odds['GAP01'], odds['GAP02'] = np.sum(mat_first[:, 0]), np.sum(mat_first[:, :2]), np.sum(mat_first[:, :3])
    odds['GAP1+'], odds['GAP2+'], odds['GAP3+'] = np.sum(mat_first[:, 1:]), np.sum(mat_first[:, 2:]), np.sum(mat_first[:, 3:])
    odds['GAP12'], odds['GAP23'] = np.sum(mat_first[:, 1:3]), np.sum(mat_first[:, 2:4])



def calc_game(mat1, mat2):
    mask = np.multiply(mat1, mat2)
    mask[mask > 0] = 1
    return np.sum(np.multiply(mat1, mask))


def combinations(mat, odds, n):
    grans = [2.5, 3.5, 4.5, 5.5, 6.5]
    combs = {}
    for gran_over in grans:
        mat1 = np.fliplr(np.triu(np.fliplr(mat), k=n - gran_over - 0.5))
        mat2 = np.tril(mat, k=-1)

        k1_min = calc_game(mat1, mat2)
        mat2 = np.triu(mat, k=1)
        k2_min = calc_game(mat1, mat2)

        mat1 = np.fliplr(np.tril(np.fliplr(mat), k=n - gran_over - 1.5))
        mat2 = np.tril(mat, k=-1)
        k1_plus = calc_game(mat1, mat2)

        mat2 = np.triu(mat, k=1)
        k2_plus = calc_game(mat1, mat2)

        combs[gran_over] = {'1&+': k1_plus, '1&-': k1_min, '2&+': k2_plus, '2&-': k2_min}

    odds['1&G0-3'], odds['2&G0-3'] = combs[3.5]['1&-'], combs[3.5]['2&-']
    odds['1&G0-4'], odds['2&G0-4'] = combs[4.5]['1&-'], combs[4.5]['2&-']
    odds['1&G0-5'], odds['2&G0-5'] = combs[5.5]['1&-'], combs[5.5]['2&-']
    odds['1&3+'], odds['2&3+'] = combs[2.5]['1&+'], combs[2.5]['2&+']
    odds['1&4+'], odds['2&4+'] = combs[3.5]['1&+'], combs[3.5]['2&+']       
    odds['1&5+'], odds['2&5+'] = combs[4.5]['1&+'], combs[4.5]['2&+']
    odds['1&6+'], odds['2&6+'] = combs[5.5]['1&+'], combs[5.5]['2&+']

def prelazi_combs(odds, first, rest):
    odds.update({'1-1&3+': 0, '1-1&G03': 0, '1-1&4+': 0, '1-1&5+': 0,
                 '1-1&GG': 0, '1-1&I2+': 0, '1-1&IGG': 0,'1-1&D3+': 0,
                 '2-2&3+': 0, '2-2&G03': 0, '2-2&4+': 0, '2-2&5+': 0,
                 '2-2&GG': 0, '2-2&I2+': 0, '2-2&IGG': 0, '1-1&I0-1': 0, 
                 '2-2&I0-1': 0, '2-2&G3+': 0, '1&I0-1': 0, '1&I2+': 0, 
                 '2&I0-1': 0, '2&I2+': 0, '1&IGG': 0, '2&IGG': 0, '1&D3+': 0, 
                 '2&G3+': 0, '1&I1+': 0, '2&I1+': 0, '1-1&G04': 0, '1-1&G05': 0,
                 '2-2&G04': 0, '2-2&G05': 0, '1-1&6+': 0, '2-2&6+': 0})
    goals = [3, 4, 5, 6]
    for i in range(first.shape[0]):
        for j in range(first.shape[1]):
            for k in range(rest.shape[0]):
                for m in range(rest.shape[1]):
                    faktor = first[i, j] * rest[k, m]
                    num_goals = i + j + k + m
                    prefix, prefix_full = None, None
                    if (i + k) > (j + m):
                        prefix_full = '1'
                        if i > j:
                            prefix = '1-1'
                    elif (i + k) < (j + m):
                        prefix_full = '2'
                        if i < j:
                            prefix = '2-2'
                    if prefix_full:
                        keys = []
                        if prefix:
                            for gran in goals:
                                if num_goals >= gran:
                                    keys.append(prefix + '&' + str(gran) + '+')
                            if num_goals <= 3:
                                keys.append(prefix + '&G03')
                            if num_goals <= 4:
                                keys.append(prefix + '&G04')
                            if num_goals <= 5:
                                keys.append(prefix + '&G05')
                            if k > 0 and m > 0:
                                keys.append(prefix + '&GG')
                            keys.append(prefix + '&I2+' if i + j >= 2 else prefix + '&I0-1')
                        if i > 0 and j > 0:
                            keys.append(prefix_full + '&IGG')
                            if prefix:
                                keys.append(prefix + '&IGG')

                        keys.append(prefix_full + '&I2+' if i + j >= 2 else prefix_full + '&I0-1')
                        
                        if prefix == '1-1' and i + k >= 3:
                            keys.append('1-1&D3+')
                        if prefix == '2-2' and j + m >= 3:
                            keys.append('2-2&G3+')
                        if prefix_full == '1' and i + k >=3:
                            keys.append(prefix_full + '&D3+')
                        if prefix_full == '2' and j + m >= 3:
                            keys.append(prefix_full + '&G3+')
                        if i + j >= 1:
                            keys.append(prefix_full + '&I1+')
                        for key in keys:
                            odds[key] += faktor


def calculate_odds_different(p, m=0.075, n=2):
    if p > 0:
        pz = 1 / math.exp(-math.log(n * (1 - m)) * math.log(1 / p) / math.log(n))
    else:
        pz = 0
    return pz



def fixing_kvotas(odds, mat, perc, rem_kvota, add_kvota, prefix='K'):
    '''
    dodavanje razlika na matricu mat
    procenat koji se skida sa rem_kvota i dodaje na add_kvota u matricu mat
    vraca prepravljenu matricu
    '''
    rem_kvota = prefix + rem_kvota
    n = len(mat[0])
    change = perc*odds[rem_kvota]
    change_for_12 = change / ((n**2 - n) / 2)
    change_for_x = change / n
    
    if rem_kvota == prefix + '1':
        mask_for_k1 = np.tril(np.full((n,n), change_for_12), -1)
        mat = mat - mask_for_k1
    elif rem_kvota == prefix + 'X':
        mask_for_kx = np.diag(np.diag(np.full((n, n), change_for_x)))
        mat = mat - mask_for_kx
    else:
        mask_for_k2 = np.triu(np.full((n,n), change_for_12), 1)
        mat = mat - mask_for_k2


    for fiks in add_kvota:
        if prefix + fiks == prefix + '1':
            mask_for_k1 = np.tril(np.full((n,n), change_for_12/len(add_kvota)), -1)
            mat = mat + mask_for_k1
        elif prefix + fiks == prefix + 'X':
            mask_for_kx = np.diag(np.diag(np.full((n, n), change_for_x/len(add_kvota))))
            mat = mat + mask_for_kx
        else:
            mask_for_k2 = np.triu(np.full((n,n), change_for_12/len(add_kvota)), 1)
            mat = mat + mask_for_k2
    return mat


def fixing_kvotas_perc(odds, mat, perc, rem_kvota, add_kvota, prefix='K'):
    '''
    dodavanje razlika na matricu mat
    procenat koji se skida sa rem_kvota i dodaje na add_kvota u matricu mat
    vraca prepravljenu matricu
    '''

    rem_kvota = prefix + rem_kvota
    change = perc*odds[rem_kvota]
    # change_for_12 = change / ((n**2 - n) / 2)
    # change_for_x = change / n
    
    if rem_kvota == prefix + '1':
        mask_for_k1 = np.tril(mat, -1) * perc
        mat = mat - mask_for_k1
    elif rem_kvota == prefix + 'X':
        mask_for_kx = np.diag(np.diag(mat)) * perc
        mat = mat - mask_for_kx
    else:
        mask_for_k2 = np.triu(mat, 1) * perc
        mat = mat - mask_for_k2

    for fiks in add_kvota:

        change = change if len(add_kvota) == 1 else change / 2

        if prefix + fiks == prefix + '1':
            perc_for_1 = change / np.sum(np.tril(mat, - 1))
            mask_for_k1 = np.tril(mat, -1) * (1 + perc_for_1)
            mat = np.triu(mat) + mask_for_k1
        elif prefix + fiks == prefix + 'X':
            perc_for_x = change / np.sum(np.diag(mat))
            mask_for_kx = np.diag(np.diag(mat)) * (1 + perc_for_x)
            mat = np.triu(mat, 1) + np.tril(mat, -1) + mask_for_kx
        else:
            perc_for_2 = change / np.sum(np.triu(mat, 1))
            mask_for_k2 = np.triu(mat, 1) * (1 + perc_for_2)
            mat = np.tril(mat) + mask_for_k2
    return mat


def real_time_calculation(gran, hend, gran_first=None, hend_first=None, model=2):
    reverse = False
    if hend > 0:
        reverse = True
    
    hend = abs(hend)

    gran, hend = float(gran) + 0.17, float(hend)


    model_mapping = {1: 8, 2: 10, 3: 12, 4: 14, 5: 16}
    n = model_mapping[model]
    lam1, lam2 = get_exps(gran, hend)
    n_first = n / 2

    if hend_first:
        hend_first = abs(hend_first)

    if gran_first and hend_first:
        lam1_first, lam2_first = get_exps(gran_first, hend_first)
    else:
        lam1_first, lam2_first = 0.296 * lam1, 0.296 * lam2
    lam1_rest, lam2_rest = lam1 - lam1_first, lam2 - lam2_first

    n_first_pois = n_first if not n_first % 2 else (n_first + 1)
    n_first_pois = int(n_first_pois)
    final = create_matrix(lam1, lam2, n)
    first = create_matrix(lam1_first, lam2_first, n_first_pois)
    rest = create_matrix(lam1_rest, lam2_rest, n)
    
    razlika = (1 - np.sum(final)) / (n / 2.0)
    mask_mask = np.array(int(n / 2) * [0] + int(n / 2) * [1])
    mask = np.diag(np.diag(np.full((n, n), razlika)) * mask_mask)
    final = final + mask
    odds = {}
    odds['K1'], odds['KX'], odds['K2'] = create1x2(final)

    if not (hend >= 0 and hend <= 0.1):
        if odds['K1'] < 0.6 :
            final_fixed = fixing_kvotas_perc(odds, final, 0.085, '2', ['X'])
        elif odds['K1'] < 0.78 and odds['K1'] >= 0.6:
            final_fixed = fixing_kvotas_perc(odds, final, 0.035, '1', ['X', '2'])
            final_fixed = final
        elif odds['K1'] < 0.78 and odds['K1'] >= 0.7:
            final_fixed = fixing_kvotas_perc(odds, final, 0.035, '1', ['X', '2'])
        elif odds['K1'] >= 0.78 and odds['K1'] < 0.85:
            final_fixed = fixing_kvotas_perc(odds, final, 0.17, 'X', ['1'])
            final_fixed = fixing_kvotas_perc(odds, final_fixed, 0.13, '2', ['1'])
        elif odds['K1'] >= 0.85:
            final_fixed = fixing_kvotas_perc(odds, final, 0.45, 'X', ['1'])
            final_fixed = fixing_kvotas_perc(odds, final_fixed, 0.35, '2', ['1'])
        if model == 4:
            final_fixed = fixing_kvotas_perc(odds, final_fixed, 0.08, '2', ['X'])
        if model == 5:
            final_fixed = final
    else:
        final_fixed = fixing_kvotas_perc(odds, final, 0.04, '2', ['X'])
        final_fixed = fixing_kvotas_perc(odds, final_fixed, 0.04, '1', ['X'])
    

    final = final_fixed
    odds['K1'], odds['KX'], odds['K2'] = create1x2(final)

    odds['P1'], odds['PX'], odds['P2'] = create1x2(first)
    odds['D1X'], odds['DX2'], odds['D12'] = odds['K1'] + odds['KX'], odds['K2'] + odds['KX'], odds['K1'] + odds['K2']
    odds['DI1X'], odds['DIX2'], odds['DI12'] = odds['P1'] + odds['PX'], odds['P2'] + odds['PX'], odds['P1'] + odds['P2']
    rest1, restx, rest2 = create1x2(rest)   
    odds['SW1'], odds['SW2'] = np.sum(final[1:, 0]), np.sum(final[0, 1:])
    #odds['DW1'], odds['DW2'] = odds['P1'] * rest1, odds['P2'] * rest2
    odds['W1'], odds['W2'] = (1 / (1 - odds['KX'])) * odds['K1'], (1 / (1 - odds['KX'])) * odds['K2']

    overs = calc_over(final, n, rng=18)
    overs_first = calc_over(first, n_first_pois, rng=18)
    
    calc_goal_combs(overs, odds, limit=9)
    calc_goal_combs(overs_first, odds, limit=4, mode='first')

    odds['GG'], odds['GG2+'], odds['GG3+'] = np.sum(final[1:, 1:]), np.sum(final[2:, 2:]), np.sum(final[3:, 3:])
    odds['GN'], odds['nGG2+'] = np.sum(final[1:, 0]) + np.sum(final[0, 1:]) + final[0, 0], 1 - odds['GG2+']
    odds['GG1'], odds['GN1'] = np.sum(first[1:, 1:]), 1 - np.sum(first[1:, 1:])
    odds['GG&3+'], odds['GG&4+'] = odds['GG'] - final[1, 1], odds['GG'] - final[1, 1] - final[1, 2] - final[2, 1]
    odds['nGG3+'] = 1 - odds['GG3+']
    odds['GG&5+'] = odds['GG&4+'] - final[3, 1] - final[1, 3] - final[2, 2]
    odds['GG&6+'] = odds['GG&5+'] - final[4, 1] - final[1, 4] - final[3, 2] - final[2, 3]
    odds['2GG&5+'] = odds['GG2+'] - final[2, 2]
    odds['2GG&6+'] = odds['2GG&5+'] - final[3, 2] - final[2, 3]
    odds['1&GG'], _, odds['2&GG'] = create1x2(final[1:, 1:])
    odds['I0'] = first[0, 0]
    hends = calc_hend(final)

    odds['2HW1'], odds['2HW2'] = hends[-1.5]['h1'], hends[1.5]['h2']
    odds['3HW1'], odds['3HW2'] = hends[-2.5]['h1'], hends[2.5]['h2']
    
    goals_one_team(final, first, odds)
    prelazi(first, rest, odds, n)
    combinations(final, odds, n)
    prelazi_combs(odds, first, rest)

    odds_new = {base_to_code[key] : odds[key] for key in odds if key in base_to_code.keys()}

    if reverse:
        odds_new = invert(odds_new)

    return odds_new

def egal_kvota(odds):
    dif = 1000
    gran, over, under = 0, 0, 0
    for key in odds:
        if 'over' in key:
            if abs(1.85 - odds[key]['vrednost']) < dif:
                dif = abs(1.85 - odds[key]['vrednost'])
                gran = odds[key]['granica_ou']
    if gran != 0:
        return gran, odds['over_' + str(gran)]['vrednost'], odds['under_' + str(gran)]['vrednost']
    else:
        return 0, 0, 0


def calculate_exp(g1, g2, k1, k2, k3, k4):
    p1_real, p2_real = to_real_2(k1, k2)
    p3_real, p4_real = to_real_2(k3, k4)
    k1_real, k2_real, k3_real, k4_real = 1 / p1_real, 1 / p2_real, 1 / p3_real, 1 / p4_real
    x, y = abs((2 / k1_real) - 1), abs((2 / k3_real) - 1)
    z = g2 - g1
    g = (x / (x + y)) * z + g1

    return g


def calculate_all(h11, h12, gh1, h21, h22, gh2, o1, u1, g1, o2, u2, g2):
    hend = calculate_exp(gh1, gh2, h11, h12, h21, h22)
    ou = calculate_exp(g1, g2, o1, u1, o2, u2)
    lam1, lam2 = get_exps(ou, hend)
    # print lam1, lam2
    # print lam1 + lam2
    # print lam1 - lam2
    final = create_matrix_bin(lam1, lam2, int(round(lam1 + lam2)))
    odds = {}
    k2 = np.triu(final, k=1)
    k1 = np.tril(final, k=-1)
    odds['KI 1'] = np.sum(k1)
    odds['KI 2'] = np.sum(k2)
    odds['KI X'] = 1 - odds['KI 1'] - odds['KI 2']
    print (1 / odds['KI 1'], 1 / odds['KI X'], 1 / odds['KI 2'])


def update_sums(odds, mec, sume, gran_egal):
    domacin = mec.prva_trecina_domacin + mec.druga_trecina_daomcin + mec.treca_trecina_daomcin
    gost = mec.prva_trecina_gost + mec.druga_trecina_gost + mec.treca_trecina_gost

    if domacin > gost:
        sume['KI 1'] = sume['KI 1'] + 1 / odds['KI 1']
    elif gost > domacin:
        sume['KI 2'] = sume['KI 2'] + 1 / odds['KI 2']
    else:
        sume['KI X'] = sume['KI X'] + 1 / odds['KI X']

    ukupno_poena = domacin + gost
    granice = {'-1': gran_egal - 1, '': gran_egal, '+1': gran_egal + 1}
    for key in granice:
        if ukupno_poena > granice[key]:
            sume['over' + key] += 1 / odds['o/u'][granice[key]]['+']
        else:
            sume['under' + key] += 1 / odds['o/u'][granice[key]]['-']

def invert(odds):
    for key in odds:
        if key in mapping.keys():
            odds[mapping[key]], odds[key] = odds[key], odds[mapping[key]]
    return odds

if __name__ == '__main__':
    kvote = real_time_calculation(7.7, 4, model=4)  
    for key in kvote:
        print(key, kvote[key])