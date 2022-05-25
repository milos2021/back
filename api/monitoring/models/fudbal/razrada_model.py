# coding=utf-8
import os
import sys
import time
import numpy as np
import operator as op
from scipy.stats import poisson
import django
import math
import pickle
from scipy.optimize import fsolve, brentq, broyden2, newton_krylov, anderson
from scipy.stats import skellam
from functools import reduce
sys.path.append(os.path.dirname(os.path.realpath(__file__)).rsplit(os.path.sep, 3)[0])
from monitoring.models.fudbal.map import mapping, base_to_code
dir_path = os.path.dirname(os.path.realpath(__file__)) 
# obrada_dict = pickle.load(open(os.path.join(dir_path, 'obrada_dict3_6.pickle'), 'rb'))
with open(os.path.join(dir_path, 'obrada_dict3_6.pickle'),'rb') as handle:
    obrada_dict=pickle.load(handle)

'''
Ova skripta sluzi za racunanje celokupne ponude u fudbalu. Jedina funkcija koja je vama bitna je real_time_calculation (objasnjenja imate u funkciji).
Ostale sluze samo kako bi ih ona pozivala. U prilogu dobijate i  pickle file neophodan za racunicu (ovo cemo mozda promeniti). Dodato je okretanje igara. 
Koristi se python 3.6.
'''

def nck(n, r):
    r = min(r, n - r)
    if r == 0:
        return 1
    numer = reduce(op.mul, range(n, n - r, -1))
    denom = reduce(op.mul, range(1, r + 1))
    return numer // denom


def create_matrix_pois(lam1, lam2, num):
    x = np.arange(0, num, 1)
    y = np.arange(0, num, 1)
    poisson1 = poisson.pmf(x, lam1, loc=0)
    poisson2 = poisson.pmf(y, lam2, loc=0)
    final = np.outer(poisson1, poisson2)
    return final


def bivariate_poisson(x, y, lam1, lam2, cov=0):
    ceil = min(x, y)
    lam1, lam2 = lam1 - cov, lam2 - cov
    con = math.exp(-(lam1 + lam2 + cov)) * (lam1 ** x) * (lam2 ** y) / (math.factorial(x) * math.factorial(y))
    prob = 0
    for k in range(ceil + 1):
        prob += con * nck(x, k) * nck(y, k) * math.factorial(k) * (cov / (lam1 * lam2)) ** k
    return prob


def create1x2(mat):
    k2 = np.triu(mat, k=1)
    k1 = np.tril(mat, k=-1)
    tmp1 = np.sum(k1)
    tmp2 = np.sum(k2)
    tmpX = 1 - tmp1 - tmp2
    return tmp1, tmpX, tmp2


def obaranje_fudbal(odds, margin_name='1'):
    # to do
    return odds


