#!/usr/bin/env python3
#
# author: jun 2019
# cassio batista - https://cassota.gitlab.io/

import sys
import os
import re

import math
import pandas as pd
import numpy as np
from collections import OrderedDict

from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.resources import INLINE
from bokeh.util.browser import view

from bokeh.io import curdoc
from bokeh.models.layouts import Row, Column
from bokeh.models.widgets import DateRangeSlider, Button
from bokeh.models.annotations import Title
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid, LabelSet, Label, ColorBar, FixedTicker
from bokeh.models.glyphs import HBar
from bokeh.layouts import gridplot

from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap

import data_handler 

NUM_WORDS = 10
MIN_WLEN  = 3

data             = data_handler.load_data()
useful_wordlist  = data_handler.get_useful_words()
useless_wordlist = data_handler.get_useless_words()

mapper = linear_cmap(field_name='right', palette=Spectral6, low=3, high=234)

word_count = OrderedDict()
barplots   = []
sources    = []

def init_barplots():
    global barplots
    global sources
    barplots = []
    sources  = []
    for i in range(len(word_count)):
        src = ColumnDataSource(dict(y=[], right=[],))
        plt = Plot(
            title            = None, 
            plot_width       = 95, 
            plot_height      = 400,
            min_border       = 0, 
            toolbar_location = None)
        barplots.append(plt)
        sources.append(src)
    plt = Plot(
            title            = None, 
            plot_width       = 60, 
            plot_height      = 400,
            min_border       = 0, 
            toolbar_location = None)
    color_bar = ColorBar(
                color_mapper = mapper['transform'], 
                width        = 8,
                location     = (0,0),
                ticker       = FixedTicker(ticks=np.linspace(0, 250, 11, dtype=np.int)))
    plt.add_layout(color_bar, 'right')
    barplots.append(plt)

def init_wordcount():
    global word_count
    word_count = OrderedDict()
    for location in data.location.unique():
        if location.startswith('unk') or location.startswith('<loc'):
            continue
        word_count[location] = {}

init_wordcount()
init_barplots()

def init_plot():
    init_wordcount()
    global word_count
    global barplots
    global sources
    date_value = date_range_slider.value_as_datetime
    data_chunk = data[data.time.between(date_value[0], date_value[1])]
    print(len(data), len(data_chunk))
    for location, tweet in zip(data_chunk.location, data_chunk.message): 
        if location.startswith('unk') or location.startswith('<loc'):
            continue
        if not isinstance(tweet, str):
            continue
        tweet = re.sub('[#@!?,.;]', ' ', tweet)
        for word in tweet.split():
            if len(word) > MIN_WLEN:
                word = word[:MIN_WLEN+1]
                if word in useless_wordlist:
                    continue
                if word in word_count[location]:
                    word_count[location][word] += 1
                else:
                    word_count[location][word]  = 1

    y = np.arange(NUM_WORDS)
    for i, (neigh,wcount) in enumerate(word_count.items()):
        wordfreqlist = sorted(wcount.items(), key=lambda kv: kv[1], reverse=True)
        x = []
        words = []
        for word, freq in wordfreqlist[:NUM_WORDS]:
            x.append(freq)
            words.append(word)

        plt = barplots[i]
        src = sources[i]
        src.data = dict(y=y, right=x)

        t = Title()
        t.text = neigh.split()[0]
        plt.title = t

        glyph = HBar(y='y', right='right', left=0, height=0.85, fill_color=mapper)
        plt.add_glyph(src, glyph)

        xaxis = LinearAxis()
        xaxis.ticker = np.linspace(0, max(x), 5, dtype=np.int)[1:]
        plt.add_layout(xaxis, 'below')
        plt.xaxis.major_label_orientation = +math.pi/2
        
        yaxis = LinearAxis()
        yaxis.ticker = y
        yaxis.major_label_overrides = { i : word for i, word in enumerate(words) }
        yaxis.major_label_standoff = -35
        plt.add_layout(yaxis, 'left')

        plt.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plt.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

def update():
    init_wordcount()
    global word_count
    global barplots
    global sources
    date_value = date_range_slider.value_as_datetime
    data_chunk = data[data.time.between(date_value[0], date_value[1])]
    print(len(data), len(data_chunk))
    for location, tweet in zip(data_chunk.location, data_chunk.message): 
        if location.startswith('unk') or location.startswith('<loc'):
            continue
        if not isinstance(tweet, str):
            continue
        tweet = re.sub('[#@!?,.;]', ' ', tweet)
        for word in tweet.split():
            if len(word) > MIN_WLEN:
                word = word[:MIN_WLEN+1]
                if word in useless_wordlist:
                    continue
                if word in word_count[location]:
                    word_count[location][word] += 1
                else:
                    word_count[location][word]  = 1

    y = np.arange(NUM_WORDS)
    for i, (neigh,wcount) in enumerate(word_count.items()):
        wordfreqlist = sorted(wcount.items(), key=lambda kv: kv[1], reverse=True)
        x = []
        words = []
        for word, freq in wordfreqlist[:NUM_WORDS]:
            x.append(freq)
            words.append(word)

        plt = barplots[i]
        src = sources[i]
        src.data = dict(y=y, right=x)

        xaxis = LinearAxis()
        xaxis.ticker = np.linspace(0, max(x), 5, dtype=np.int)[1:]
        plt.add_layout(xaxis, 'below')
        plt.xaxis.major_label_orientation = +math.pi/2
        
        yaxis = LinearAxis()
        yaxis.ticker = y
        yaxis.major_label_overrides = { i : word for i, word in enumerate(words) }
        yaxis.major_label_standoff = -35
        plt.add_layout(yaxis, 'left')

        plt.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plt.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

grid = gridplot([ barplots ])

date_range_slider = DateRangeSlider(
        start  = data['time'].iloc[0],
        end    = data['time'].iloc[-1],
        value  = (data['time'].iloc[0], data['time'].iloc[-1]),
        format = '%d/%m@%H:%M',
        step   = 1,
        width = 95*(len(barplots)-1),
        bar_color='purple')

play_button = Button(
        label       = 'Run', 
        width       = 75,
        button_type = 'success')

bottom_layout = Row(children=[
    date_range_slider, play_button,
])

main_layout = Row(children=[
    Column(children=[ grid, bottom_layout, ]),
])

play_button.on_click(update)

init_plot()  # initial load of the data

curdoc().add_root(main_layout)
