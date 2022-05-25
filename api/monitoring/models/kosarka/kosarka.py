# -*- coding: utf-8 -*-
import math
import numpy as np
from scipy.special import factorial
import scipy.stats

'''
Ova skripta sluzi za racunanje celokupne ponude u kosarci. Jedina funkcija koja je vama bitna je real_time_calculation (objasnjenja imate u funkciji).
Ostale sluze samo kako bi ih ona pozivala. Koristi se python 3.6.
'''


mapping = {'C2-2&|-|': 'C1-1&|-|', 'C2-1&|-|':'C1-2&|-|', 'C2-2&|+|': 'C1-1&|+|', 'C1-2&|+|': 'C2-1&|+|', 'C1-2&|+|': 'C2-1&|+|',
            '1-1&|+|': '2-2&|+|', '1-2&|+|':'2-1&|+|', '1-1&|-|': '2-2&|-|', '1-2&|-|': '2-1&|-|', 'Icet2&|+|':'Icet1&|+|', 
            'Icet2&|-|': 'Icet1&|-|', 'IcetH1&|-|': 'IcetH2&|-|', 'IcetH1&|+|':'IcetH2&|+|', 'D Icet |-|':'G Icet |-|', 
            'G Icet |+|': 'D Icet |+|', 'HC1':'HC2', 'HC11': 'HC21', 'HC12':'HC22', 'Ipol1&|-|': 'Ipol2&|-|', 'Ipol1&|+|':'Ipol2&|+|',
            'IpolH1&|+|': 'IpolH2&|+|', 'IpolH1&|-|':'IpolH2&|-|', 'G Ipol |-|': 'D Ipol |-|', 'D Ipol |+|':'G Ipol |+|', 
            'HP16': 'HP26', 'HP15':'HP25', 'HP14': 'HP24', 'HP13':'HP23', 'HP12': 'HP22', 'HP11':'HP21', 'HP1': 'HP2', 
            'D |+|': 'G |+|', 'D |-|' : 'G |-|', '1&|-|':'2&|-|', '1&|+|': '2&|+|', 'H1&|-|': 'H2&|-|', 'H1&|+|': 'H2&|+|',
            'H1': 'H2', 'H11': 'H21', 'H12': 'H22', '1 bez prod': '2 bez prod', 'D 1-5': 'G 1-5', 'D 6-10': 'G 6-10',
            'D 11-15': 'G 11-15', 'D 16-20': 'G 16-20', 'D 21-25': 'G 21-25', 'D 26+': 'G 26+', 'KI 1': 'KI 2', 'Ipol 1': 'Ipol 2',
            'Icet 1': 'Icet 2', 'Imin 1': 'Imin 2', 'DP 1': 'DP 2', 'PK 1-1': 'PK 2-2', 'PK 1-2': 'PK 2-1', 'PK X-1': 'PK X-2', 
            'CK 1-1': 'CK 2-2', 'CK 1-2': 'CK 2-1', 'CK X-1': 'CK X-2', 'MK 1-1': 'MK 2-2', 'MK 1-2': 'MK 2-1', 'MK X-1': 'MK X-2',
            'H13': 'H23', 'H14': 'H24', 'H15': 'H25', 'H16': 'H26', 'H17': 'H27', 'H18': 'H28', 'H19': 'H29', 'H110': 'H210', 
            'H111': 'H211', 'H112': 'H212'}


def poisson(lam, k):
    # return float(Decimal(pow(lam, k)) * Decimal(math.exp(-lam)) / Decimal(math.factorial(k)))
    return pow(lam, k) * math.exp(-lam) / math.factorial(k)


def calc_points(igre, x, f, s, gran):
    if (f + s) < gran:
        igre['|-|'] += x
    else:
        igre['|+|'] += x


def calc_hend(igre, x, f, s, hend):
    if f - s > hend:
        igre['H1'] += x
    else:
        igre['H2'] += x


def calc_one(igre, x, points_one, gran):
    if points_one > gran:
        igre['|+|'] += x
    else:
        igre['|-|'] += x


def calculate_odds_different(p, n=2):
    if p != 0:
        pz = 1 / math.exp(-math.log(n * (1 - 0.075)) * math.log(1 / p) / math.log(2))
    else:
        pz = 0
    return pz

def create_matrix_normal(lam1, lam2, num, std):

    p_x, p_y = [], []
    norm_x , norm_y = scipy.stats.norm(lam1, std), scipy.stats.norm(lam2, std)
    for i in range(num):
        p_x.append(norm_x.cdf(i + 0.5) - norm_x.cdf(i - 0.5))
        p_y.append(norm_y.cdf(i + 0.5) - norm_y.cdf(i - 0.5))
    final = np.outer(p_x, p_y)
    return final

def create_matrix_pois(lam1, lam2, num):

    x = np.arange(0, num, 1)
    y = np.arange(0, num, 1)
    poisson1 = scipy.stats.poisson.pmf(x, lam1, loc=0)
    poisson2 = scipy.stats.poisson.pmf(y, lam2, loc=0)
    final = np.outer(poisson1, poisson2)
    return final
    
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
    # poisson1 = power1 * poisson1
    poisson2 = expon2 / faktor
    poisson2 = power2 * poisson2 * power2
    # poisson2 = power2 * poisson2
    # print np.sum(poisson1[102:]) * np.sum(poisson2[102:])
    final = np.outer(poisson1, poisson2)
    return final


