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
from bokeh.models.widgets import RangeSlider

from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.palettes import Viridis3
from bokeh.plotting import figure

from bokeh.models.annotations import Title
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid, LabelSet, Label
from bokeh.models.glyphs import HBar

from data_handler import load_data, get_useless_words, get_useful_words

data = load_data()
w_useless = get_useless_words()
w_useful  = get_useful_words()

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
    source = ColumnDataSource(dict(y=y, right=x,))
    plt = Plot( 
                title=None, plot_width=60, plot_height=400,
                min_border=0, toolbar_location=None)
    t = Title()
    t.text = key.replace(' ', '\n')
    plt.title = t
    glyph = HBar(y='y', right='right', left=0, height=0.85, fill_color="#b3de69")
    plt.add_glyph(source, glyph)

    xaxis = LinearAxis()
    plt.add_layout(xaxis, 'below')
    plt.xaxis.major_label_orientation = math.pi/2
    
    #plt.add_layout(yaxis, 'left')

    plt.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    #plt.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    #labels = LabelSet(
    #            x='x', y='y', text='y', level='glyph',
    #            #x_offset=5, y_offset=5, 
    #            source=source, render_mode='canvas')
    #plt.add_layout(labels)
    for i, word in enumerate(words):
        note = Label(x=5, y=i*34, x_units='screen', y_units='screen',
                    text=word, render_mode='css',
                    border_line_color='black',
                    border_line_alpha=1.0,
                    background_fill_color='white',
                    background_fill_alpha=0.5)
        plt.add_layout(note)
    plots.append(plt)

# make a grid
grid = gridplot([
    plots,
])

range_slider = RangeSlider(
            title = "Time Interval", 
            value = [1000, 20000], 
            start = data.index[0], 
            end   = data.index[-1], 
            step  = 1)

sliders = Row(children=[
    Column(children=[
        grid,
        range_slider,
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
