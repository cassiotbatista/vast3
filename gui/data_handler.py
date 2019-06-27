#!/usr/bin/env python3
#
# author: june 2019
# cassio batista - cassio.batista.13@gmail.com

import sys
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None) 

from termcolor import cprint

DATA_CSVFILE = '../MC3/data/YInt.csv'
REPLACE_FILE = '../src/replace.txt'
USELESS_FILE = '../src/w_useless.txt'
USEFUL_FILE  = '../src/w_useful.txt'
TAG = 'DH'

def get_replace_rules():
    rules = {}
    with open(REPLACE_FILE) as f:
        for line in f:
            key, value = line.split()
            rules[key] = value
    return rules

def get_useless_words():
    wordlist = []
    with open(USELESS_FILE) as f:
        for line in f:
            word, freq = line.split(':')
            wordlist.append(word)
    return wordlist

def get_useful_words():
    wordlist = []
    with open(USEFUL_FILE) as f:
        for line in f:
            word, freq = line.split(':')
            wordlist.append(word)
    return wordlist

def preprocess(data):
    mapping_rules = get_replace_rules()
    cprint('%s: replacing wrong words' % TAG, 'green', attrs=['bold'])
    for wrong, correct in mapping_rules.items():
        data['message'] = data['message'].str.replace(wrong, correct)
    cprint('%s: lowercasing text cols' % TAG, 'green', attrs=['bold'])
    for col in data.columns:
        if col != 'time':
            data[col] = data[col].str.lower()
    return data

def load_data():
    cprint('%s: loading data' % TAG, 'green', attrs=['bold'])
    data = pd.read_csv(DATA_CSVFILE, parse_dates=['time'])
    return preprocess(data)
