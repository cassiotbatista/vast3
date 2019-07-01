#!/usr/bin/env python3
#
# VAST Challenge 2019: Disaster at St. Himark!
# https://vast-challenge.github.io/2019/index.html
#
# Federal University of Pará (UFPA)
#
# author: june 2019
# cassio batista - cassio.batista.13@gmail.com
# edwin jueda - 
# erick campos - 

import sys
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None) 

from termcolor import cprint
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer

import config

TAG = 'DH'
tokenizer  = WhitespaceTokenizer()
lemmatizer = WordNetLemmatizer()

def get_replace_rules():
    rules = {}
    with open(config.REPLACE_FILE) as f:
        for line in f:
            key, value = line.split()
            rules[key] = value
    return rules

def get_useless_words():
    wordlist = []
    with open(config.USELESS_FILE) as f:
        for line in f:
            word, freq = line.split(':')
            wordlist.append(word)
    return wordlist

def get_useful_words():
    wordlist = []
    with open(config.USEFUL_FILE) as f:
        for line in f:
            word, freq = line.split(':')
            wordlist.append(word)
    return wordlist

def lemmatize(text):
    if isinstance(text, str):
        tokens = [lemmatizer.lemmatize(word) for word in tokenizer.tokenize(text)]
        return ' '.join(tokens)

def preprocess(data):
    mapping_rules = get_replace_rules()
    cprint('%s: replacing wrong words' % TAG, 'green', attrs=['bold'])
    for wrong, correct in mapping_rules.items():
        data['message'] = data['message'].str.replace(wrong, correct)
    cprint('%s: lowercasing text cols' % TAG, 'green', attrs=['bold'])
    for col in data.columns:
        if col != 'time':
            data[col] = data[col].str.lower()
    cprint('%s: lemmatizing words twice (this step may take a while...)' % TAG, 
            'green', attrs=['bold', 'blink'])
    data['message'] = data.message.apply(lemmatize)
    return data

def load_data():
    cprint('%s: loading data' % TAG, 'green', attrs=['bold'])
    data = pd.read_csv(config.DATA_CSVFILE, parse_dates=['time'])
    return preprocess(data)
