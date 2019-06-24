#!/usr/bin/env python3

import sys
import os
import re

from datetime import date

import collections
import math

import pandas as pd
import numpy as np

from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.resources import INLINE
from bokeh.util.browser import view
from bokeh.models.layouts import Row, Column
from bokeh.models.widgets import DateRangeSlider

from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.palettes import Viridis3
from bokeh.plotting import figure

from bokeh.models.annotations import Title
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid, LabelSet, Label, ColorBar, FixedTicker
from bokeh.models.glyphs import HBar

from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap

from data_handler import load_data, get_useless_words, get_useful_words

data = load_data()
w_useless = get_useless_words()
w_useful  = get_useful_words()

mapper = linear_cmap(field_name='right', palette=Spectral6, low=3, high=234)

word_count = {}
for location in data.location.unique():
    word_count[location] = {}

for location, tweet in zip(data['location'], data['message']): # TODO add time filter
    if isinstance(tweet, str):
        tweet = re.sub('[#@!?,.;]', ' ', tweet)
        for word in tweet.split():
            if len(word) > 3:
                word = word[:4]
                if word in w_useless:
                    continue
                if word in word_count[location]:
                    word_count[location][word] += 1
                else:
                    word_count[location][word]  = 1
plots = []
for key, value in word_count.items():
    if key.startswith('unk') or key.startswith('<loc'):
        continue
    y = np.arange(10)
    wordfreqlist = sorted(value.items(), key=lambda kv: kv[1], reverse=True)
    x = []
    words = []
    for i, element in enumerate(wordfreqlist):
        word, freq = element
        x.append(freq)
        words.append(word)
        if i == 9:
            break

    print(max(x), min(x))
    source = ColumnDataSource(dict(y=y, right=x,))
    plt = Plot( 
                title=None, plot_width=95, plot_height=400,
                min_border=0, toolbar_location=None)
    t = Title()
    t.text = key.split()[0]
    plt.title = t
    glyph = HBar(y='y', right='right', left=0, height=0.85, fill_color=mapper)
    plt.add_glyph(source, glyph)

    xaxis = LinearAxis()
    xaxis.ticker = np.linspace(0, max(x), 5, dtype=np.int)[1:]
    plt.add_layout(xaxis, 'below')
    plt.xaxis.major_label_orientation = +math.pi/2
    
    yticklabels = {}
    yaxis = LinearAxis()
    for i, word in enumerate(words):
        yticklabels[str(i)] = word.strip().rstrip()
        if i == 9:   
            break
    yaxis.ticker = y
    yaxis.major_label_overrides = yticklabels
    yaxis.major_label_standoff = -35
    plt.add_layout(yaxis, 'left')

    plt.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plt.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

    plots.append(plt)

plt = Plot( 
        title=None, plot_width=60, plot_height=400,
        min_border=0, toolbar_location=None)
color_bar = ColorBar(
            color_mapper=mapper['transform'], 
            width=8,
            location=(0,0),
            ticker=FixedTicker(ticks=np.linspace(0,250,11, dtype=np.int)))
plt.add_layout(color_bar, 'right')
plots.append(plt)

# make a grid
grid = gridplot([
    plots,
])

date_range_slider = DateRangeSlider(
            start  = data['time'].iloc[0],
            end    = data['time'].iloc[-1],
            value  = (data['time'].iloc[0], data['time'].iloc[-1]),
            format = '%d/%m@%H:%M',
            step   = 1,
            bar_color='purple')

sliders = Row(children=[
    Column(children=[
        grid,
        date_range_slider,
    ]),
])

doc = Document()
doc.add_root(sliders)

if __name__ == "__main__":
    doc.validate()
    filename = "sliders.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "sliders"))
    view(filename)
