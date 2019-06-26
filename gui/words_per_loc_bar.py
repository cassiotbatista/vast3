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

mapper = linear_cmap(field_name='right', palette=Spectral6, low=0, high=1)
color_bar = ColorBar(
        color_mapper = mapper['transform'], 
        width        = 8,
        location     = (0,0))

word_count = OrderedDict()
barplots   = []
sources    = []
hbarglyphs = []

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

def count_words(word_count):
    date_value = date_range_slider.value_as_datetime
    data_chunk = data[data.time.between(date_value[0], date_value[1])]
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

def get_freq_range(word_count):
    frequencies = []
    for wordcountdict in word_count.values():
        wordfreqlist = sorted(wordcountdict.items(), 
                    key=lambda kv: kv[1], reverse=True)
        for word, freq in wordfreqlist[:NUM_WORDS]:
            frequencies.append(freq)
    return min(frequencies), max(frequencies)

def init_plot():
    init_wordcount()
    global word_count
    global barplots
    global sources
    global mapper

    count_words(word_count)

    # update colorbar
    min_freq, max_freq = get_freq_range(word_count)
    mapper['transform'].low  = min_freq
    mapper['transform'].high = max_freq

    # update colorbar tickers
    steps = 11
    if max_freq < steps:
        steps = max_freq
    color_bar.ticker = FixedTicker(ticks=np.linspace(min_freq, 
                    max_freq, steps, dtype=np.int))

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
        t.text = neigh[:13]
        plt.title = t

        glyph = HBar(y='y', right='right', left=0, height=0.85, fill_color=mapper)
        hbarglyphs.append(glyph)
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
    global mapper
    global color_bar

    count_words(word_count)

    # update mapper
    min_freq, max_freq = get_freq_range(word_count)
    mapper['transform'].low  = min_freq
    mapper['transform'].high = max_freq

    # update colorbar tickers
    steps = 11
    if max_freq < steps:
        steps = max_freq
    color_bar.ticker = FixedTicker(ticks=np.linspace(min_freq, 
                    max_freq, steps, dtype=np.int))

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
        glyph = hbarglyphs[i]

        src.data = dict(y=y, right=x)
        glyph.update(fill_color=mapper)

        steps = 5
        if max(x) < steps:
            steps = max(x)
        plt.xaxis.ticker = np.linspace(0, max(x), steps, dtype=np.int)[1:]
        
        plt.yaxis.major_label_overrides = { i : word for i, word in enumerate(words) }

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
