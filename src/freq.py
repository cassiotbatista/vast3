#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# author: jun 2019
# Cassio Batista - cassio.batista.13@gmail.com

import sys
import os

from datetime import datetime

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

TIME_INTERVAL = 30

class TimeChunks:
    def __init__(self):
        super(TimeChunks, self).__init__()
        self.data = pd.read_csv('../MC3/data/YInt.csv')

    def sortby(self, col):
        self.data.sort_values(by=[col])

    def parse_str2datetime(self):
        for i in range(len(self.data)):
            strdate = self.data['time'][i] 
            self.data['time'][i] = datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')
        

if __name__=='__main__':
    tc = TimeChunks()
    tc.sortby('time')
