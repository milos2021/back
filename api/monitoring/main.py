import pandas as pd
import json
import os

from pandas.core.groupby.groupby import GroupBy

mecevi = ""
kvote = ""
lige = ""
with open('mecevi.json') as json_file:
    mecevi = json.load(json_file)['RECORDS']
with open('kvote.json') as json_file:
    kvote = json.load(json_file)['RECORDS']

# mecevidf = pd.DataFrame(mecevi)
# print(mecevidf.head())
# print(mecevidf.columns)
# mecevi_groups = mecevidf.groupby(['sport', 'liga'])

key_list = ['FD', 'KO']
groupedBy = {key: {} for key in key_list}
lige = list(set([e['liga'] for e in mecevi]))
for elem in mecevi:
    if elem['sport'] == 'FD':
        for liga in lige:
            if elem['liga'] in liga and not liga in groupedBy['FD']:
                groupedBy['FD'][liga] = []
    if elem['sport'] == 'KO':
        for liga in lige:
            if elem['liga'] in liga and not liga in groupedBy['KO']:
                groupedBy['KO'][liga] = []

kvote_keys = kvote[0].keys()
for elem in mecevi:
    for gr_lige in groupedBy['FD']:
        if elem['liga'] == gr_lige and elem['sport']=="FD":
            elem['odds']={}
            for kv in kvote_keys:
                elem['odds'][kv]={"production":x[kv] for x in kvote if x['code']==elem['Code']}
            groupedBy['FD'][gr_lige].append(elem)
    for gr_lige in groupedBy['KO']:
        if elem['liga'] == gr_lige and elem['sport']=="KO":
            elem['odds']={}
            for kv in kvote_keys:
                elem['odds'][kv]={"production":x[kv] for x in kvote if x['code']==elem['Code']}
            groupedBy['KO'][gr_lige].append(elem)
with open('data.txt', 'w') as outfile:
    json.dump(groupedBy, outfile)





# betradardf = pd.DataFrame(betradar)
# print(betradardf.head())

# betradardf_groups = betradardf.groupby(['matchId'])
# '''
# for key, group in betradardf_groups:
#     print(key, group)
# print(betradardf_groups)
# '''
# print(betradardf.index)
# betradardf = betradardf.pivot(columns=['betGameOutcome'], values=['prob', 'matchId'])
# print(betradardf.head())






    


