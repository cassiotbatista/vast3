#!/usr/bin/env python3
#
# VAST Challenge 2019: Disaster at St. Himark!
# https://vast-challenge.github.io/2019/index.html
#
# Federal University of Pará (UFPA)
#
# author: june 2019
# cassio batista - cassio.batista.13@gmail.com
# edwin jueda    - 
# erick campos   - 

import sys
import os
import re

import pandas as pd
import numpy as np

from collections import OrderedDict
from termcolor import cprint
from sklearn.preprocessing import minmax_scale
from datetime import datetime, timedelta
  
from bokeh.io import curdoc, export_png
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid, ColorBar, \
            FixedTicker, HoverTool
from bokeh.models.widgets import DateRangeSlider, Button, Div, Select
from bokeh.models.layouts import Row, Column
from bokeh.models.glyphs import HBar, VBar
from bokeh.models.annotations import Title
from bokeh.layouts import gridplot
from bokeh.plotting import figure

from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral6, Category20_19, Reds9
Reds9.reverse()

import config
import data_handler 

from svg2 import SVG

TAG = 'VASTGUI'

data                = data_handler.load_data()
useful_wordlist     = data_handler.get_useful_words()
useless_wordlist    = data_handler.get_useless_words()
keyclusters         = data_handler.get_synonym_cluster()
heatmap_data        = data_handler.load_heatmap_data()

full_time_range = list(heatmap_data.time.unique())

mapper = linear_cmap(field_name='right', palette=Spectral6, low=0, high=1)

color_bar = ColorBar(
        color_mapper = mapper['transform'], 
        width        = 8,
        location     = (0,0))

prefix_count    = OrderedDict()
wword_count     = OrderedDict()
user_count      = OrderedDict()
mention_count   = OrderedDict()

word_barplots   = []
word_sources    = []
word_hbarglyphs = []

user_barplot=Plot(title=None, 
        plot_width=650, plot_height=500,
        min_border=0, toolbar_location=None,
        tools=[HoverTool(tooltips=[('wlist', '@wlist')], 
            point_policy='follow_mouse')])

mention_barplot=Plot(title=None, 
        plot_width=600, plot_height=500,
        min_border=0, toolbar_location=None)

svg = SVG()
svg.rescale(0.45)
svg_div = Div(text=svg.to_string(), width=100, height=100)

ghost_fig = figure(title=None, plot_width=60, plot_height=400,
            min_border=0, toolbar_location=None)
ghost_fig.add_layout(color_bar, 'right')

user_tweet_freq    = OrderedDict()
mention_tweet_freq = OrderedDict()

def save_png_callback():
    export_png(grid,            filename=config.HBAR_PNG)
    export_png(user_barplot,    filename=config.USER_PNG)
    export_png(mention_barplot, filename=config.MENTION_PNG)
    export_png(svg_layout,      filename=config.SVGMAP_PNG)
    export_png(heatmap_layout,  filename=config.HEATKW_PNG)

def init_word_barplots():
    global word_barplots
    global word_sources
    word_barplots = []
    word_sources  = []
    for i in range(len(prefix_count)):
        src = ColumnDataSource(dict(y=[], right=[], wlist=[],))
        plt = Plot(title=None, plot_width=95, plot_height=300,
                min_border=0, toolbar_location=None,
                tools=[HoverTool(tooltips=[ ('wlist','@wlist')], 
                        point_policy='follow_mouse')])
        word_barplots.append(plt)
        word_sources.append(src)
        plt = Plot(title=None, plot_width=60, plot_height=300, 
                min_border=0, toolbar_location = None)
    plt.add_layout(color_bar, 'right')
    word_barplots.append(plt)

def init_wordcount():
    global prefix_count
    global wword_count
    prefix_count = OrderedDict()
    wword_count  = OrderedDict()
    for location in data.location.unique():
        if location.startswith('unk') or location.startswith('<loc') \
                or location.startswith('wilson'):
            continue
        prefix_count[location] = {}
        wword_count[location] = {}

init_wordcount()
init_word_barplots()

def function_to_call(attr, old, new):
    global neigh_heatmap
    global neigh_source
    global neigh_mapper
    keyword = keycluster_select.value.split()[0]
    neigh_heatmap.title.text = 'Keyword "%s" peaks over time' % keyword
    neigh_source.data = heatmap_data[heatmap_data.keyword==keyword].to_dict(orient='list')
    neigh_mapper['transform'].low  = min(neigh_source.data['frequency']) 
    neigh_mapper['transform'].high = max(neigh_source.data['frequency']) 

