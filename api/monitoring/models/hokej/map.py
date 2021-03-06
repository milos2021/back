mapping = {'KI 1': 'KI 2', 'DS 1X': 'DS X2', 'XNB 1': 'XNB 2', 'HP1': 'HP2', 'HH1': 'HH2', 'D 0' : 'G 0', 'D 0-1': 'G 0-1', 'D 0-2': 'G 0-2',
                  'D 0-3': 'G 0-3', 'D 1+': 'G 1+', 'D 2+': 'G 2+', 'D 3+': 'G 3+', 'D 4+': 'G 4+', 'D 1-2': 'G 1-2', 'D 1-3': 'G 1-3',
                  'D 2-3': 'G 2-3', 'D 2-4': 'G 2-4', 'SP 1': 'SP 2', 'I 1X': 'I X2', '1&GG' : '2&GG', 'D I0': 'G I0', 'D I0-1': 'G I0-1',
                  'D I0-2': 'G I0-2', 'D I1+': 'G I1+', 'D I2+': 'G I2+', 'D I3+': 'G I3+', 'D I1-2': 'G I1-2', 'D I2-3': 'G I2-3', 
                  'PK 1-1': 'PK 2-2', 'PK 1-X': 'PK 2-X', 'PK 1-2': 'PK 2-1', 'PK X-1': 'PK X-2', '1&0-3': '2&0-3', '1&0-4': '2&0-4',
                  '1&0-5': '2&0-5', '1&3+': '2&3+', '1&4+': '2&4+', '1&5+': '2&5+', '1&6+': '2&6+', '1-1&3+': '2-2&3+', '1-1&0-3': '2-2&0-3',
                  '1-1&4+': '2-2&4+', '1-1&5+': '2-2&5+', '1-1&GG': '2-2&GG', '1-1&I2+': '2-2&I2+', '1-1&IGG': '2-2&IGG', '1-1&D3+': '2-2&G3+',
                  '1-1&I0-1': '2-2&I0-1', '1&I0-1': '2&I0-1', '1&I2+': '2&I2+', '1&IGG': '2&IGG', '1&D3+': '2&G3+', '1&I1+': '2&I1+',
                  '1-1&0-4': '2-2&0-4', '1-1&0-5': '2-2&0-5', '1-1&6+': '2-2&6+', 'Iper 1': 'Iper 2'}