def goals_one_team(odds, final, final_first, final_last):
    odds['HS2'], odds['GH01'], odds['1TM02'] = np.sum(final[0, :]), np.sum(final[:2, :]), np.sum(final[:3, :])
    odds['1TM03'], odds['HS1'], odds['GH2+'] = np.sum(final[:4, :]), np.sum(final[1:, :]), np.sum(final[2:, :])
    odds['GH3+'], odds['1TM4+'], odds['1TM12'] = np.sum(final[3:, :]), np.sum(final[4:, :]), np.sum(final[1:3, :])
    odds['1TM13'] = np.sum(final[1:4, :])
    odds['1TM01&02'] = np.sum(final_first[:2, :]) * np.sum(final_last[:3, :])
    odds['1TM02&02'] = np.sum(final_first[:3, :]) * np.sum(final_last[:3, :])
    odds['1TM02&01'] = np.sum(final_first[:3, :]) * np.sum(final_last[:2, :])

    odds['2TM01&02'] = np.sum(final_first[:, :2]) * np.sum(final_last[:, :3])
    odds['2TM02&02'] = np.sum(final_first[:, :3]) * np.sum(final_last[:, :3])
    odds['2TM02&01'] = np.sum(final_first[:, :3]) * np.sum(final_last[:, :2])

    odds['AS2'], odds['GA01'], odds['2TM02'] = np.sum(final[:, 0]), np.sum(final[:, :2]), np.sum(final[:, :3])
    odds['2TM03'], odds['AS1'], odds['GA2+'] = np.sum(final[:, :4]), np.sum(final[:, 1:]), np.sum(final[:, 2:])
    odds['GA3+'], odds['2TM4+'], odds['2TM12'] = np.sum(final[:, 3:]), np.sum(final[:, 4:]), np.sum(final[:, 1:3])
    odds['2TM13'], odds['GA23'] = np.sum(final[:, 1:4]), np.sum(final[:, 2:4])

    odds['GHP0'], odds['GHP01'] = np.sum(final_first[0, :]), np.sum(final_first[:2, :])
    odds['GHP1+'], odds['GHP2+'], odds['GHP3+'] = np.sum(final_first[1:, :]), np.sum(final_first[2:, :]), np.sum(
        final_first[3:, :])
    odds['GHD1+'] = np.sum(final_last[1:, :])
    odds['GHD0'], odds['GHD1'] = np.sum(final_last[0, :]), np.sum(final_last[1, :])
    odds['GAD0'], odds['GAD1'] = np.sum(final_last[:, 0]), np.sum(final_last[:, 1])
    odds['GHD01'], odds['GAD01'] = np.sum(final_last[:2, :]), np.sum(final_last[:, :2])
    odds['GHD12'], odds['GAD12'] = np.sum(final_last[1:3, :]), np.sum(final_last[:, 1:3])
    odds['DS1'] = odds['GHP1+'] * odds['GHD1+']

    odds['GHP12'] = np.sum(final_first[1:3, :])
    odds['GHP1'], odds['GAP1'] = np.sum(final_first[1, :]), np.sum(final_first[:, 1])
    odds['GH23'], odds['GA23'] = np.sum(final[2:4, :]), np.sum(final[:, 2:4])

    odds['GAP0'], odds['GAP01'] = np.sum(final_first[:, 0]), np.sum(final_first[:, :2])
    odds['GAP1+'], odds['GAP2+'], odds['GAP3+'] = np.sum(final_first[:, 1:]), np.sum(final_first[:, 2:]), np.sum(
        final_first[:, 3:])
    odds['GAD1+'] = np.sum(final_last[:, 1:])
    odds['GHD2+'], odds['GAD2+'] = np.sum(final_last[2:, :]), np.sum(final_last[:, 2:])
    odds['GHD3+'], odds['GAD3+'] = np.sum(final_last[3:, :]), np.sum(final_last[:, 3:])
    odds['GAP12'] = np.sum(final_first[:, 1:3])
    odds['DS2'] = odds['GAP1+'] * odds['GAD1+']
    odds['GH2-4'] = np.sum(final[2:5, :])
    odds['GA2-4'] = np.sum(final[:, 2:5])


def goals_match(odds, final, final_first, final_last):
    odds['G1'] = final[0, 1] + final[1, 0]
    odds['G2'] = final[0, 2] + final[2, 0] + final[1, 1]
    odds['G3'] = final[0, 3] + final[3, 0] + final[2, 1] + final[1, 2]
    odds['G4'] = final[4, 0] + final[3, 1] + final[2, 2] + final[1, 3] + final[0, 4]
    odds['G5'] = final[5, 0] + final[4, 1] + final[3, 2] + final[2, 3] + final[1, 4] + final[0, 5]

    odds['I0'] = final_first[0, 0]
    odds['I1'] = final_first[0, 1] + final_first[1, 0]
    odds['I2'] = final_first[0, 2] + final_first[2, 0] + final_first[1, 1]
    odds['I3'] = final_first[0, 3] + final_first[3, 0] + final_first[2, 1] + final_first[1, 2]
    odds['I1-2'] = final_first[1, 0] + final_first[0, 1] + final_first[1, 1] + final_first[2, 0] + final_first[0, 2]

    odds['II0'] = final_last[0, 0]
    odds['II1'] = final_last[0, 1] + final_last[1, 0]
    odds['II2'] = final_last[0, 2] + final_last[2, 0] + final_last[1, 1]
    odds['II3'] = final_last[0, 3] + final_last[3, 0] + final_last[2, 1] + final_last[1, 2]
    odds['II1-2'] = final_last[1, 0] + final_last[0, 1] + final_last[1, 1] + final_last[2, 0] + final_last[0, 2]


def correct_score(odds, final, mode='full'):
    n, prefix = 5, 'T'
    if mode == 'first':
        n, prefix = 4, 'P'
    for i in range(n):
        for j in range(n):
            key = prefix + str(i) + ':' + str(j)
            odds[key] = final[i, j]


def first_second_half_goal_combs(odds, overs_f, overs_s):
    for i in range(1, 3):
        for j in range(1, 4):
            key = 'I' + str(i) + '+' + '&II' + str(j) + '+'
            prob = overs_f[i - 0.5]['+'] * overs_s[j - 0.5]['+']
            odds.update({key: prob})
            key = 'I0' + str(i) + '&II0' + str(j)
            prob = overs_f[i + 0.5]['-'] * overs_s[j + 0.5]['-']
            odds.update({key: prob})
    to_update = {'I1-2&II1-2': (overs_f[2.5]['-'] - overs_f[0.5]['-']) * (overs_s[2.5]['-'] - overs_s[0.5]['-']),
                 'I1-3&II1-3': (overs_f[3.5]['-'] - overs_f[0.5]['-']) * (overs_s[3.5]['-'] - overs_s[0.5]['-'])}
    odds.update(to_update)


