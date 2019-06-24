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

from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.resources import INLINE
from bokeh.util.browser import view

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

def count_words(data, useful, useless, start_date, end_date):
    word_count = {}
    for location in data.location.unique():
        word_count[location] = {}
    data = data[data.time.between(start_date, end_date)]
    for location, tweet in zip(data.location, data.message): 
        if not isinstance(tweet, str):
            continue
        tweet = re.sub('[#@!?,.;]', ' ', tweet)
        for word in tweet.split():
            if len(word) > MIN_WLEN:
                word = word[:MIN_WLEN+1]
                if word in useless:
                    continue
                if word in word_count[location]:
                    word_count[location][word] += 1
                else:
                    word_count[location][word]  = 1
    return word_count

def get_barplots(word_count):
    mapper = linear_cmap(field_name='right', palette=Spectral6, low=3, high=234)
    plots = []
    for key, value in word_count.items():
        if key.startswith('unk') or key.startswith('<loc'): # useless tweets here
            continue
        y = np.arange(NUM_WORDS)
        wordfreqlist = sorted(value.items(), key=lambda kv: kv[1], reverse=True)
        x = []
        words = []
        for i, element in enumerate(wordfreqlist[:NUM_WORDS]):
            word, freq = element
            x.append(freq)
            words.append(word)

        source = ColumnDataSource(dict(y=y, right=x,))
        plt = Plot(
                title            = None, 
                plot_width       = 95, 
                plot_height      = 400,
                min_border       = 0, 
                toolbar_location = None)
        t = Title()
        t.text = key.split()[0]
        plt.title = t
        glyph = HBar(y='y', right='right', left=0, height=0.85, fill_color=mapper)
        plt.add_glyph(source, glyph)

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

        plots.append(plt)

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
    plots.append(plt)
    return plots

def draw_layout(data, plots):
    grid = gridplot([
        plots,
    ])

    date_range_slider = DateRangeSlider(
                start  = data['time'].iloc[0],
                end    = data['time'].iloc[-1],
                value  = (data['time'].iloc[0], data['time'].iloc[-1]),
                format = '%d/%m@%H:%M',
                step   = 1,
                width = 95*(len(plots)-1),
                bar_color='purple')

    play_button = Button(
            label       = 'Run', 
            width       = 75,
            button_type = 'success')

    bottom_layout = Row(children=[
        date_range_slider, 
        play_button,
    ])

    main_layout = Row(children=[
        Column(children=[
            grid,
            bottom_layout,
        ]),
    ])

    doc = Document()
    doc.add_root(main_layout)
    return doc

if __name__ == "__main__":
    data_source      = data_handler.load_data()
    useful_wordlist  = data_handler.get_useful_words()
    useless_wordlist = data_handler.get_useless_words()
    
    word_count = count_words(data_source, useful_wordlist, useless_wordlist,
                data_source.time.iloc[0], data_source.time.iloc[-1])

    barplots = get_barplots(word_count)

    doc = draw_layout(data_source, barplots)

    doc.validate()
    filename = "vast-mc3.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "vast-mc3"))
    view(filename)
