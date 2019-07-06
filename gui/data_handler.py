#!/usr/bin/env python3
#
# VAST Challenge 2019: Disaster at St. Himark!
# https://vast-challenge.github.io/2019/index.html
#
# Federal University of Pará (UFPA)
#
# author: june 2019
# cassio batista - cassio.batista.13@gmail.com
# edwin jueda    - 
# erick campos   - 

import sys
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None) 

from termcolor import cprint
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

import time

import config

TAG = 'DH'
tokenizer  = WhitespaceTokenizer()
lemmatizer = WordNetLemmatizer()

blob_count = 0

def get_replace_rules():
    rules = {}
    with open(config.REPLACE_FILE) as f:
        for line in f:
            key, value = line.split()
            rules[key] = value
    return rules.items()

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

def get_user_blacklist():
    blacklist = []
    with open(config.BLACKLIST_FILE) as f:
        for user in f:
            blacklist.append(user.strip('@'))
    return blacklist

def get_keywords():
    wordlist = []
    with open(config.KEYPREFS_FILE) as f:
        for line in f:
            prefix, words = line.split(':')
            wordlist.append(prefix)
    return wordlist

def lemmatize(text, pos):
    tokens = [lemmatizer.lemmatize(word, pos=pos) \
            for word in tokenizer.tokenize(text)]
    return ' '.join(tokens)

def check_spell(text):
    global blob_count
    sys.stdout.write('\r%06d' % blob_count)
    sys.stdout.flush()
    blob_count += 1
    blob = TextBlob(text).correct()
    return blob.raw

def reduce_lengthening(data):
    data['message'] = data.message.str.replace(r'(.)\1{2,}',r'\1\1')
    return data

def normalise(data):
    data['message'] = data.message.str.replace(r'[#!?,.;\-$"\*/)(><\']', ' ')
    data['message'] = data.message.str.replace(r'([qwyuiahjkxv])\1+', r'\1')
    return data

def lowercase(data):
    for col in data.columns:
        if col != 'time':
            data[col] = data[col].str.lower()
    return data

def preprocess(data):
    cprint('%s: converting message column to str' % TAG, 'green', attrs=['bold'])
    data['message'] = data.message.apply(str)
    cprint('%s: lowercasing text cols' % TAG, 'green', attrs=['bold'])
    data = lowercase(data)
    if config.DO_BLACK_SELECT:
        cprint('%s: selecting tweets by username' % TAG, 'green', attrs=['bold'])
        blackgex = '|'.join(get_user_blacklist())
        data = data[~data['account'].str.contains(blackgex)]
    cprint('%s: replacing wrong words' % TAG, 'green', attrs=['bold'])
    for wrong, correct in get_replace_rules():
        data['message'] = data['message'].str.replace(wrong, correct)
    cprint('%s: normalising chars' % TAG, 'green', attrs=['bold'])
    data = normalise(data)
    cprint('%s: removing chars redundancy' % TAG, 'green', attrs=['bold'])
    data = reduce_lengthening(data)
    if config.DO_SPELLCHECK:
        cprint('%s: checking spell (it may take a while...) ' % TAG, 
                'green', attrs=['bold', 'blink'])
        data['message'] = data.message.apply(check_spell)
    if config.DO_LEMMATIZE:
        cprint('%s: lemmatizing words twice (it may take a while...)' % TAG, 
                'green', attrs=['bold', 'blink'])
        data['message'] = data.message.apply(lemmatize, args=('n'))
        data['message'] = data.message.apply(lemmatize, args=('v'))
    if config.DO_KW_SELECT:
        cprint('%s: selecting tweets by keyword' % TAG, 'green', attrs=['bold'])
        wordgex = '|'.join(get_keywords())
        data = data[data['message'].str.contains(wordgex)]
    return data

def load_data():
    cprint('%s: loading data from "%s"' % (TAG, config.DATA_PROC_CSVFILE), 
            'green', attrs=['bold'])
    return pd.read_csv(config.DATA_PROC_CSVFILE, parse_dates=['time'])

if __name__=='__main__':
    cprint('%s: loading data from "%s"' % (TAG, config.DATA_SRC_CSVFILE), 
            'green', attrs=['bold'])
    data = preprocess(pd.read_csv(config.DATA_SRC_CSVFILE, parse_dates=['time']))
    with open(config.DATA_PROC_CSVFILE, 'w') as f:
        data.to_csv(f, index=False, quoting=1)