def double_chance_goal_combs_full(odds, final):
    odds.update({'D12&G23': 0, 'D12&G2+': 0, 'D1X&G23': 0, 'DX2&GG': 0, 'D1X&G4-6': 0, 'D1X&G3-6': 0,
                 'D1X&G0-3': 0, 'D1X&G0-2': 0, 'D1X&4+': 0, 'D1X&G2-6': 0, 'D1X&G2-5': 0, 'D1X&G2-4': 0, 'DX2&G4-6': 0,
                 'D12&G2-5': 0, 'DX2&G0-2': 0, 'DX2&G0-3': 0, 'DX2&G3-5': 0, 'DX2&G3-6': 0, 'D12&G2-4': 0,
                 'D12&G2-6': 0, 'D1X&3+': 0, 'D12&G4+': 0, 'DX2&G2-4': 0, 'DX2&G2-5': 0, 'DX2&G2-6': 0, 'DX2&4+': 0,
                 'DX2&3+': 0, 'D12&G03': 0, 'D12&G02': 0, 'D1X&GG': 0, 'D12&G3-5': 0, 'D12&G3-6': 0, 'D12&G4-6': 0,
                 'D12&GG': 0, 'D1X&2+': 0, 'DX2&G23': 0, 'D12&G3+': 0, 'D1X&G3-5': 0, 'DX2&2+': 0,
                 })

    for i in range(final.shape[0]):
        for j in range(final.shape[1]):
            prob = final[i, j]
            game, keys = [], []
            if i >= j:
                game.append('1X')
            if i <= j:
                game.append('X2')
            if i != j:
                game.append('12')
            for g in game:
                prefix = 'D' + g + '&'
                if i >= 1 and j >= 1:
                    keys.append(prefix + 'GG')

                if i + j >= 2:
                    if prefix == 'D12&':
                        keys.append(prefix + 'G2+')
                    else:
                        keys.append(prefix + '2+')

                    if i + j <= 6:
                        keys.append(prefix + 'G2-6')
                        if i + j <= 5:
                            keys.append(prefix + 'G2-5')
                            if i + j <= 4:
                                keys.append(prefix + 'G2-4')
                                if i + j <= 3:
                                    keys.append(prefix + 'G23')

                if i + j >= 3:
                    if prefix == 'D12&':
                        keys.append(prefix + 'G3+')
                    else:
                        keys.append(prefix + '3+')

                    if i + j <= 6:
                        keys.append(prefix + 'G3-6')
                        if i + j <= 5:
                            keys.append(prefix + 'G3-5')
                else:
                    if prefix == 'D12&':
                        keys.append(prefix + 'G02')
                    else:
                        keys.append(prefix + 'G0-2')

                if i + j >= 4:
                    if prefix == 'D12&':
                        keys.append(prefix + 'G4+')
                    else:
                        keys.append(prefix + '4+')

                    if i + j <= 6:
                        keys.append(prefix + 'G4-6')
                else:
                    if prefix == 'D12&':
                        keys.append(prefix + 'G03')
                    else:
                        keys.append(prefix + 'G0-3')

            for key in keys:
                odds[key] += prob


def full_time_goals_combs(odds, final):
    odds.update({'1&2-3': 0, '1&G2-4': 0, '1&G2-5': 0, '1&G2-6': 0, '1&G3-4': 0, '1&G3-5': 0, '1&G3-6': 0,
                 '1&G4-5': 0, '1&G4-6': 0, '1&G5-6': 0, '2&2-3': 0, '2&G2-4': 0,
                 '2&G2-5': 0, '2&G2-6': 0, '2&G3-4': 0, '2&G3-5': 0, '2&G3-6': 0, '2&G4-5': 0, '2&G4-6': 0,
                 '2&G5-6': 0,})
    n = final.shape[0]
    mat1 = np.tril(final, k=-1)
    mat2 = np.triu(final, k=1)
    for i in range(2, 6):
        for j in range(i + 1, 7):
            key1 = '1&G' + str(i) + '-' + str(j)
            key2 = '2&G' + str(i) + '-' + str(j)
            if i == 2 and j == 3:
                key1 = '1&' + str(i) + '-' + str(j)
                key2 = '2&' + str(i) + '-' + str(j)
            odds[key1] = np.sum(np.tril(np.triu(np.fliplr(mat1), k = n - j - 1), k=n - i - 1))
            odds[key2] = np.sum(np.tril(np.triu(np.fliplr(mat2), k = n - j - 1), k=n - i - 1))