def prelazi(test, n, X):
    odds = {'PK 1-1': 0, 'PK 1-2': 0, 'PK 2-1': 0, 'PK 2-2': 0}
    pk1_x, pk2_x = 0, 0
    for i in range(1, n + 1):
        odds['PK 1-1'] += np.sum(np.diag(test, k=-i)) * np.sum(np.tril(test, k=i-1))
        odds['PK 2-2'] += np.sum(np.diag(test, k=i)) * np.sum(np.triu(test, k=1-i))
        odds['PK 1-2'] += np.sum(np.diag(test, k=-i)) * np.sum(np.triu(test, k=(i+1)))
        odds['PK 2-1'] += np.sum(np.diag(test, k=i)) * np.sum(np.tril(test, k=-(i+1)))
        # pk1_x += np.sum(np.diag(test, k=-i)) * np.sum(np.diag(test, k=i))
        # pk2_x += np.sum(np.diag(test, k=i)) * np.sum(np.diag(test, k=-i))
    odds['PK X-1'] = np.sum(np.diag(test)) * np.sum(np.tril(test, k=-1))
    odds['PK X-2'] = np.sum(np.diag(test)) * np.sum(np.triu(test, k=1))
    # pkX_X = np.sum(np.diag(test)) * np.sum(np.diag(test))
    for key in odds:
        odds[key] += X / 6

    return odds


def prelazi_prvi(first, rest, n, x, name='MK'):
    odds = {name + ' 1-1': 0, name + ' 1-2': 0, name + ' 2-1': 0, name + ' 2-2': 0}
    pk1_x, pk2_x = 0, 0
    for i in range(1, n + 1):
        odds[name + ' 1-1'] += np.sum(np.diag(first, k=-i)) * np.sum(np.tril(rest, k=i-1))
        odds[name + ' 2-2'] += np.sum(np.diag(first, k=i)) * np.sum(np.triu(rest, k=1-i))
        odds[name + ' 1-2'] += np.sum(np.diag(first, k=-i)) * np.sum(np.triu(rest, k=(i+1)))
        odds[name + ' 2-1'] += np.sum(np.diag(first, k=i)) * np.sum(np.tril(rest, k=-(i+1)))
        # pk1_x += np.sum(np.diag(first, k=-i)) * np.sum(np.diag(rest, k=i))
        # pk2_x += np.sum(np.diag(test, k=i)) * np.sum(np.diag(test, k=-i))
    odds[name + ' X-1'] = np.sum(np.diag(first)) * np.sum(np.tril(rest, k=-1))
    odds[name + ' X-2'] = np.sum(np.diag(first)) * np.sum(np.triu(rest, k=1))
    # pkX_X = np.sum(np.diag(test)) * np.sum(np.diag(test))

    for key in odds:
        odds[key] += x / 6

    return odds


def egal(odds, k):
    diff = 1
    gran = 0
    for key in odds:
        razlika = abs(odds[key][k] - 0.5)
        if razlika < diff:
            diff = razlika
            gran = key
    return gran, odds[gran]

def find_closest(lam, mat, tip):
    gran_1, gran_2, gran_3 = round(lam) + 0.5, round(lam) - 0.5, round(lam) + 1.5
    if tip == 'prvi':
        tm = {gran_1: np.sum(mat[(int(round(lam)) + 1):, 0:]), gran_2: np.sum(mat[(int(round(lam))):, 0:]), gran_3: np.sum(mat[(int(round(lam)) + 2):, 0:])}
    else:
        tm = {gran_1: np.sum(mat[0:, (int(round(lam)) + 1):]), gran_2: np.sum(mat[0:, (int(round(lam))):]), gran_3: np.sum(mat[0:,(int(round(lam)) + 2):])}
    grantm, vredtm = min(tm.items(), key=lambda item: abs(item[1] - 0.5))
    return grantm, vredtm


def calc_over(final, n):
    overs = {}
    for i in range(150):
        gran1 = n + i - 0.5
        gran2 = n - i - 0.5
        under1 = np.sum(np.triu(np.fliplr(final), k=-i))
        under2 = np.sum(np.triu(np.fliplr(final), k=i))
        overs[gran1] = {'+': 1 - under1, '-': under1}
        overs[gran2] = {'+': 1 - under2, '-': under2}
        #print(gran1, gran2, overs[gran1], overs[gran2])
    return overs


def calc_hend(final):
    hends = {}
    for i in range(100):
        gran1 = i + 0.5
        gran2 = -i + 0.5
        h2_1 = np.sum(np.triu(final, k=-i))
        h2_2 = np.sum(np.triu(final, k=i))
        hends[-gran1] = {'h1': 1 - h2_1, 'h2': h2_1}
        hends[-gran2] = {'h1': 1 - h2_2, 'h2': h2_2}

    return hends


def calc_game(mat1, mat2):
    mask = np.multiply(mat1, mat2)
    mask[mask > 0] = 1
    return np.sum(np.multiply(mat1, mask))



def both_teams(mat):
    tm1_tm2 = {}
    for i in range(0, 120):
        gran = i + 0.5
        over = np.sum(mat[(i + 1):, (i + 1):])
        tm1_tm2[gran] = {'over': over, 'under': 1 - over}
    gran_over_oba, otp = egal(tm1_tm2, 'over')
    # print tm1_tm2[gran_over_oba + 1]
    return gran_over_oba, otp

