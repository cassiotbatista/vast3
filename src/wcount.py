#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# author: jun 2019
# Cassio Batista - cassio.batista.13@gmail.com

import sys
import os

import pandas as pd
import numpy as np
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None)  

#pd.set_option('display.max_rowwidth', -1)
pd.set_option('display.max_rows', None)  

import matplotlib.pyplot as plt
plt.rcParams['axes.axisbelow'] = True

AVOID_CONTAINS = [
    '\''
]

AVOID_RADICALS = [
    'some', 'they', 'anyo', 'that', 'anyt', 'this', 'have', 'with', 'just',
    #'ther', # could it be thermometer?
    'your', 'will',
    #'work', # can it be useful?
    'what', 'from',
    #'powe', # hmmm that sounds interesting
    'thin', 'ever',
    #'peop', # hmm can be interesting
    'like', 'make', 'more',
    'grea',
    #'down', # check neighbourhood names
    #'real',
    #'need',
    'abou',
    #'help',
    #'time',
    #'safe',
    #'good',
    'were', 'know', 'goin', 
    #'wate',
    'than', 'them',
    #'nucl',
    #'here',
    #'thei',
    'movi',
    'alwa', # Always safe security
    #'city',
    'food',
    'over',
    #'shel',
    #'buil',
    #'plan',
    'hear', 'when', 'look', 'wher',
    #'plac',
    'othe', 'been', 'don\'',
    #'inte',
    #'neig',
    'hate', 'woul', 'much', 'very', 
    #'afte', # aftershock
    'it\'s' 'even', 'back', 'only', 'can\'',
    #'shou',
    'righ', 'frie', 'best',
    #'hous',
    #'part',
    'stil', 'love', 'want',
    #'clos',
    #'find',
    'tryi',
    #'thou',
    #'insp',
    #'coll',
    'does',
    #'happ', # happened vs happy
    #'brid',
    #'town',
    #'dama',
    #'call',
    #'phon',
]

class EarthQuakeData:
    def __init__(self):
        super(EarthQuakeData, self).__init__()
        self.data = pd.read_csv('../MC3/data/YInt.csv')

        print('converting from strtime to datetime...')
        self.data['time'] = pd.to_datetime(self.data['time'], format='%Y-%m-%d %H:%M:%S')

    def sortby(self, col):
        print('ordenando')
        self.data.sort_values(by=[col])

    def count_w3(self):
        wordlist  = list()
        wordset   = set()
        basecount = dict()
        for i, instance in enumerate(self.data['message']):
            if isinstance(instance, str):
                for word in instance.split():
                    if len(word) > 3:
                        baseword = word.replace('#','')[:4].lower()
                        wordlist.append(baseword)
                        wordset.add(baseword)
        print('computing word frequency')
        size = len(wordset)
        for i, word in enumerate(wordset):
            sys.stdout.write('\r%04d/%04d' % (i, size))
            sys.stdout.flush()
            basecount[word] = wordlist.count(word)
        return sorted(basecount.items(), key=lambda kv: kv[1], reverse=True)

if __name__=='__main__':
    eq = EarthQuakeData()
    eq.sortby('time')
    wordcount = eq.count_w3()
    with open('radical_freq.txt', 'w') as f:
        for i, element in enumerate(wordcount):
            word, freq = element
            f.write('%4s: %5d\n' % (word, freq))
### EOF ###
