#converts files from here: http://geocoder.ca/?freedata=1

import fileinput

ca_states = {
    "AB": "Alberta",
    "BC": "British",
    "MB": "Manitoba",
    "NB": "New",
    "NL": "Newfoundland",
    "NT": "Northwest",
    "NS": "Nova",
    "NU": "Nunavut",
    "ON": "Ontario",
    "PE": "Prince",
    "QC": "Quebec",
    "SK": "Saskatchewan",
    "YT": "Yukon"
    }

for line in fileinput.input():
    s = line.split(',')
    try:
        print "%s,%s,%s,%s,%s,%s" % (s[0],s[4].strip('\n'),s[1],s[2],s[3],ca_states[s[4].strip('\n')])
    except KeyError:
        pass