keycluster_select = Select(title='Keywords:', width=600,
        value=keyclusters[0], options=keyclusters)
neigh_source=ColumnDataSource(heatmap_data[
        heatmap_data.keyword==keycluster_select.value.split()[0]].to_dict(orient='list'))
keycluster_select.on_change('value', function_to_call)
neigh_mapper=linear_cmap(field_name='frequency', palette=Reds9, 
        low= min(neigh_source.data['frequency']), 
        high=max(neigh_source.data['frequency'])) 
neigh_heatmap=figure(
        title='Keyword "%s" peaks over time' % keycluster_select.value.split()[0],
        x_range=full_time_range,
        y_range=list(reversed(config.NEIGHBOURHOODS)),
        plot_width=95*(len(word_barplots)-1)+40, plot_height=600,
        tools='hover,save,box_zoom,reset', toolbar_location='left',
        tooltips=[('location','@location'), ('time','@time'), ('frequency', '@frequency')])
neigh_heatmap.grid.grid_line_color = None
neigh_heatmap.axis.axis_line_color = None
neigh_heatmap.axis.major_tick_line_color = None
neigh_heatmap.xaxis.major_label_orientation = np.pi / 3
neigh_heatmap.rect(x='time', y='location', width=1, height=1,
       source=neigh_source,
       fill_color=neigh_mapper,
       line_color=None)
neigh_color_bar = ColorBar(
        color_mapper = neigh_mapper['transform'], 
        width        = 8,
        location     = (0,0))
neigh_heatmap.add_layout(neigh_color_bar, 'left')

def count_words(prefix_count, wword_count):
    cprint('%s: counting words...' % TAG, 'yellow', attrs=['bold'])
    date_value = date_range_slider.value_as_datetime
    data_chunk = data[data.time.between(date_value[0], date_value[1])]
    for location, tweet in zip(data_chunk.location, data_chunk.message): 
        if location.startswith('unk') or location.startswith('<loc') \
                or location.startswith('wilson'):
            continue
        for word in tweet.split():
            if word.startswith('@') or word.count(':') > 1:
                continue
            word = re.sub('[:]', '', word)
            if len(word) > config.PREFIX_LEN:
                prefix = word[:config.PREFIX_LEN+1]
                if prefix in useless_wordlist:
                    continue
                if not prefix in prefix_count[location]:
                    prefix_count[location][prefix]  = 1
                else:
                    prefix_count[location][prefix] += 1
                if not prefix in wword_count[location]:
                    wword_count[location][prefix] = { word: 1 }
                elif not word in wword_count[location][prefix]:
                    wword_count[location][prefix][word]  = 1
                else:
                    wword_count[location][prefix][word] += 1
    cprint('done!', 'yellow', attrs=['bold'])

def count_users():
    global user_tweet_freq
    cprint('%s: counting @ users...' % TAG, 'yellow', attrs=['bold'])
    user_count = data.account.value_counts()
    user_count = user_count[user_count.between(config.MIN_NUM_TWEETS, user_count.max())]
    cprint('%s: counting words tweeted by user...' % TAG, 'yellow', attrs=['bold'])
    for user, freq in user_count.items():
        if not user in user_tweet_freq:
            user_tweet_freq[user] = {}
        for tweet in data[data.account == user].message:
            for word in tweet.split():
                if word.startswith('@') or word.count(':') > 1:
                    continue
                word = re.sub('[:]', '', word)
                if len(word) > config.PREFIX_LEN:
                    prefix = word[:config.PREFIX_LEN+1]
                    if not prefix in user_tweet_freq[user]:
                        user_tweet_freq[user][prefix]  = 1
                    else:
                        user_tweet_freq[user][prefix] += 1
    return user_count.to_dict(into=OrderedDict)

def count_mentions():
    cprint('%s: counting @ mentions...' % TAG, 'yellow', attrs=['bold'])
    mention_count = OrderedDict()
    for tweet in data['message']:
        for word in tweet.split():
            if word.startswith('@'):
                if word in mention_count.keys():
                    mention_count[word] += 1
                else:
                    mention_count[word] = 1
    return sorted(mention_count.items(), 
            key=lambda kv: kv[1], reverse=True)[:config.NUM_MENTIONS]

def get_freq_range(prefix_count):
    frequencies = []
    for wordcountdict in prefix_count.values():
        wordfreqlist = sorted(wordcountdict.items(), 
                    key=lambda kv: kv[1], reverse=True)
        for word, freq in wordfreqlist[:config.NUM_WORD_BARS]:
            frequencies.append(freq)
    return min(frequencies), max(frequencies)