def prelazi_combs(odds, final_first, final_last):
    dict_to_update = {}
    both = np.multiply.outer(final_first, final_last)
    for key in obrada_dict:
        dict_to_update[key] = np.sum(np.multiply(obrada_dict[key], both))

    odds.update(dict_to_update)


def calc_goal_combs(odds, overs, limit=6, mode='full'):
    limits = {}
    for i in range(limit):
        for j in range(i + 1, limit + 1):
            if mode == 'full':
                key = 'G' + str(i) + '-' + str(j)
            elif mode == 'first':
                key = 'I' + str(i) + str(j)
            elif mode == 'last':
                key = 'II' + str(i) + str(j)
            elif mode == '30':
                key = '30MG' + str(i) + str(j)
            elif mode == '15':
                key = '15MG' + str(i) + str(j)
            if i != 0:
                limits[key] = overs[j + 0.5]['-'] - overs[i - 0.5]['-']
            else:
                limits[key] = overs[j + 0.5]['-']
    for key in overs:
        if mode == 'full':
            new_key = 'G' + str(int(math.ceil(key))) + '+'
        elif mode == 'first':
            new_key = 'I' + str(int(math.ceil(key))) + '+'
        elif mode == 'last':
            new_key = 'II' + str(int(math.ceil(key))) + '+'
        elif mode == '30':
            new_key = '30MG' + str(int(math.ceil(key))) + '+'
        elif mode == '15':
            new_key = '15MG' + str(int(math.ceil(key))) + '+'
        odds[new_key] = overs[key]['+']
    odds.update(limits)


def calc_over(final, n, rng=10):
    overs = {}
    for i in range(rng):
        gran1 = n + i - 0.5  # povedi racuna
        gran2 = n - i - 0.5
        under1 = np.sum(np.triu(np.fliplr(final), k=-i))
        under2 = np.sum(np.triu(np.fliplr(final), k=i))
        overs[gran1] = {'+': 1 - under1, '-': under1}
        overs[gran2] = {'+': 1 - under2, '-': under2}
    overs_fin = {key: overs[key] for key in overs if 0 < key < 7}
    return overs_fin


def combinations(odds, final, n):
    grans = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    combs = {}
    for gran_over in grans:
        mat1 = np.fliplr(np.triu(np.fliplr(final), k=n - gran_over - 0.5))
        mat2 = np.tril(final, k=-1)

        k1_min = calc_game(mat1, mat2)
        mat2 = np.triu(final, k=1)
        k2_min = calc_game(mat1, mat2)

        mat1 = np.fliplr(np.tril(np.fliplr(final), k=n - gran_over - 1.5))
        mat2 = np.tril(final, k=-1)
        k1_plus = calc_game(mat1, mat2)

        mat2 = np.triu(final, k=1)
        k2_plus = calc_game(mat1, mat2)

        combs[gran_over] = {'1&+': k1_plus, '1&-': k1_min, '2&+': k2_plus, '2&-': k2_min}
    
    odds['1&G0-2'], odds['2&G0-2'] = combs[2.5]['1&-'], combs[2.5]['2&-']
    odds['1&G0-3'], odds['2&G0-3'] = combs[3.5]['1&-'], combs[3.5]['2&-']
    odds['1&G0-4'], odds['2&G0-4'] = combs[4.5]['1&-'], combs[4.5]['2&-']
    odds['1&G0-5'], odds['2&G0-5'] = combs[5.5]['1&-'], combs[5.5]['2&-']
    odds['1&3+'], odds['2&3+'] = combs[2.5]['1&+'], combs[2.5]['2&+']
    odds['1&4+'], odds['2&4+'] = combs[3.5]['1&+'], combs[3.5]['2&+']
    odds['1&G5+'], odds['2&G5+'] = combs[4.5]['1&+'], combs[4.5]['2&+']


def calc_game(mat1, mat2):
    mask = np.multiply(mat1, mat2)
    mask[mask > 0] = 1
    return np.sum(np.multiply(mat1, mask))


def find_best_matrix(lam1, lam2, x_prob, n=10):
    cov_upper = 0.2
    # if(abs(lam1-lam2) < 1):
    #     cov_upper = 0.5
    t2 = time.time()
    final = np.zeros((n, n))
    x_array, cov_array = [], []
    for cov in np.arange(0, cov_upper, 0.01):
        for i in range(n):
            for j in range(n):
                final[i][j] = bivariate_poisson(i, j, lam1, lam2, cov=cov)
        x_array.append(np.sum(np.diag(final))), cov_array.append(cov)
    idx = find_nearest(x_array, x_prob)
    cov_final = cov_array[idx]

    for i in range(n):
        for j in range(n):
            final[i][j] = bivariate_poisson(i, j, lam1, lam2, cov=cov_final)
    return final, cov_final


