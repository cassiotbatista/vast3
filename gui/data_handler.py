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

blob_count  = 0
lemma_count = 0

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
            blacklist.append(user.strip('@').rstrip())
    return blacklist

def get_keywords():
    wordlist = []
    with open(config.KEYPREFS_FILE) as f:
        for line in f:
            prefix, words = line.split(':')
            wordlist.append(prefix)
    return wordlist

def check_spell(text):
    global blob_count
    blob_count += 1
    blob = TextBlob(text).correct()
    sys.stdout.write('\r\t\t\t\t\t\t\t\t%05d' % blob_count)
    sys.stdout.flush()
    return blob.raw

def lemmatize(text):
    global lemma_count
    lemma_count += 1
    tokens = [lemmatizer.lemmatize(lemmatizer.lemmatize(word, 'n'), 'v') \
            for word in tokenizer.tokenize(text)]
    sys.stdout.write('\r\t\t\t\t\t\t\t\t%05d' % lemma_count)
    sys.stdout.flush()
    return ' '.join(tokens)

def normalise(data):
    data.message = data.message.str.replace(r'[=!?,.;\-$"\*/)(><\']', ' ')
    data.message = data.message.str.replace(r'([qwyuiahjkxv])\1+', r'\1')
    data.message = data.message.str.replace(r'(.)\1{2,}',r'\1\1')
    return data

def stringify(data):
    for col in data.columns:
        if col != 'time':
            data[col] = data[col].apply(str)
    return data

def lowercase(data):
    for col in data.columns:
        if col != 'time':
            data[col] = data[col].str.lower()
    return data

def preprocess(data):
    cprint('%s: converting message column to str' % TAG, 
            'green', attrs=['bold'])
    data = stringify(data)
    cprint('%s: lowercasing text cols' % TAG, 
            'green', attrs=['bold'])
    data = lowercase(data)
    cprint('%s: replacing wrong words' % TAG, 
            'green', attrs=['bold'])
    for wrong, correct in get_replace_rules():
        data.message = data.message.str.replace(wrong, correct)
    cprint('%s: normalising chars' % TAG, 
            'green', attrs=['bold'])
    data = normalise(data)
    if config.DO_BLACK_SELECT:
        cprint('%s: selecting tweets by username' % TAG, 
                'green', attrs=['bold'])
        blackgex = '|'.join(get_user_blacklist())
        data = data.loc[data.account.str.contains(blackgex) == False]
    if config.DO_KW_SELECT:
        cprint('%s: selecting tweets by keyword' % TAG, 
                'green', attrs=['bold'])
        wordgex = '|'.join(get_keywords())
        data = data.loc[data.message.str.contains(wordgex)]
    if config.DO_SPELLCHECK:
        cprint('%s: checking spell (it may take a while...) ' % TAG, 
                'green', attrs=['bold', 'blink'], end=' ')
        start = time.time()
        data.message = data.message.apply(check_spell)
        end = time.time()
        print('\t(%.2f seconds)' % (end - start))
    if config.DO_LEMMATIZE:
        cprint('%s: lemmatizing verbs and nouns (it may take a while...)' % TAG, 
                'green', attrs=['bold', 'blink'], end=' ')
        start = time.time()
        data.message = data.message.apply(lemmatize)
        end = time.time()
        print('\t(%.2f seconds)' % (end - start))
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
    cprint('%s: data written to "%s"' % (TAG, config.DATA_PROC_CSVFILE), 
            'green', attrs=['bold'])