def lin_inc(start, end, x):
    a = (end[1] - start[1]) / (end[0] - start[0])
    b = start[1] - a * start[0]
    y = a * x + b
    return y

def fix(k1, k2, odds, key):
    odds[key + ' 1'] = np.sum(k1)
    odds[key + ' 2'] = np.sum(k2)
    odds[key + ' X'] = 1 - odds[key + ' 1'] - odds[key + ' 2']


def period(mat, keys, odds, lam1, lam2, dim, p, all=True):
    # primer: {hend: HP, rest: Ipol}
    n = dim
    if p == 'p':
        otp_key_base = keys['rest'] + ' OTP'
        num_gran = 7
        base_hend = ('HP1', 'HP2')
        base_ou = ('Ipol |+|', 'Ipol |-|')
    else:
        num_gran = 3
        otp_key_base = keys['rest'] + ' OTP '
        base_hend = ('HC1', 'HC2')
        base_ou = ('Icet |+|', 'Icet |-|')

    overs = calc_over(mat, dim)
    granica_ou, over = egal(overs, '+')

    if all:
        alternative(odds, num_gran, granica_ou, overs, base_ou)

        hends = calc_hend(mat)
        gran_hend, hend = egal(hends, 'h1')
        alternative(odds, num_gran, gran_hend, hends, base_hend)

        gran_oba, otp = both_teams(mat)
        odds[otp_key_base + '|+|'] = {'vrednost': otp['over'], 'granica_ou': gran_oba}
        odds[otp_key_base + '|-|'] = {'vrednost': otp['under'], 'granica_ou': gran_oba}

        gran1, vred1 = find_closest(lam1, mat, 'prvi')
        gran2, vred2 = find_closest(lam2, mat, 'drugi')

        odds['D' + ' ' + keys['rest'] + ' |+|'] = {'granica_ou': gran1, 'vrednost': vred1}
        odds['D' + ' ' + keys['rest'] + ' |-|'] = {'granica_ou': gran1, 'vrednost': 1 - vred1}
        odds['G' + ' ' + keys['rest'] + ' |+|'] = {'granica_ou': gran2, 'vrednost': vred2}
        odds['G' + ' ' + keys['rest'] + ' |-|'] = {'granica_ou': gran2, 'vrednost': 1 - vred2}

        odds[keys['rest'] + ' Par'] = 0.5
        odds[keys['rest'] + ' Nepar'] = 0.5

        mat1 = np.fliplr(np.triu(np.fliplr(mat), k=n - granica_ou - 0.5))
        mat2 = np.triu(mat, k=gran_hend + 0.5)
        odds[keys['rest'] + 'H2&|-|'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou, 'granica_hd': gran_hend}
        mat1 = np.fliplr(np.tril(np.fliplr(mat), k=n - granica_ou - 1.5))
        odds[keys['rest'] + 'H2&|+|'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou, 'granica_hd': gran_hend}
        mat1 = np.fliplr(np.tril(np.fliplr(mat), k=n - granica_ou - 1.5))
        mat2 = np.tril(mat, k=gran_hend - 0.5)
        odds[keys['rest'] + 'H1&|+|'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou, 'granica_hd': gran_hend}
        odds[keys['rest'] + 'H1&|-|'] = {'vrednost': 1 - odds[keys['rest'] + 'H2&|-|']['vrednost'] -
                                         odds[keys['rest'] + 'H2&|+|']['vrednost'] -
                                         odds[keys['rest'] + 'H1&|+|']['vrednost'],
                                         'granica_ou': granica_ou, 'granica_hd': gran_hend}
        mat1 = np.fliplr(np.triu(np.fliplr(mat), k=n - granica_ou - 0.5))
        mat2 = np.tril(mat, k=-1)
        odds[keys['rest'] + '1&|-|'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou}

        mat2 = np.triu(mat, k=1)
        odds[keys['rest'] + '2&|-|'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou}

        mat1 = np.fliplr(np.tril(np.fliplr(mat), k=n - granica_ou - 1.5))
        mat2 = np.tril(mat, k=-1)
        odds[keys['rest'] + '1&|+|'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou}

        mat2 = np.triu(mat, k=1)
        odds[keys['rest'] + '2&|+|'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou}
    else:
        odds[keys['rest'] + ' |+|'] = {'vrednost': overs[2.5]['+'], 'granica_ou': 2.5}
        odds[keys['rest'] + ' |-|'] = {'vrednost': overs[2.5]['-'], 'granica_ou': 2.5}
        odds[keys['rest'] + ' |+|1'] = {'vrednost': overs[3.5]['+'], 'granica_ou': 3.5}
        odds[keys['rest'] + ' |-|1'] = {'vrednost': overs[3.5]['-'], 'granica_ou': 3.5}


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
        odds[base[0] + ext] = {str_gran: granica - (num_gran - 1) / 2 + i, 'vrednost': full[granica - (num_gran - 1) / 2 + i][parts[0]]}
        odds[base[1] + ext] = {str_gran: granica - (num_gran - 1) / 2 + i, 'vrednost': full[granica - (num_gran - 1) / 2 + i][parts[1]]}