def create_matrix(lam1, lam2, n=10, cov=0.1):
    final = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            final[i][j] = bivariate_poisson(i, j, lam1, lam2, cov=cov)
    return final


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def calculate_mean_poisson(gran, gran_prob_under=0.5):
    eq = lambda x: np.exp(-x)*sum(x**i / math.factorial(i) for i in range(int(math.ceil(gran)))) - gran_prob_under
    return fsolve(eq, gran)[0]


def get_exps(gran_ou, hend):
    gran_ou, hend = float(gran_ou), float(hend)
    lam1 = gran_ou / 2 + hend / 2
    lam2 = gran_ou / 2 - hend / 2
    return lam1, lam2


def calculate_mean_skellam(hend, gran, hend_prob_under=0.5):
    lam1_start, lam2_start = get_exps(gran, hend)
    for x in np.arange(0, gran, 0.01):
        if -0.005 <= sum([skellam.pmf(k=i, mu1=x, mu2=gran-x) for i in range(int(math.ceil(hend)), 10)]) - hend_prob_under <= 0.005:
            # return (gran - x, x, 1 - skellam.cdf(int(math.floor(hend)), x, gran - x))
            return x


def generate_matrix(gran, hend, gran_prob_under, hend_prob_under):
    total = calculate_mean_poisson(gran, gran_prob_under)
    lam1 = calculate_mean_skellam(hend, total, hend_prob_under)
    if not lam1:
        return (0,0)
    lam2 = total - lam1
    
    return lam1, lam2


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