base_to_code = {u'GH3+': u'D 3+', u'2&GG': u'2&GG', u'GAP2+': u'G I2+', u'2&G0-5': u'2&0-5', u'G5-7': u'UG 5-7', u'G5-6': u'UG 5-6', 
            u'G5-8': u'UG 5-8', u'1TM12': u'D 1-2', u'1TM13': u'D 1-3', u'2-2&4+': u'2-2&4+', u'GG&3+': u'GG&3+', u'1&3+': u'1&3+', 
            u'G6-8': u'UG 6-8', u'1-1&5+': u'1-1&5+', u'G6-7': u'UG 6-7', u'GH2+': u'D 2+', u'1-1&6+': u'1-1&6+', u'G5+': u'UG 5+', 
            u'GAP3+': u'G I3+', u'FG1': u'PG 1', u'FG2': u'PG 2', u'HS2': u'D 0', u'GA01': u'G 0-1', u'HS1': u'D 1+', u'GH23': u'D 2-3', 
            u'GN': u'NG', u'nGG2+': u'2NG', u'GH24': u'D 2-4', u'2-2&IGG': u'2-2&IGG', u'GG&4+': u'GG&4+', u'GA24': u'G 2-4', u'GG': u'GG',
            u'1-1&D3+': u'1-1&D3+', u'W2': u'XNB 2', u'W1': u'XNB 1', u'1&I1+': u'1&I1+', u'G2-4': u'UG 2-4', u'G2-5': u'UG 2-5',
            u'G2-6': u'UG 2-6', u'1&G0-5': u'1&0-5', u'1&G0-4': u'1&0-4', u'G2-3': u'UG 2-3', u'GH01': u'D 0-1', u'GHP1+': u'D I1+',
            u'2&3+': u'2&3+', 'D1X': 'DS 1X', u'G4+': u'UG 4+', u'2TM4+': u'G 4+', u'2&4+': u'2&4+', u'2-2&I2+': u'2-2&I2+', u'GHP12': u'D I1-2', 
            u'2-2&6+': u'2-2&6+', 'X-1': 'PK X-1', 'X-2': 'PK X-2', u'1-1&G05': u'1-1&0-5', u'GG&5+': u'GG&5+', u'2&G0-3': u'2&0-3', 
            u'2&G0-4': u'2&0-4', u'2GG&6+': u'2GG&6+', u'1-1&G03': u'1-1&0-3', u'GH34': u'D 3-4', 'PX': 'Iper X', u'1&G0-3': u'1&0-3', 
            u'G2+': u'UG 2+', u'2-2&I0-1': u'2-2&I0-1', u'DIX2': u'I X2', 'P2': 'Iper 2', 'P1': 'Iper 1', u'GA34': u'G 3-4', u'GA2+': u'G 2+', 
            u'2&G3+': u'2&G3+', u'G7+': u'UG 7+', u'I34': u'UG I3-4', u'I3+': u'UG I3+', u'GHP02': u'D I0-2', u'1TM4+': u'D 4+', u'GHP01': u'D I0-1', 
            u'GA23': u'G 2-3', u'GG2+': u'2GG', u'I4+': u'UG I4+', u'2&IGG': u'2&IGG', u'2-2&G3+': u'2-2&G3+', u'1&GG': u'1&GG', u'2-2&G05': u'2-2&0-5', 
            u'X-X': u'PK X-X', u'GG&6+': u'GG&6+', u'2&5+': u'2&5+', u'G6+': u'UG 6+', u'GA3+': u'G 3+', u'2&I2+': u'2&I2+', 'D12': 'DS 12', 
            u'I23': u'UG I2-3', u'I24': u'UG I2-4', u'2-2&G04': u'2-2&0-4', u'K2': u'KI 2', u'K1': u'KI 1', u'I2+': u'UG I2+', u'1&6+': u'1&6+', 
            u'nGG3+': u'3NG', u'G4-6': u'UG 4-6', u'G4-7': u'UG 4-7', u'G4-5': u'UG 4-5', u'GHP3+': u'D I3+', u'3HW2': u'HH2', u'1-1&I2+': u'1-1&I2+', 
            u'1-1&3+': u'1-1&3+', u'GG3+': u'3GG', u'GAP0': u'G I0', u'DI1X': u'I 1X', '2-X': 'PK 2-X', u'G0-2': u'UG 0-2', u'G0-3': u'UG 0-3', 
            u'G0-1': u'UG 0-1', u'G0-6': u'UG 0-6', u'G0-7': u'UG 0-7', u'G0-4': u'UG 0-4', u'G0-5': u'UG 0-5', u'GAP23': u'G I2-3', 
            u'1-1&IGG': u'1-1&IGG', u'2-2&G03': u'2-2&0-3', '2-2': 'PK 2-2', u'AS2': u'G 0', u'AS1': u'G 1+', '2-1': 'PK 2-1', u'GG1': u'IGG', 
            u'2TM13': u'G 1-3', u'2TM12': u'G 1-2', u'DI12': u'I 12', u'1&IGG': u'1&IGG', u'I13': u'UG I1-3', u'I12': u'UG I1-2', u'1&5+': u'1&5+', 
            u'2&I0-1': u'2&I0-1', u'I1+': u'UG I1+', u'2-2&3+': u'2-2&3+', u'GHP2+': u'D I2+', u'2&6+': u'2&6+', u'2-2&GG': u'2-2&GG', u'G3-5': u'UG 3-5', 
            u'G3-4': u'UG 3-4', u'G3-6': u'UG 3-6', u'1-1&GG': u'1-1&GG', u'KX': u'KI X', u'2GG&5+': u'2GG&5+', u'2&I1+': u'2&I1+', u'2TM02': u'G 0-2', 
            u'2TM03': u'G 0-3', u'1&D3+': u'1&D3+', 'DX2': 'DS X2', u'2HW2': u'HP2', u'2HW1': u'HP1', u'GHP23': u'D I2-3', '1-X': 'PK 1-X', 
            u'1&I0-1': u'1&I0-1', u'GAP1+': u'G I1+', u'GAP01': u'G I0-1', u'I0': u'UG I0', u'GAP02': u'G I0-2', u'1&I2+': u'1&I2+', u'2-2&5+': u'2-2&5+', 
            u'1-1&G04': u'1-1&0-4', '1-1': 'PK 1-1', '1-2': 'PK 1-2', u'1-1&4+': u'1-1&4+', u'3HW1': u'HH1', u'G3+': u'UG 3+', u'1TM03': u'D 0-3', 
            u'1TM02': u'D 0-2', u'GHP0': u'D I0', u'GN1': u'ING', u'G7-8': u'UG 7-8', u'GAP12': u'G I1-2', u'1&4+': u'1&4+', u'G8+': u'UG 8+', 
            u'I02': u'UG I0-2', u'I03': u'UG I0-3', u'I01': u'UG I0-1', u'SW1': u'SP 1', u'1-1&I0-1': u'1-1&I0-1', u'SW2': u'SP 2'}

