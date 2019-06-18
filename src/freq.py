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

    def splitby_time(self):
        print('dividindo')
        first_date = self.data['time'].head(1).get_values()[0]
        last_date  = self.data['time'].tail(1).get_values()[0]

        curr_date   = first_date
        time_chunks = []
        count = 0
        while curr_date < last_date:
            next_date = curr_date + np.timedelta64(TIME_INTERVAL, 'm')
            sys.stdout.flush()

            if next_date > last_date:
                next_date = last_date
            while not self.data.isin({'time':[next_date]})['time'].any():
                next_date += np.timedelta64(1, 'm')

            data = self.data[self.data['time'].between(curr_date, next_date)]
            tc = TimeChunks(data)
            time_chunks.append(tc)

            curr_date = next_date
        return time_chunks

    def str2datetime(self, strdate):
        return None # FIXME

    def datetime2str(self, dtdate):
        return None # FIXME

class TimeChunks:
    def __init__(self, data):
        super(TimeChunks, self).__init__()
        self.data = data

def plot_bar_tweet_freq(data):
    print('plotting bar chart...')
    vec = [len(ch.data) for ch in data]
    size = len(vec)
    xticklabels = []
    for i in range(0, size+1, 10):
        xticklabels.append('%s' % pd.to_datetime(data[i].data['time']
                    .head(1).get_values()[0]).strftime('%b/%d\n%H:%M')) # 

    plt.ylabel('Frequency', fontsize=32)
    plt.xlabel('Time intervals', fontsize=32)
    plt.xlim([-1.5, 215.5])

    plt.bar(np.arange(size), vec)
    plt.xticks(np.arange(0, size+1, 10), xticklabels)
    plt.yticks(np.arange(0, 1300, 100))
    plt.grid()
    plt.subplots_adjust(top=0.950, bottom=0.10, left=0.050, right=0.970)
    plt.show()

if __name__=='__main__':
    eq = EarthQuakeData()
    eq.sortby('time')
    #time_intervals = eq.splitby_time()
    #plot_bar_tweet_freq(time_intervals)
### EOF ###