def prelazi_over(odds, ext):
    if ext == 'C':
        tip = 'CK'
    else:
        tip = 'PK'

    odds[ext + '1-1&|+|'] = {'vrednost': odds[tip + ' 1-1'] * odds['|+|6']['vrednost'], 'granica_ou': odds['|+|6']['granica_ou']}
    odds[ext + '1-2&|+|'] = {'vrednost': odds[tip + ' 1-2'] * odds['|+|6']['vrednost'], 'granica_ou': odds['|+|6']['granica_ou']}
    odds[ext + '2-1&|+|'] = {'vrednost': odds[tip + ' 2-1'] * odds['|+|6']['vrednost'], 'granica_ou': odds['|+|6']['granica_ou']}
    odds[ext + '2-2&|+|'] = {'vrednost': odds[tip + ' 2-2'] * odds['|+|6']['vrednost'], 'granica_ou': odds['|+|6']['granica_ou']}
    odds[ext + '1-1&|-|'] = {'vrednost': odds[tip + ' 1-1'] * odds['|-|6']['vrednost'], 'granica_ou': odds['|+|6']['granica_ou']}
    odds[ext + '1-2&|-|'] = {'vrednost': odds[tip + ' 1-2'] * odds['|-|6']['vrednost'], 'granica_ou': odds['|+|6']['granica_ou']}
    odds[ext + '2-1&|-|'] = {'vrednost': odds[tip + ' 2-1'] * odds['|-|6']['vrednost'], 'granica_ou': odds['|+|6']['granica_ou']}
    odds[ext + '2-2&|-|'] = {'vrednost': odds[tip + ' 2-2'] * odds['|-|6']['vrednost'], 'granica_ou': odds['|+|6']['granica_ou']}


def get_exps(gran_ou, hend):
    lam1 = gran_ou / 2 + hend / 2
    lam2 = gran_ou / 2 - hend / 2
    return lam1, lam2


def to_real(k1, k2):
    k1, k2 = float(k1), float(k2)
    p1 = 1 / k1 - (1 / k1 + 1 / k2 - 1) / 2
    p2 = 1 / k2 - (1 / k1 + 1 / k2 - 1) / 2
    return p1, p2


def get_exps_with_odds(over, under, gran_ou, h1, h2, gran_hd):
    over_real, under_real = to_real(over, under)
    h1_real, h2_real = to_real(h1, h2)
    temp_gran_ou = 2 * gran_ou * over_real
    temp_gran_hd = 2 * gran_hd * h1_real
    lam1, lam2 = get_exps(temp_gran_ou, temp_gran_hd)
    return lam1, lam2


def minute(lam1, lam2, faktor=0.021):
    odds = {}
    minute = create_matrix(lam1 * faktor, lam2 * faktor, 15)
    rest = create_matrix(lam1 * (1 - faktor), lam2 * (1 - faktor), 160)
    fix(np.tril(minute, k=-1), np.triu(minute, k=1), odds, 'Imin')
    odds.update(prelazi_prvi(minute, rest, 15, name='MK'))
    suma = 0
    for key in odds:
        if 'MK' in key:
            suma += odds[key]
    x = 1 - suma
    for key in odds:
        if 'MK' in key:
            odds[key] += x / 6
    overs = calc_over(minute, 15)
    odds['Imin |+|'] = {'vrednost': overs[2.5]['+'], 'granica_ou': 2.5}
    odds['Imin |-|'] = {'vrednost': overs[2.5]['-'], 'granica_ou': 2.5}
    odds['Imin |+|1'] = {'vrednost': overs[3.5]['+'], 'granica_ou': 3.5}
    odds['Imin |-|1'] = {'vrednost': overs[3.5]['-'], 'granica_ou': 3.5}
    '''
    kvote = {}
    for key in odds:
        if '|' in key:
            kvote[key] = {'vrednost': 1 / odds[key]['vrednost'], 'granica_ou': odds[key]['granica_ou']}

    print kvote['Imin |+|']
    print kvote['Imin |+|1']
    '''
    return odds


def reduce_by_perc(odds, perc, perc_pol, perc_prelazi, perc_dp, perc_prelazi_2):
    odds['Ipol 1'] += perc_pol
    odds['Ipol 2'] -= perc_pol
    odds['PK 1-1'] += perc_prelazi
    odds['PK 2-2'] -= perc_prelazi
    odds['PK 2-1'] += perc_prelazi_2
    odds['PK 1-2'] -= perc_prelazi_2
    odds['DP 1'] += perc_dp
    odds['DP 2'] -= perc_dp
    odds['1&|+|']['vrednost'] += perc / 2
    odds['1&|-|']['vrednost'] += perc / 2
    odds['2&|+|']['vrednost'] -= perc / 2
    odds['2&|-|']['vrednost'] -= perc / 2


def clone_correction(odds, key1, key2, perc):
    odds[key1]['vrednost'] = perc * odds[key1]['vrednost']
    odds[key2]['vrednost'] = 1 - odds[key1]['vrednost'] 