def real_time_calculation(gran, hend, gran_prob_under=None, hend_prob_under=None, x_prob=None, gran_first=None,
                          hend_first=None, x_prob_first=None, model=4, margin=0.075, real_probs=False, cov=None):

    '''
    gran - granica over/under (total) full time (obavezan parametar)
    hend - granica hendikep full time (obavezan parametar)
    gran_prob_under - realna verovatnoca under-a na zadatoj granici total
    hend_prob_under - realna verovatnoca hendikepa na favorita (h1 ako hendikep negativan, i h2 ako je pozitivan)
    x_prob - realna verovatnoca X
    gran_first - granica total prvo poluvreme
    hend_first - granica hendikep prvo poluvreme, trenutno apsolutna vrednost

    Parametri margin i model ce biti definisani zavisno od takmicenja ili po mecu na neki nacin. Za potrebe testiranja ih drzati na default-nim vrednostima. 
    Parametar real_probs za potrebe testiranja drzati na True. Funkcija za obaranje ce naknadno biti dodata.
    Ispod su dati primeri poziva funkcije.
    hend i hend_first moraju imati isti znak (oba pozitivna ili oba negativna)
    u slucaju da se unose podaci za poluvreme, moraju biti uneseni gran_first i hend_first, a x_prob_first opciono (u vecini situacija se parametri za poluvreme ne prosledjuju)
    '''
    # md = test_master_data()

    reverse = False
    if hend > 0:
        reverse = True
    
    hend = abs(hend)
    if hend == 0.5 and hend_prob_under < 0.45500001:
        hend_prob_under = hend_prob_under * 1.03
    if hend_first:
        hend_first = abs(hend_first)

    model_mapping = {1: 8, 2: 10, 3: 12, 4: 14}
    n = model_mapping[model]
    
    if gran_prob_under:
        lam1, lam2 = get_exps(calculate_mean_poisson(gran, gran_prob_under), hend)
    else:
        lam1, lam2 = get_exps(gran + 0.17, hend)
    lam1, lam2 = generate_matrix(gran, hend, gran_prob_under, hend_prob_under)
    if lam1 == 0 and lam2 == 0:
        return (0.1,{base_to_code[key]:0 for key in base_to_code})
    if x_prob:
        final, cov_final = find_best_matrix(lam1, lam2, x_prob, n)
    else:
        final = create_matrix(lam1, lam2, n, cov=cov)
        cov_final = cov

    if gran_first and hend_first:
        lam1_first, lam2_first = get_exps(gran_first + 0.17, hend_first)
    else:
        lam1_first, lam2_first = lam1 * 0.435, lam2 * 0.435
        
    lam1_rest, lam2_rest = lam1 - lam1_first, lam2 - lam2_first
    lam1_30, lam2_30 = lam1_first * 0.62, lam2_first * 0.62
    lam1_15, lam2_15 = lam1_first * 0.29, lam2_first * 0.29
    
    if x_prob_first:
        final_first, cov_first = find_best_matrix(lam1_first, lam2_first, x_prob_first, n)
    else:
        final_first = create_matrix_pois(lam1_first, lam2_first, n)

    final_last = create_matrix_pois(lam1_rest, lam2_rest, n)
    final_30 = create_matrix_pois(lam1_30, lam2_30, n)
    final_15 = create_matrix_pois(lam1_15, lam2_15, n)

    odds = dict()
    full_time_goals_combs(odds, final)

    odds['K1'], odds['KX'], odds['K2'] = create1x2(final)
    
    # if odds['K2'] > odds['K1'] and hend==0.5:
    #     final, final_first, final_last = final.T, final_first.T, final_last.T
    #     odds['K1'], odds['KX'], odds['K2'] = create1x2(final)
    
    if final[0, 1] + final[0, 2] < 0:
        final = create_matrix_pois(lam1, lam2, n)
        final_first = create_matrix_pois(lam1_first, lam2_first, n)
        final_last = create_matrix_pois(lam1_rest, lam2_rest, n)
        odds['K1'], odds['KX'], odds['K2'] = create1x2(final)

    odds['P1'], odds['PX'], odds['P2'] = create1x2(final_first)
    odds['DP1'], odds['DPX'], odds['DP2'] = create1x2(final_last)

    final_first = fixing_kvotas_perc(odds, final_first, 0.05, '2', ['1'], prefix='P')
    odds['P1'], odds['PX'], odds['P2'] = create1x2(final_first)

    odds['2&GG'] = odds['K2'] - np.sum(final[0, 1:])
    odds['1&GG'] = odds['K1'] - np.sum(final[1:, 0])
    odds['X&GG'] = odds['KX'] - final[0, 0]
    odds['X&G0-2'] = final[0, 0] + final[1, 1]
    odds['X&2+'] = np.sum(np.diag(final)) - final[0, 0]
    
    odds['30K1'], odds['30KX'], odds['30K2'] = create1x2(final_30)
    odds['15K1'], odds['15KX'], odds['15K2'] = create1x2(final_15)

    odds['W1'], odds['W2'] = (1 / (1 - odds['KX'])) * odds['K1'], (1 / (1 - odds['KX'])) * odds['K2']
    odds['D1X'], odds['DX2'], odds['D12'] = odds['K1'] + odds['KX'], odds['K2'] + odds['KX'], odds['K1'] + odds['K2']
    odds['DW1'] = odds['P1'] * odds['DP1']
    odds['DW2'] = odds['P2'] * odds['DP2']
    odds['SW1'], odds['SW2'] = np.sum(final[1:, 0]), np.sum(final[0, 1:])

    odds['GG'], odds['GG2+'] = np.sum(final[1:, 1:]), np.sum(final[2:, 2:])
    odds['GN'], odds['nGG2+'] = np.sum(final[1:, 0]) + np.sum(final[0, 1:]) + final[0, 0], 1 - odds['GG2+']
    odds['GG&3+'] = 1 - (odds['GN'] + final[1, 1])
    odds['GG&4+'] = 1 - (np.sum(final[1:, 0]) + np.sum(final[0, 1:]) + final[0, 0] + final[1, 1] + final[1, 2] +
                         final[2, 1])
    odds['GG1'], odds['GN1'] = np.sum(final_first[1:, 1:]), 1 - np.sum(final_first[1:, 1:])
    odds['GG2'], odds['GN2'] = np.sum(final_last[1:, 1:]), 1 - np.sum(final_last[1:, 1:])
    odds['GG1&GG2'] = odds['GG1'] * odds['GG2']
    odds['GG1&GN2'] = odds['GG1'] * odds['GN2']
    odds['GN1&GN2'] = odds['GN1'] * odds['GN2']
    odds['GN1&GG2'] = odds['GN1'] * odds['GG2']

    odds['GG&1T2+'] = odds['GG'] - np.sum(final[1, 1:])
    odds['GG&2T2+'] = odds['GG'] - np.sum(final[1:, 1])

    odds['30MG1'], odds['30MGG'] = final_30[1, 0] + final_30[0, 1], np.sum(final_30[1:, 1:])
    odds['30MG0'] = final_30[0, 0]
    odds['15MG1'] = final_15[1, 0] + final_15[0, 1]
    odds['15MG0'] = final_15[0, 0]
    odds['FG1'] = lam1 / ((lam1 + lam2) / (1 - final[0, 0]))
    odds['FG2'] = lam2 / ((lam1 + lam2) / (1 - final[0, 0]))

    odds['1t1+2+'] = np.sum(final_first[1:, :]) * np.sum(final_last[2:, :])
    odds['1t2+2+'] = np.sum(final_first[2:, :]) * np.sum(final_last[2:, :])
    odds['1t2+1+'] = np.sum(final_first[2:, :]) * np.sum(final_last[1:, :])

    odds['2t1+2+'] = np.sum(final_first[:, 1:]) * np.sum(final_last[:, 2:])
    odds['2t2+2+'] = np.sum(final_first[:, 2:]) * np.sum(final_last[:, 2:])
    odds['2t2+1+'] = np.sum(final_first[:, 2:]) * np.sum(final_last[:, 1:])

    matrica_koef_kec = np.zeros(final.shape)
    matrica_koef_dvojka = np.zeros(final.shape)
    matrica_koef_kec[1:, 0] = 1
    matrica_koef_dvojka[0, 1:] = 1

    for i in range(1, len(matrica_koef_kec)):
        for j in range(1, len(matrica_koef_kec)):
            matrica_koef_kec[i,j] = i/(i+j)
            matrica_koef_dvojka[i,j] = j/(i+j)    
    matrica_PG1= np.multiply(final,matrica_koef_kec)
    matrica_PG2= np.multiply(final,matrica_koef_dvojka)

    odds['1&FG1'] = np.sum(np.tril(matrica_PG1,-1))
    odds['1&FG2'] = np.sum(np.tril(matrica_PG2,-1))
    odds['2&FG1'] = np.sum(np.triu(matrica_PG1,1))
    odds['2&FG2'] = np.sum(np.triu(matrica_PG2,1))
    odds['X&FG1'] = np.sum(np.diag(matrica_PG1))
    odds['X&FG2'] = np.sum(np.diag(matrica_PG2))

    odds['FG1&1T2+'] = np.sum(matrica_PG1[2:,:])
    odds['FG2&2T2+'] = np.sum(matrica_PG2[:,2:])
    odds['FG2&G2+'] = np.sum(matrica_PG2) - (matrica_PG2[0,0] + matrica_PG2[0,1] + matrica_PG2[1,0])
    odds['FG1&G2+'] = np.sum(matrica_PG1) - (matrica_PG1[0,0] + matrica_PG1[0,1] + matrica_PG1[1,0])
    odds['FG2&G3+'] = odds['FG2&G2+'] - (matrica_PG2[1,1] + matrica_PG2[2,0] + matrica_PG2[0,2])
    odds['FG1&G3+'] = odds['FG1&G2+'] - (matrica_PG1[1,1] + matrica_PG1[2,0] + matrica_PG1[0,2])
    odds['FG2&G4+'] = odds['FG2&G3+'] - (matrica_PG2[3,0] + matrica_PG2[0,3] + matrica_PG2[2,1] + matrica_PG2[1,2])
    odds['FG1&G4+'] = odds['FG1&G3+'] - (matrica_PG1[3,0] + matrica_PG1[0,3] + matrica_PG1[2,1] + matrica_PG1[1,2])

    odds['FG1&GG'] = np.sum(matrica_PG1[1:,1:])
    odds['FG2&GG'] = np.sum(matrica_PG2[1:,1:])

    turned = np.fliplr(final_first)
    turned_sec = np.fliplr(final_last)

    odds['I=II'], odds['I>II'] = 0, 0
    for i in range(-turned.shape[0], turned.shape[0]):
        odds['I>II'] += np.sum(np.diag(turned, i)) * np.sum(np.triu(turned_sec, i + 1))
        odds['I=II'] += np.sum(np.diag(turned, i)) * np.sum(np.diag(turned_sec, i)) 
    odds['I<II'] = 1 - odds['I=II'] - odds['I>II']

    final_overs = create_matrix_pois(lam1,lam2,n)
    overs = calc_over(final_overs, n, rng=18)

    overs_first = calc_over(final_first, n, rng=18)
    overs_sec = calc_over(final_last, n, rng=18)
    overs_30 = calc_over(final_30, n, rng=18)
    overs_15 = calc_over(final_15, n, rng=18)

    first_second_half_goal_combs(odds, overs_f=overs_first, overs_s=overs_sec)

    odds['2+2+'] = overs_first[1.5]['+'] * overs_sec[1.5]['+']

    goals_one_team(odds, final, final_first, final_last)
    calc_goal_combs(odds, overs, limit=6, mode='full')
    calc_goal_combs(odds, overs_first, limit=4, mode='first')
    calc_goal_combs(odds, overs_sec, limit=4, mode='last')
    calc_goal_combs(odds, overs_30, limit=4, mode='30')
    calc_goal_combs(odds, overs_15, limit=4, mode='15')
    odds['2HW1'], odds['2HW2'] = np.sum(np.tril(final, -2)), np.sum(np.triu(final, 2))
    odds['3HW1'], odds['3HW2'] = np.sum(np.tril(final, -3)), np.sum(np.triu(final, 3))


    odds['1&1T2+'] = odds['K1'] - final[1, 0]
    odds['2&2T2+'] = odds['K2'] - final[0, 1]

    odds['1&1T3+'] = odds['K1'] - final[1, 0] - final[2, 0] - final[2, 1]
    odds['2&2T3+'] = odds['K2'] - final[0, 1] - final[0, 2] - final[1, 2]
    odds['1&1T2-3'] = final[2, 0] + final[2, 1] + final[3, 0] + final[3, 1] + final[3, 2]
    odds['2&2T2-3'] = final[0, 2] + final[1, 2] + final[0, 3] + final[1, 3] + final[2, 3]

    odds['1v3+'] = 1 - final[0, 0] - final[0, 1] - final[0, 2] - final[1, 1]
    odds['2v3+'] = 1 - final[0, 0] - final[1, 0] - final[2, 0] - final[1, 1]
    odds['XvG3+'] = 1 - final[1, 0] - final[0, 1] - final[2, 0] - final[0, 2]
    odds['GGvG3+'] = 1 - final[0, 0] - final[1, 0] - final[0, 1] - final[2, 0] - final[0, 2]

    odds['FG1&1T2+'] = odds['FG1'] * odds['GH2+']
    odds['FG2&2T2+'] = odds['FG2'] * odds['GA2+']

    odds['FG2&G2+'] = odds['FG2'] * (odds['G2+'] - np.sum(final[0, 2:]))
    odds['FG1&G2+'] = odds['FG1'] * (odds['G2+'] - np.sum(final[2:, 0]))

    odds['FG2&G3+'] = odds['FG2'] * (odds['G3+'] - np.sum(final[0, 3:]))
    odds['FG1&G3+'] = odds['FG1'] * (odds['G3+'] - np.sum(final[3:, 0]))

    odds['FG2&G4+'] = odds['FG2'] * (odds['G4+'] - np.sum(final[0, 4:]))
    odds['FG1&G4+'] = odds['FG1'] * (odds['G4+'] - np.sum(final[4:, 0]))

    odds['GG&G23'] = final[1, 1] + final[2, 1] + final[1, 2]

    odds['30M2+0'], odds['15M0+2+'] = odds['30MG2+'] * odds['15MG0'], odds['15MG0'] * odds['30MG2+']
    odds['30M1+0'], odds['15M1+0'] = odds['30MG1+'] * odds['15MG0'], odds['15MG1+'] * odds['30MG0']
    odds['30M0+1+'], odds['15M0+1+'] = odds['30MG0'] * odds['15MG1+'], odds['15MG0'] * odds['30MG1+']
    odds['30M1+1+'], odds['15M1+1+'] = odds['30MG1+'] * odds['15MG1+'], odds['15MG1+'] * odds['30MG1+']
    odds['30M2+1+'], odds['15M1+2+'] = odds['30MG2+'] * odds['15MG1+'], odds['15MG1+'] * odds['30MG2+']
    prelazi_combs(odds, final_first, final_last)

    goals_match(odds, final, final_first, final_last)
    correct_score(odds, final)
    correct_score(odds, final_first, mode='first')
    double_chance_goal_combs_full(odds, final)
    combinations(odds, final, n)

    odds['GG1&I3+'] = odds['GG1'] - (final_first[1, 1])
    odds['GG2&II3+'] = odds['GG2'] - (final_last[1, 1])

    odds['G-G'] = odds['I1+'] * odds['II1+']
    
    # to_remove = [key for key in odds if key not in md]
    # [odds.pop(key) for key in to_remove]

    if reverse:
        odds = invert(odds)

    if not real_probs:
        odds = obaranje_fudbal(odds)

    odds_code = {base_to_code[key]: odds[key] for key in odds if key in base_to_code}

    return cov_final, odds_code


def invert(odds):
    for key in odds:
        if key in mapping.keys():
            odds[mapping[key]], odds[key] = odds[key], odds[mapping[key]]
    return odds


if __name__ == '__main__':
    #odds_cov = real_time_calculation(2.5, -0.5, 0.5593758630, 0.4518781279216851, cov=0.12)[-1]
    odds = real_time_calculation(3.5, 0.5, 0.606837, 1-0.594201, 0.21909)[-1]
    for od in odds:
        if od == 'KI X' or od=='KI 1' or od =='KI 2' or od=='UG 0-2' or od=='UG 3+':
            print(od, 1/odds[od])
            
