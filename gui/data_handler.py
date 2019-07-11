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
import os

import pandas as pd
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None) 

import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

from termcolor import cprint
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from multiprocessing import cpu_count, Pool
from datetime import datetime, timedelta
from collections import OrderedDict

import time

import config

TAG = 'DH'
TIME_INTERVAL = 1 # in hours please

tokenizer  = WhitespaceTokenizer()
lemmatizer = WordNetLemmatizer()

blob_count  = 0
lemma_count = 0

def set_wcount_time():
    cprint('%s: loading data from "%s"' % (TAG, config.DATA_PROC_CSVFILE), 
            'green', attrs=['bold'])
    data = stringify(pd.read_csv(config.DATA_PROC_CSVFILE, parse_dates=['time']))
    keyclusters = get_synonym_cluster()
    full_time_range = np.arange(
            data.time.iloc[0], 
            data.time.iloc[-1] + timedelta(hours=TIME_INTERVAL, minutes=1), 
            timedelta(hours=TIME_INTERVAL),
            dtype='datetime64[h]')
    wcount_vec = OrderedDict()
    for neigh in config.NEIGHBOURHOODS:
        wcount_vec[neigh] = OrderedDict()
        for cluster in keyclusters:
            word = cluster.split()[0]
            wcount_vec[neigh][word] = np.zeros(len(full_time_range), dtype=np.int16)
    print('counting.......')
    for cluster in keyclusters:
        cluster = cluster.split()
        prefices = tuple([w[:config.PREFIX_LEN+2] for w in cluster])
        chunk_sizes = []
        for i, hour in enumerate(full_time_range[:-1]):
            start_time = full_time_range[i]
            end_time   = full_time_range[i+1]
            chunk      = data[data.time.between(start_time, 
                    end_time, inclusive=False)]
            chunk_sizes.append(chunk.shape[0])
            sys.stdout.write('\r%+10s %s' % (cluster[0], start_time))
            sys.stdout.flush()
            for index, timestamp, location, account, tweet in chunk.itertuples():
                if location.startswith('unk') or location.startswith('<loc') \
                        or location.startswith('wilson'):
                    continue
                for word in tweet.split():
                    if word.startswith(prefices):
                        position = np.where(full_time_range == start_time)[0][0]
                        wcount_vec[location][cluster[0]][position] += 1
        sys.stdout.write('\n')
    print('saindoo')
    df = pd.DataFrame(columns=['location', 'keyword', 'frequency', 'time'])
    for location, value in wcount_vec.items():
        for keyword, vector in value.items():
            for i, frequency in enumerate(vector):
                df = df.append(pd.DataFrame([[location, keyword, frequency,
                    full_time_range[i].tolist().strftime('%d/%m @ %Hh')]],
                        columns=['location', 'keyword', 'frequency', 'time']))
    print('escrevendo')
    with open(config.DATA_HEAT_CSVFILE, 'w') as f:
        df.to_csv(f, index=False, quoting=1)

def get_synonym_cluster():
    with open(config.SYNCLUSTER_FILE) as f:
        clusters = f.read().splitlines()
    return clusters

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

def get_stopwords():
    wordlist = []
    with open(config.STOPWORDS_FILE) as f:
        for word in f:
            wordlist.append(word.rstrip())
    return wordlist

def parallel_spell(data):
    data = data.apply(check_spell)
    return data

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
    replace_rules = [
        (r'[=!?,.;\-$"\*/)(><\']', ' '), # strip non-alphanum chars except @#:
        (r'([qwyuiahjkxv])\1+', r'\1'),  # remove selected chars repeated
        (r'(.)\1{2,}',r'\1\1'),          # set max num of char repetition to 2
        #(r'\b\w{0,1}\b', ''),
        ('re:', 'reply:'),               # FIXME gambiarra 1/2
        #(r'\b[^\W:]{0,1}\b', ''),
        (r'\b\w{0,2}\b', ''),            # strip words with length less then 3
        #(r'(\w)\1+', r'\1'),
        #(r'\b(\w+)( \1\b)+', r'\1'),
        ('reply:', 're:'),               # FIXME gambiarra 2/2
    ]
    for patt, repl in replace_rules:
        data.message = data.message.str.replace(patt, repl)
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

# NOTE that will use all CPU cores
def parallelize(data, func):
        data_split = np.array_split(data, cpu_count())
        pool = Pool(cpu_count())
        data = pd.concat(pool.map(func, data_split))
        pool.close()
        pool.join()
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
        keygex = '|'.join(get_keywords())
        data = data.loc[data.message.str.contains(keygex)]
    if config.DO_SW_SELECT:
        cprint('%s: excluding tweets with stopwords' % TAG, 
                'green', attrs=['bold'])
        stopgex = '|'.join(get_stopwords())
        data = data.loc[data.message.str.contains(stopgex) == False]
    if config.DO_SPELLCHECK:
        cprint('%s: checking spell (it may take a while...) ' % TAG, 
                'green', attrs=['bold', 'blink'], end=' ')
        start = time.time()
        data.message = parallelize(data.message, parallel_spell)
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

def load_heatmap_data():
    cprint('%s: loading data from "%s"' % (TAG, config.DATA_HEAT_CSVFILE), 
            'green', attrs=['bold'])
    return pd.read_csv(config.DATA_HEAT_CSVFILE)

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