def fix_margins(final, px):
    odds = {'D 1-5' : 0, 'D 6-10' : 0, 'D 11-15' : 0, 'D 16-20' : 0, 'D 21-25' : 0, 'D 26+' : 0, 
            'G 1-5' : 0, 'G 6-10' : 0, 'G 11-15' : 0, 'G 16-20' : 0, 'G 21-25' : 0, 'G 26+' : 0}


    odds['D 1-5'] = np.sum(np.triu(np.tril(final, k=-1), k=-5))
    odds['D 6-10'] = np.sum(np.triu(np.tril(final, k=-6), k=-10))
    odds['D 11-15'] = np.sum(np.triu(np.tril(final, k=-11), k=-15))
    odds['D 16-20'] = np.sum(np.triu(np.tril(final, k=-16), k=-20))
    odds['D 21-25'] = np.sum(np.triu(np.tril(final, k=-21), k=-25))
    odds['D 26+'] = np.sum(np.tril(final, k=-26))

    odds['G 1-5'] = np.sum(np.tril(np.triu(final, k=1), k=5))
    odds['G 6-10'] = np.sum(np.tril(np.triu(final, k=6), k=10))
    odds['G 11-15'] = np.sum(np.tril(np.triu(final, k=11), k=15))
    odds['G 16-20'] = np.sum(np.tril(np.triu(final, k=16), k=20))
    odds['G 21-25'] = np.sum(np.tril(np.triu(final, k=21), k=25))
    odds['G 26+'] = np.sum(np.triu(final, k=26))

    return odds

def fix_margins_normal(final, px):
    odds = {'D 1-5' : 0, 'D 6-10' : 0, 'D 11-15' : 0, 'D 16-20' : 0, 'D 21-25' : 0, 'D 26+' : 0,
            'G 1-5' : 0, 'G 6-10' : 0, 'G 11-15' : 0, 'G 16-20' : 0, 'G 21-25' : 0, 'G 26+' : 0}


    odds['D 1-5'] = np.sum(np.triu(np.tril(final, k=-1), k=-5))
    odds['D 6-10'] = np.sum(np.triu(np.tril(final, k=-6), k=-10))
    odds['D 11-15'] = np.sum(np.triu(np.tril(final, k=-11), k=-15))
    odds['D 16-20'] = np.sum(np.triu(np.tril(final, k=-16), k=-20))
    odds['D 21-25'] = np.sum(np.triu(np.tril(final, k=-21), k=-25))
    odds['D 26+'] = np.sum(np.tril(final, k=-26))

    odds['G 1-5'] = np.sum(np.tril(np.triu(final, k=1), k=5))
    odds['G 6-10'] = np.sum(np.tril(np.triu(final, k=6), k=10))
    odds['G 11-15'] = np.sum(np.tril(np.triu(final, k=11), k=15))
    odds['G 16-20'] = np.sum(np.tril(np.triu(final, k=16), k=20))
    odds['G 21-25'] = np.sum(np.tril(np.triu(final, k=21), k=25))
    odds['G 26+'] = np.sum(np.triu(final, k=26))


    # odds['D 1-5'] += (1/2)*px
    # odds['D 6-10'] += (1/2)*px

    return odds


def poeni_cetvrtine(faktor_e, full_time_ou):
    
    odds = {}
    prob = 0
    for i in range(100):
        gran = i + 0.5
        prob += poisson(faktor_e*full_time_ou, i)
        odds[gran] = {'-': prob, '+':1 - prob}

    return odds
    

