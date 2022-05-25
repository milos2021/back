

mapping_base = {'KI 1': 'KI 2', 'DS 1X': 'DS X2', 'XNB 1': 'XNB 2', 'H1': 'H2', '1H1': '1H2', '2H1': '2H2', '1&|-|': '2&|-|',
				'1&|+|': '2&|+|', 'H1&|-|': 'H2&|-|', 'H1&|+|': 'H2&|+|', 'Ipol 1': 'Ipol 2', 'Ipol H1': 'Ipol H2', 'IIpol 1': 'IIpol 2',
				'IIpol H1': 'IIpol H2', 'PK 1-1': 'PK 2-2', 'PK 1-X': 'PK 2-X', 'PK 1-2': 'PK 2-1', 'PK X-1': 'PK X-2',
				'1-1&|-|': '2-2&|-|', '1-1&|+|': '2-2&|+|', '1-2&|-|': '2-1&|-|', '1-2&|+|': '2-1&|+|', 'DP 1': 'DP 2', 'D |-|': 'G |-|',
				'D |+|': 'G |+|', 'Ipol D|-|': 'Ipol G|-|', 'Ipol D|+|': 'Ipol G|+|', 'IIpol D|-|': 'IIpol G|-|', 'IIpol D|+|': 'IIpol G|+|'}


base_to_name = {u'OT|+|PP': u'Ipol OTP|+|', u'1H2': u'1H2', u'1H1': u'1H1', u'2TM-DP': u'IIpol G|-|', u'OT|-|': u'OTP |-|',
				u'1|-|': u'1|-|', u'OT|+|DP': u'IIpol OTP|+|', u'1TM+PP': u'Ipol D|+|', u'W2': u'XNB 2', u'W1': u'XNB 1', u'2TM+PP': u'Ipol G|+|',
				u'1TM-DP': u'IIpol D|-|', 'X-1': 'PK X-1', 'X-2': 'PK X-2', u'2TM-PP': u'Ipol G|-|', u'|+|': u'|+|', u'2H1': u'2H1', u'PX': u'Ipol X',
				u'2H2': u'2H2', '1-1': 'PK 1-1', u'2&+': u'2&|+|', u'HDP1': u'IIpol H1', u'HDP2': u'IIpol H2', u'SH+': u'IIpol |+|', u'SH-': u'IIpol |-|', 
				u'2&-': u'2&|-|', u'P2': u'Ipol 2', u'P1': u'Ipol 1', u'OT|-|DP': u'IIpol OTP|-|', u'EV': u'Par', u'H2': u'H2', u'H1': u'H1', 'X-X': 'PK X-X',
				u'I>II': u'VG I>II', u'2|-|': u'2|-|', 'D12': 'DS 12', u'K2': u'KI 2', u'K1': u'KI 1', u'2TM+DP': u'IIpol G|+|', u'2-1&-': u'2-1&|-|',
				u'2-1&+': u'2-1&|+|', '2-X': 'PK 2-X', u'PD2': u'prolaz 2', u'PD1': u'prolaz 1', u'|-|': u'|-|', u'ODD': u'Nepar', '2-2': 'PK 2-2',
				'2-1': 'PK 2-1', u'2-2&-': u'2-2&|-|', u'H2&-': u'H2&|-|', u'FH+': u'Ipol |+|', u'H2&+': u'H2&|+|', u'I=II': u'VG I=II', 'D1X': 'DS 1X',
				u'KX': u'KI X', u'OT|-|PP': u'Ipol OTP|-|', u'2|+|': u'2|+|', 'DX2': 'DS X2', u'DPX': u'IIpol X', u'1TM+DP': u'IIpol D|+|',
				u'DW2': u'DP 2', '1-X': 'PK 1-X', u'DW1': u'DP 1', u'HP2': u'Ipol H2', u'HP1': u'Ipol H1', u'1TM-PP': u'Ipol D|-|', u'1&-': u'1&|-|',
				u'OT|+|': u'OTP |+|', u'1&+': u'1&|+|', u'I<II': u'VG I<II', u'2TM-': u'G |-|', u'1|+|': u'1|+|', '1-2': 'PK 1-2', u'2TM+': u'G |+|',
				u'1-2&-': u'1-2&|-|', u'1-2&+': u'1-2&|+|', u'FH-': u'Ipol |-|', u'1TM-': u'D |-|', u'2-2&+': u'2-2&|+|', u'DP2': u'IIpol 2', u'DP1': u'IIpol 1',
				u'1TM+': u'D |+|', u'H1&+': u'H1&|+|', u'1-1&+': u'1-1&|+|', u'1-1&-': u'1-1&|-|', u'H1&-': u'H1&|-|'}


name_to_base = {base_to_name[key]: key for key in base_to_name}


def generate_mapping():
      mapping = {}
      for key in mapping_base:
            mapping[name_to_base[key]] = name_to_base[mapping_base[key]]
      return mapping

mapping = generate_mapping()