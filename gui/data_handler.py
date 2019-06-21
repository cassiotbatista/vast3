#!/usr/bin/env python3
#
# author: june 2019
# cassio batista - cassio.batista.13@gmail.com

import pandas as pd
import numpy as np

DATA_CSVFILE = '../MC3/data/YInt.csv'
REPLACE_FILE = '../src/replace.txt'

def get_replace_rules():
    rules = {}
    with open(REPLACE_FILE) as f:
        for line in f:
            key, value = line.split()
            rules[key] = value
    return rules

def load_data():
    data = pd.read_csv(DATA_CSVFILE, parse_dates=['time'])
    mapping_rules = get_replace_rules()
    for i in range(len(data['message'])):
        
    #for wrong, correct in mapping_rules.items():
        

load_data()
