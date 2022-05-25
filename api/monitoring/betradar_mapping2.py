import json
import os
from decimal import Decimal

# betradar=""
# with open('betradar.json') as json_file:
#     betradar = json.load(json_file)['RECORDS']


def extract1X2(outcomeToExtract, outcomes):
    niz = outcomes.split(",")
    val = [x for x in niz if x.startswith(outcomeToExtract)]
    if len(val)!=0:
        rez = val[0].split("_")[2]
    else:
        rez = None
    return rez 

def extractTotal(outcomes):
    niz = outcomes.split(",")
    available_handicaps = []
    for el in niz:
        if el.startswith("UNDER_Total Spreads"):
            available_handicaps.append(el.split("_")[2])
    available_handicaps = filter(lambda x:float(x)%0.5==0 and float(x)>=2.5 and not float(x).is_integer(), available_handicaps)
    sorted_handicaps = sorted(available_handicaps, key=lambda x:float(x))
    if len(sorted_handicaps)==0:
        return {"total":None, "prob":None}
    handicap = float(sorted_handicaps[0])
    return {"total":handicap, "prob":list(filter(lambda x:x.startswith("UNDER_Total Spreads_"+str(handicap)), niz))[0].split("_")[3]}

def extractHandicap(outcomes):
    niz = outcomes.split(",")
    available_handicaps = []
    for el in niz:
        if el.startswith("H1_Goal Spreads"):
            available_handicaps.append(el.split("_")[2])
    available_handicaps = filter(lambda x:float(x)%0.5==0 and not float(x).is_integer(), available_handicaps)
    sorted_handicaps = sorted(available_handicaps, key=lambda x:float(x))
    if len(sorted_handicaps)==0:
        return {"handicap":None, "prob":None}
    handicap = float(sorted_handicaps[0])
    if handicap == -0.5 and '0.5' in sorted_handicaps:
        handicap=0.5
    is_negative = handicap<0
    if is_negative:
        return {"handicap":handicap, "prob":list(filter(lambda x:x.startswith("H1_Goal Spreads_"+str(handicap)), niz))[0].split("_")[3]}
    else:
        return {"handicap":handicap, "prob":list(filter(lambda x:x.startswith("H2_Goal Spreads_"+str(handicap)), niz))[0].split("_")[3]}



