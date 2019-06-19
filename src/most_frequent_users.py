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

TIME_INTERVAL = 30 # NOTE: please provide value in minutes

class EarthQuakeData:
    def __init__(self):
        super(EarthQuakeData, self).__init__()
        self.data = pd.read_csv('../MC3/data/YInt.csv')

        print('converting from strtime to datetime...')
        self.data['time'] = pd.to_datetime(self.data['time'], format='%Y-%m-%d %H:%M:%S')

    def sortby(self, col):
        print('ordenando')
        self.data.sort_values(by=[col])


    def calc_user_freq(self):
        user_count = dict()
        for username in self.data['account']:
            if username in user_count.keys():
                user_count[username] += 1
            else:
                user_count[username] = 1
        return sorted(user_count.items(), key=lambda kv: kv[1], reverse=True)

class TimeChunks:
    def __init__(self, data):
        super(TimeChunks, self).__init__()
        self.data = data

def plot_bar_tweet_freq(x, xticklabels):
    print('plotting bar chart...')
    myvecs = [
        x[x.index(max(x)):x.index(24)],
        x[x.index(24):x.index(20)],
        x[x.index(20):x.index(18)]
    ]
    myvecticks = [
        xticklabels[x.index(max(x)):x.index(24)],
        xticklabels[x.index(24):x.index(20)],
        xticklabels[x.index(20):x.index(18)]
    ]
    for vec, vecticklabels in zip(myvecs,myvecticks):
        size = len(vec)

        plt.ylabel('Number of Tweets Overall', fontsize=28)
        plt.xlim([-1.0, size])

        plt.bar(np.arange(size), vec)
        plt.xticks(np.arange(0, size+1), vecticklabels, rotation=90)
        plt.yticks(np.arange(0, max(vec)+2.5, 2.5))

        for i, freq in enumerate(vec):
            plt.text(i, freq+0.5, str(vec[i]), ha='center', va='center', rotation=90)

        plt.grid()
        plt.subplots_adjust(top=0.950, bottom=0.25, left=0.050, right=0.980)

        plt.show()

if __name__=='__main__':
    eq = EarthQuakeData()
    eq.sortby('time')
    ufreq = eq.calc_user_freq()
    x = []
    xticklabels = []
    for i, element in enumerate(ufreq):
        username, freq = element
        x.append(freq)
        xticklabels.append('@' + username)

    plot_bar_tweet_freq(x, xticklabels)
### EOF ###