def real_time_calculation(full_time_ou, full_time_hd, half_time_ou=None, half_time_hd=None, quarter_ou=None, quarter_hd=None, model=1, competition='other'):
    '''
    full_time_ou - granica over/under najbliza verovatnoci 0.5 (total) full time (obavezan parametar)
    full_time_hd - granica hendikep full time najbliza verovatnoci 0.5 (obavezan parametar)
    half_time_ou - granica over/under (total) half time najbliza verovatnoci 0.5 (neobavezan parametar, ako postoji treba proslediti)
    half_time_hd - granica hendikep half time najbliza verovatnoci 0.5 (neobavezan parametar, ako postoji treba proslediti)
    quarter_ou - granica over/under (total) 1 cetvrtina najbliza verovatnoci 0.5 (neobavezan parametar, ako postoji treba proslediti)
    quarter_hd - granica hendikep 1 cetvrtina najbliza verovatnoci 0.5 (neobavezan parametar, ako postoji treba proslediti)
    

    Parametar model ce biti definisan zavisno od takmicenja ili po mecu na neki nacin. Za potrebe testiranja ih drzati na default-nim vrednostima. 
    Funkcija za obaranje ce naknadno biti dodata.
    Ispod su dati primeri poziva funkcije
    '''

    nuliranje = False
    
    reverse = False
    if full_time_hd > 0:
        reverse = True
    
    full_time_hd = abs(full_time_hd)

    full_time_ou, full_time_hd = float(full_time_ou), float(full_time_hd)
    
    if competition == 'other':
        faktor_e = 0.294
        faktor_n = 0.206
    elif competition == 'NBA':
        faktor_e = 0.287
        faktor_n = 0.213

    if half_time_ou and half_time_hd:
        pol_ou, pol_hd = half_time_ou, half_time_hd
        if quarter_ou and quarter_hd:
            cet_ou, cet_hd = quarter_ou, quarter_hd
        else:
            cet_ou, cet_hd = float(half_time_ou) / 2, float(half_time_hd) / 2
        if abs(full_time_ou / 2 - half_time_ou) > 3:
            nuliranje = True
    else:
        pol_ou, pol_hd, cet_ou, cet_hd = float(full_time_ou) / 2, float(full_time_hd) / 2, float(full_time_ou) / 4, float(full_time_hd) / 4
    lam1, lam2 = get_exps(full_time_ou, full_time_hd)
    lam1_first, lam2_first = get_exps(pol_ou, pol_hd)
    lam1_sec, lam2_sec = get_exps(full_time_ou - pol_ou, full_time_hd - pol_hd)
    lam1_quarter, lam2_quarter = get_exps(cet_ou, cet_hd)
    lam1_x3, lam2_x3 = get_exps(full_time_ou - cet_ou, full_time_hd - cet_hd)
    pol, cet = pol_ou / full_time_ou, cet_ou / pol_ou
    final = create_matrix(lam1, lam2, 160)
    first = create_matrix(lam1_first, lam2_first, 80)
    sec = create_matrix(lam1_sec, lam2_sec, 80)
    quarter = create_matrix(lam1_quarter, lam2_quarter, 60)
    n = 160
    if full_time_ou > 250:
        final = create_matrix_pois(lam1, lam2, 260)
        first = create_matrix(lam1_first, lam2_first, 160)
        sec = create_matrix(lam1_sec, lam2_sec, 160)
        quarter = create_matrix(lam1_quarter, lam2_quarter, 120)
        n = 260

    quarterx3 = create_matrix(lam1_x3, lam2_x3, 140)
    if competition == 'other':
        minute = create_matrix(lam1 * 0.021, lam2 * 0.021, 15)
        rest = create_matrix(lam1 * 0.979, lam2 * 0.979, 160)
    elif competition == 'NBA':
        minute = create_matrix(lam1 * 0.015, lam2 * 0.015, 15)
        rest = create_matrix(lam1 * 0.985, lam2 * 0.985, 160)
        if full_time_ou > 250:
            rest = create_matrix_pois(lam1 * 0.985, lam2 * 0.985, 260)

    odds = {}

    k2 = np.triu(final, k=1)
    k1 = np.tril(final, k=-1)

    odds['1 bez prod'] = np.sum(k1)
    odds['2 bez prod'] = np.sum(k2)
    odds['X bez prod'] = 1 - odds['1 bez prod'] - odds['2 bez prod']
    odds.update(fix_margins(final, odds['X bez prod']))

    naj_efik_odds = poeni_cetvrtine(faktor_e, full_time_ou)
    gran_naj_efik, over_naj_efik = egal(naj_efik_odds, '+')
    odds['Ncet |+|'] = {'granica_ou':gran_naj_efik, 'vrednost':over_naj_efik['+']}
    odds['Ncet |-|'] = {'granica_ou':gran_naj_efik, 'vrednost':over_naj_efik['-']}

    naj_neefik_odds = poeni_cetvrtine(faktor_n, full_time_ou)
    gran_naj_neefik, over_naj_neefik = egal(naj_neefik_odds, '+')
    odds['NNcet |+|'] = {'granica_ou':gran_naj_neefik, 'vrednost':over_naj_neefik['+']}
    odds['NNcet |-|'] = {'granica_ou':gran_naj_neefik, 'vrednost':over_naj_neefik['-']}

    perc, change = 0, False

    if model == 1:
        change = True
        if 0.745 < odds['1 bez prod'] <= 0.81:
            perc = odds['2 bez prod'] * lin_inc((0.745, 0), (0.81, 0.04), odds['1 bez prod'])
        elif 0.81 < odds['1 bez prod'] <= 0.84:
            perc = odds['2 bez prod'] * lin_inc((0.81, 0.04), (0.84, 0.25), odds['1 bez prod'])
        elif 0.84 < odds['1 bez prod'] <= 0.88:
            perc = odds['2 bez prod'] * 0.25
        elif 0.88 < odds['1 bez prod'] <= 0.92:
            perc = odds['2 bez prod'] * lin_inc((0.88, 0.25), (0.92, 0.43), odds['1 bez prod'])
        elif odds['1 bez prod'] > 0.92:
            perc = odds['2 bez prod'] * 0.43
        else:
            change = False
    elif model == 2:
        change = True
        if 0.6 < odds['1 bez prod'] <= 0.79:
            # perc = odds['2 bez prod'] * lin_inc((0.6, 0), (0.048, 0.085), odds['1 bez prod'])
            perc = odds['2 bez prod'] * lin_inc((0.6, 0), (0.662, 0.05), odds['1 bez prod']) # 0.048
        elif 0.79 < odds['1 bez prod'] <= 0.84:
            perc = odds['2 bez prod'] * lin_inc((0.79, 0.05), (0.84, 0.34), odds['1 bez prod'])
            # perc = odds['2 bez prod'] * lin_inc((0.6, 0), (0.662, 0.06), odds['1 bez prod'])
        elif 0.84 < odds['1 bez prod'] <= 0.88:
            perc = odds['2 bez prod'] * 0.34
        elif 0.88 < odds['1 bez prod'] <= 0.92:
            perc = odds['2 bez prod'] * lin_inc((0.88, 0.34), (0.92, 0.53), odds['1 bez prod'])
        elif odds['1 bez prod'] > 0.92:
            perc = odds['2 bez prod'] * 0.53
        else:
            change = False
    elif model == 3:
        if 0.6 < odds['1 bez prod']:
            perc = odds['2 bez prod'] * lin_inc((0.6, 0), (0.662, 0.1), odds['1 bez prod'])
            change = True
    elif model == 4:
        if 0.6 < odds['1 bez prod']:
            perc = odds['2 bez prod'] * lin_inc((0.6, 0), (0.662, 0.17), odds['1 bez prod'])
            change = True
    # print perc
    odds['1 bez prod'] += perc
    odds['2 bez prod'] -= perc
    odds['KI 1'] = odds['1 bez prod'] + odds['X bez prod'] / 2
    odds['KI 2'] = odds['2 bez prod'] + odds['X bez prod'] / 2

    fix(np.tril(first, k=-1), np.triu(first, k=1), odds, 'Ipol')
    fix(np.tril(quarter, k=-1), np.triu(quarter, k=1), odds, 'Icet')
    fix(np.tril(minute, k=-1), np.triu(minute, k=1), odds, 'Imin')

    k2_sec = np.sum(np.triu(sec, k=1))
    k1_sec = np.sum(np.tril(sec, k=-1))
    odds['DP 1'] = odds['Ipol 1'] * k1_sec
    odds['DP 2'] = odds['Ipol 2'] * k2_sec

    odds.update(prelazi_prvi(first, sec, 80, odds['X bez prod'], name='PK'))
    odds.update(prelazi_prvi(quarter, quarterx3, 60, odds['X bez prod'], name='CK'))
    odds.update(prelazi_prvi(minute, rest, 15, odds['X bez prod'], name='MK'))
    perc_pol, perc_prelazi, perc_dp, perc_prelazi_2 = 0, 0, 0, 0
    if change:
        if model == 2:
            perc_pol = odds['Ipol 2'] * lin_inc((0.6, 0), (0.662, 0.02), odds['1 bez prod'])
            perc_prelazi = odds['PK 2-2'] * lin_inc((0.6, 0), (0.662, 0.05), odds['1 bez prod'])
            perc_prelazi_2 = odds['PK 1-2'] * lin_inc((0.6, 0), (0.662, 0.05), odds['1 bez prod'])
            perc_dp = odds['DP 2'] * lin_inc((0.6, 0), (0.662, 0.05), odds['1 bez prod'])
        if model == 3:
            perc_pol = odds['Ipol 2'] * lin_inc((0.6, 0), (0.662, 0.04), odds['1 bez prod'])
            perc_prelazi = odds['PK 2-2'] * lin_inc((0.6, 0), (0.662, 0.09), odds['1 bez prod'])
            perc_prelazi_2 = odds['PK 1-2'] * lin_inc((0.6, 0), (0.662, 0.05), odds['1 bez prod'])
            perc_dp = odds['DP 2'] * lin_inc((0.6, 0), (0.662, 0.09), odds['1 bez prod'])
        if model == 4:
            perc_pol = odds['Ipol 2'] * lin_inc((0.6, 0), (0.662, 0.09), odds['1 bez prod'])
            perc_prelazi = odds['PK 2-2'] * lin_inc((0.6, 0), (0.662, 0.12), odds['1 bez prod'])
            perc_prelazi_2 = odds['PK 1-2'] * lin_inc((0.6, 0), (0.662, 0.05), odds['1 bez prod'])
            perc_dp = odds['DP 2'] * lin_inc((0.6, 0), (0.662, 0.12), odds['1 bez prod'])

    odds['Prk DA'] = odds['PK 1-2'] + odds['PK 2-1']
    odds['Prk NE'] = 1 - odds['Prk DA']
    overs = calc_over(final, n)
    granica_ou, over = egal(overs, '+')
    alternative(odds, 13, granica_ou, overs, ('|+|', '|-|'))

    hends = calc_hend(final)
    gran_hend, hend = egal(hends, 'h1')
    alternative(odds, 13, gran_hend, hends, ('H1', 'H2'))

    mat1 = np.fliplr(np.triu(np.fliplr(final), k=n - granica_ou - 0.5))
    mat2 = np.triu(final, k=gran_hend + 0.5)
    odds['H2&|-|'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou, 'granica_hd': gran_hend}
    mat1 = np.fliplr(np.tril(np.fliplr(final), k=n - granica_ou - 1.5))
    odds['H2&|+|'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou, 'granica_hd': gran_hend}
    mat1 = np.fliplr(np.tril(np.fliplr(final), k=n - granica_ou - 1.5))
    mat2 = np.tril(final, k=gran_hend - 0.5)
    odds['H1&|+|'] = {'vrednost': calc_game(mat1, mat2), 'granica_ou': granica_ou, 'granica_hd': gran_hend}
    odds['H1&|-|'] = {'vrednost': 1 - odds['H2&|-|']['vrednost'] - odds['H2&|+|']['vrednost'] - odds['H1&|+|']['vrednost'], 'granica_ou': granica_ou, 'granica_hd': gran_hend}

    mat1 = np.fliplr(np.triu(np.fliplr(final), k=n - granica_ou - 0.5))
    mat2 = np.tril(final, k=-1)
    odds['1&|-|'] = {'vrednost': calc_game(mat1, mat2) + odds['X bez prod'] / 4, 'granica_ou': granica_ou}
    mat2 = np.triu(final, k=1)
    odds['2&|-|'] = {'vrednost': calc_game(mat1, mat2) + odds['X bez prod'] / 4, 'granica_ou': granica_ou}
    mat1 = np.fliplr(np.tril(np.fliplr(final), k=n - granica_ou - 1.5))
    mat2 = np.tril(final, k=-1)
    odds['1&|+|'] = {'vrednost': calc_game(mat1, mat2) + odds['X bez prod'] / 4, 'granica_ou': granica_ou}
    mat2 = np.triu(final, k=1)
    odds['2&|+|'] = {'vrednost': calc_game(mat1, mat2) + odds['X bez prod'] / 4, 'granica_ou': granica_ou}

    reduce_by_perc(odds, perc, perc_pol, perc_prelazi, perc_dp, perc_prelazi_2)

    gran1, vred1 = find_closest(lam1, final, 'prvi')
    gran2, vred2 = find_closest(lam2, final, 'drugi')
    to_add = {'D |+|': {'granica_ou': gran1, 'vrednost': vred1}, 'D |-|': {'granica_ou': gran1, 'vrednost': 1 - vred1},
              'G |+|': {'granica_ou': gran2, 'vrednost': vred2}, 'G |-|': {'granica_ou': gran2, 'vrednost': 1 - vred2}}

    odds.update(to_add)

    turned = np.fliplr(first)
    turned_sec = np.fliplr(sec)

    odds['VP I=II'], odds['VP I>II'] = 0, 0
    for i in range(-turned.shape[0], turned.shape[0]):
        odds['VP I>II'] += np.sum(np.diag(turned, i)) * np.sum(np.triu(turned_sec, i + 1))
        odds['VP I=II'] += np.sum(np.diag(turned, i)) * np.sum(np.diag(turned_sec, i))
    odds['VP I<II'] = 1 - odds['VP I=II'] - odds['VP I>II']
    if nuliranje:
        odds['VP I>II'], odds['VP I<II'], odds['VP I=II'] = 0, 0, 0

    period(first, {'hend': 'HP', 'rest': 'Ipol'}, odds, lam1_first, lam2_first, 80, 'p', all=True)
    period(quarter, {'hend': 'HC', 'rest': 'Icet'}, odds, lam1_quarter, lam2_quarter, 60, 'c', all=True)
    if competition == 'other':
        period(minute, {'hend': 'HM', 'rest': 'Imin'}, odds, lam1 * 0.021, lam2 * 0.021, 15, 'm', all=False)
    elif competition == 'NBA':
        period(minute, {'hend': 'HM', 'rest': 'Imin'}, odds, lam1 * 0.015, lam2 * 0.015, 15, 'm', all=False)

    gran_oba, otp = both_teams(final)
    odds['OTP|+|'] = {'vrednost': otp['over'], 'granica_ou': gran_oba}
    odds['OTP|-|'] = {'vrednost': otp['under'], 'granica_ou': gran_oba}
    odds['Par'], odds['Nepar'] = 0.5, 0.5
    prelazi_over(odds, '')
    prelazi_over(odds, 'C')

    odds['nc2+'] = 0
    for i in range(60):
        clan = (np.sum(np.diag(quarter, k=-i)) + np.sum(np.diag(quarter, k=i)))
        odds['nc2+'] += clan ** 2

    rest = 1 - odds['nc2+']
    fakt1, fakt2, fakt3, fakt4 = pol * cet, pol * (1 - cet), (1 - pol) * (1 - cet), (1 - pol) * cet
    odds['ncIcet'], odds['ncIIcet'], odds['ncIIIcet'], odds['ncIVcet'] = fakt1 * rest, fakt2 * rest, fakt3 * rest, fakt4 * rest
    
    clone_correction(odds, 'H2', 'H1', 1.05), clone_correction(odds, 'H21', 'H11', 1.05), clone_correction(odds, 'H22', 'H12', 1.05)
    clone_correction(odds, 'H112', 'H212', 1.02), clone_correction(odds, 'H111', 'H211', 1.02), clone_correction(odds, 'H110', 'H210', 1.02)
    clone_correction(odds, 'H110', 'H210', 1.02), clone_correction(odds, 'H19', 'H29', 1.02)
    clone_correction(odds, 'H23', 'H13', 1.03), clone_correction(odds, 'H24', 'H14', 1.02), clone_correction(odds, 'H25', 'H15', 1.01)
    
    for key in odds:
        if not isinstance(odds[key], dict):
            vrednost = odds[key]
            odds[key] = {'granica_hd': None, 'granica_ou': None, 'vrednost':vrednost}
            pass
        else:
            if 'granica_hd' not in odds[key]:
                odds[key]['granica_hd'] = None
            if 'granica_ou' not in odds[key]:
                odds[key]['granica_ou'] = None

    if reverse:
        odds = invert(odds)

    return odds


def invert(odds):
    for key in odds:
        if key in mapping.keys():
            odds[mapping[key]], odds[key] = odds[key], odds[mapping[key]]
    return odds


if __name__ == '__main__':
    # Primeri pozivanja funkcije
    odds1 = real_time_calculation(240.5, -4.5, model=4, competition='NBA')
    print(len(odds1.keys()) ,odds1.keys())
    '''
    full_time_ou = 310.5
    full_time_hd = -4.5
    '''
    odds2 = real_time_calculation(155.5, 2.5, model=2, competition='other')
    '''
    full_time_ou = 155.5
    full_time_hd = 2.5
    '''