def init_user_plot():
    cprint('%s: init @ users barcharts...' % TAG, 'yellow', attrs=['bold'])
    global user_count
    global user_barplot
    user_count = count_users()
    y = []
    users = []
    for (user, freq) in user_count.items():
        y.append(freq)
        users.append(user)
    x = np.arange(len(users))

    wlist = []
    for user in users:
        prefixes = ['@' + user]
        for prefix, freq in sorted(user_tweet_freq[user].items(), 
                key=lambda kv: kv[1], reverse=True)[:10]:
            prefixes.append(' %s:%d' % (prefix, freq))
        wlist.append(list(prefixes))

    source = ColumnDataSource(dict(x=x, top=y, wlist=wlist))
    glyph = VBar(x='x', top='top', bottom=0, width=0.85, fill_color='#1f77b4')
    user_barplot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    xaxis.ticker = x
    xaxis.major_label_overrides = {i : '@'+user for i, user in enumerate(users)}
    #xaxis.major_label_standoff = -35
    user_barplot.add_layout(xaxis, 'below')
    user_barplot.xaxis.major_label_orientation = +np.pi/2

    yaxis = LinearAxis()
    yaxis.axis_label='Overall number of tweets per @'
    yaxis.axis_label_text_font_size = '14pt'
    yaxis.ticker = np.linspace(0, max(y), 11, dtype=np.int)[1:]
    user_barplot.add_layout(yaxis, 'left')
    
    user_barplot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    user_barplot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

def init_mention_plot():
    cprint('%s: init @ mentios barcharts...' % TAG, 'yellow', attrs=['bold'])
    global mention_count
    global mention_barplot
    mention_count = count_mentions()
    y = []
    mentions = []
    for (mention, freq) in mention_count:
        y.append(freq)
        mentions.append(mention)
    x = np.arange(len(mentions))
    source = ColumnDataSource(dict(x=x, top=y,))
    glyph = VBar(x='x', top='top', bottom=0, width=0.85, fill_color='#ff7f0e')
    mention_barplot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    xaxis.ticker = x
    xaxis.major_label_overrides = {i : mention for i, mention in enumerate(mentions)}
    mention_barplot.add_layout(xaxis, 'below')
    mention_barplot.xaxis.major_label_orientation = +np.pi/2

    yaxis = LinearAxis()
    yaxis.axis_label='Overall number of @ mentions' 
    yaxis.axis_label_text_font_size = '14pt'
    yaxis.ticker = np.linspace(0, max(y), 11, dtype=np.int)[1:]
    mention_barplot.add_layout(yaxis, 'left')
    
    mention_barplot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    mention_barplot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

def init_plot():
    cprint('%s: init barcharts per neighbourhood...' % TAG, 'yellow', attrs=['bold'])
    init_wordcount()
    global prefix_count
    global wword_count
    global word_barplots
    global word_sources
    global mapper

    global svg_div

    init_user_plot()
    init_mention_plot()

    count_words(prefix_count, wword_count)

    # update colorbar
    min_freq, max_freq = get_freq_range(prefix_count)
    mapper['transform'].low  = min_freq
    mapper['transform'].high = max_freq

    # update colorbar tickers
    steps = 13
    while max_freq < steps:
        steps = steps//2
    color_bar.ticker = FixedTicker(ticks=np.linspace(min_freq, 
                    max_freq, steps, dtype=np.int))

    y = np.arange(config.NUM_WORD_BARS)
    for i, (neigh,wcount) in enumerate(prefix_count.items()):
        wordfreqlist = sorted(wcount.items(), key=lambda kv: kv[1], reverse=True)
        x = []
        prefixes = []
        wlist = []
        for prefix, freq in wordfreqlist[:config.NUM_WORD_BARS]:
            x.append(freq)
            prefixes.append(prefix)
            wlist.append([' %s:%d' % (k,v) \
                        for (k,v) in sorted(wword_count[neigh][prefix].items(), 
                                key=lambda kv:kv[1], reverse=True)[:5]])

        color_index = np.round(minmax_scale([np.mean(x[:5]), min_freq, max_freq], 
                        feature_range=(0,5))[0])
        map_fill_color = Spectral6[np.int(color_index)]
        svg.change_fill_color(neigh.replace(' ',''), map_fill_color)

        plt = word_barplots[i]
        src = word_sources[i]
        src.data = dict(y=y, right=x, wlist=wlist)

        t = Title()
        t.text = neigh.title()[:13]
        plt.title = t

        glyph = HBar(y='y', right='right', left=0, height=0.90, fill_color=mapper)
        word_hbarglyphs.append(glyph)
        plt.add_glyph(src, glyph)

        xaxis = LinearAxis()
        xaxis.ticker = np.linspace(0, max(x), 5, dtype=np.int)[1:]
        plt.add_layout(xaxis, 'below')
        plt.xaxis.major_label_orientation = +np.pi/2
        
        yaxis = LinearAxis()
        yaxis.ticker = y
        yaxis.major_label_overrides = { i : prefix for i, prefix in enumerate(prefixes) }
        yaxis.major_label_standoff = -35
        plt.add_layout(yaxis, 'left')

        plt.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plt.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

    svg_div.text = svg.to_string()

