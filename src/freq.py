#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# author: jun 2019
# Cassio Batista - cassio.batista.13@gmail.com

import sys
import os

from datetime import datetime, timedelta

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
plt.rcParams['axes.axisbelow'] = True

TIME_INTERVAL = 30 # NOTE: please provide value in minutes

class EarthQuakeData:
    def __init__(self):
        super(EarthQuakeData, self).__init__()
        self.data = pd.read_csv('../MC3/data/YInt.csv')

        print('converting from strtime to datetime...')
        for i in range(len(self.data)):
            time = self.data['time'][i]
            self.data['time'][i] = self.str2datetime(time)

    def sortby(self, col):
        self.data.sort_values(by=[col])

    def splitby_time(self):
        print('dividindo')
        first_date = self.data['time'].head(1).get_values()[0]
        last_date  = self.data['time'].tail(1).get_values()[0]

        curr_date   = first_date
        time_chunks = []
        while curr_date < last_date:
            next_date = curr_date + timedelta(minutes=TIME_INTERVAL)
            #print(first_date, '|||', curr_date, '@@', next_date, '|||', last_date)
            sys.stdout.flush()

            if next_date > last_date:
                next_date = last_date
            while not self.data.isin({'time':[next_date]})['time'].any():
                next_date += timedelta(minutes=1)

            data = self.data[self.data['time'].between(curr_date, next_date)]
            tc = TimeChunks(data)
            time_chunks.append(tc)

            curr_date = next_date
        return time_chunks

    def str2datetime(self, strdate):
        return datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')

    def datetime2str(self, dtdate):
        return dtdate.strftime('%Y-%m-%d %H:%M:%S')

class TimeChunks:
    def __init__(self, data):
        super(TimeChunks, self).__init__()
        self.data = data

    def str2datetime(self, strdate):
        return datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')

    def datetime2str(self, dtdate):
        return dtdate.strftime('%Y-%m-%d %H:%M:%S')

def plot_bar_tweet_freq(vec):
    print('plotting bar chart...')
    size = len(vec)
    xticklabels = []
    for i in range(0, size+1, 10):
        xticklabels.append('%s' % chunks[i].data['time'].head(1).get_values()[0].strftime('%m/%d\n%H:%M'))

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
    chunks = eq.splitby_time()

    lengths = []
    for i, ch in enumerate(chunks):
        lengths.append(len(ch.data))

    plot_bar_tweet_freq(lengths)
### EOF ###