def update():
    cprint('%s: update barcharts per neighbourhood...' % TAG, 'yellow', attrs=['bold'])
    init_wordcount()
    global prefix_count
    global wword_count
    global word_barplots
    global word_sources
    global mapper
    global color_bar

    global svg_div

    count_words(prefix_count, wword_count)

    # update mapper
    min_freq, max_freq = get_freq_range(prefix_count)
    mapper['transform'].low  = min_freq
    mapper['transform'].high = max_freq

    # update colorbar tickers
    steps = 13
    while max_freq < steps:
        steps = steps//2
    color_bar.ticker = FixedTicker(ticks=np.linspace(min_freq, 
                    max_freq, steps, dtype=np.int))

    y = np.arange(config.NUM_WORD_BARS)
    for i, (neigh,wcount) in enumerate(prefix_count.items()):
        if len(wcount) == 0:
            wcount = { 'none': 1 }

        wordfreqlist = sorted(wcount.items(), key=lambda kv: kv[1], reverse=True)
        x = []
        prefixes = []
        wlist = []
        for prefix, freq in wordfreqlist[:config.NUM_WORD_BARS]:
            x.append(freq)
            prefixes.append(prefix)
            wlist.append([' %s:%d' % (k,v) \
                        for (k,v) in sorted(wword_count[neigh][prefix].items(), 
                                key=lambda kv:kv[1], reverse=True)[:5]])

        color_index = np.round(minmax_scale([np.mean(x[:5]), min_freq, max_freq], 
                        feature_range=(0,5))[0])
        map_fill_color = Spectral6[np.int(color_index)]
        svg.change_fill_color(neigh.replace(' ',''), map_fill_color)

        plt = word_barplots[i]
        src = word_sources[i]
        glyph = word_hbarglyphs[i]

        src.data = dict(y=y, right=x, wlist=wlist)
        glyph.update(fill_color=mapper)

        steps = 5
        if max(x) < steps:
            steps = max(x)
        plt.xaxis.ticker = np.linspace(0, max(x), steps, dtype=np.int)[1:]
        
        plt.yaxis.major_label_overrides = { i : prefix for i, prefix in enumerate(prefixes) }

    svg_div.text = svg.to_string()

save_button = Button(
        label       = 'Save all plots at once', 
        width       = 100,
        height      = 50,
        orientation = 'vertical',
        button_type = 'primary')
save_button.on_click(save_png_callback)

grid = gridplot(children=[ 
        word_barplots,
    ], toolbar_location=None, merge_tools=True)

date_range_slider = DateRangeSlider(
        start  = data['time'].iloc[0],
        end    = data['time'].iloc[-1],
        value  = (data['time'].iloc[0], data['time'].iloc[-1]),
        format = '%d/%m@%H:%M',
        step   = 1,
        width = 95*(len(word_barplots)-1)-40, # padded
        bar_color='purple')

play_button = Button(
        label       = 'Run', 
        width       = 75,
        button_type = 'success')
play_button.on_click(update)

bottom_layout = Row(children=[
    date_range_slider, play_button,
])

svg_layout = Row(svg_div, width=450, height=380)

arroba_layout = Row(children=[
    ghost_fig, svg_layout, user_barplot, mention_barplot, 
])

heatmap_layout = Column(children=[
        keycluster_select,
        neigh_heatmap,
    ])

main_layout = Row(children=[
    Column(children=[ 
        grid, 
        bottom_layout, 
        arroba_layout,
        heatmap_layout,
        save_button,
    ]),
])

init_plot()  # initial load of the data

curdoc().add_root(main_layout)
curdoc().title = 'VAST 3 by Cassio, Edwin, Erick & Larissa'
