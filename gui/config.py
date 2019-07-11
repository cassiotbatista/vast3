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

import os
from termcolor import cprint

TAG = 'cfg'

SRC_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SRC_DIR, os.pardir))

IMG_DIR = os.path.join(SRC_DIR, 'images')

DO_LEMMATIZE = True
if not DO_LEMMATIZE:
    cprint('%s: lemmatize step will be skipped to speed up the process' % TAG, 
            'red', attrs=['bold'])

DO_BLACK_SELECT = True
if not DO_BLACK_SELECT:
    cprint('%s: all tweets will pass irrespective of who\'s tweeting' % TAG, 
            'red', attrs=['bold'])

DO_KW_SELECT = True
if not DO_KW_SELECT:
    cprint('%s: all tweets will pass irrespective of the keywords defined' % TAG, 
            'red', attrs=['bold'])

DO_SW_SELECT = True
if not DO_SW_SELECT:
    cprint('%s: all tweets will pass irrespective of the stopwords defined' % TAG, 
            'red', attrs=['bold'])

DO_SPELLCHECK = True
if not DO_SPELLCHECK:
    cprint('%s: spell checking will be skipped to speed up the process' % TAG, 
            'red', attrs=['bold'])

NEIGHBOURHOODS = [ 
        'old town',    'northwest',   'palace hills',
        'downtown',    'weston',      'easton',
        'safe town',   'southwest',   'southton',
        'west parton', 'east parton', 'oak willow',
        'cheddarford', 'pepper mill', 'terrapin springs',
        'broadview',   'chapparal',    'scenic vista', ]

NUM_WORD_BARS = 15
PREFIX_LEN  = 3

MIN_NUM_TWEETS = 11
NUM_MENTIONS = 22

SVG_NODE_HIERARCHY = ['svg', 'g', 'path', 'text', 'tspan']
SVGFILE = os.path.join(ROOT_DIR, 'MC3', 'maps', 'custom', 'neigh_labels.svg')
SVGTEST = os.path.join(ROOT_DIR, 'MC3', 'maps', 'mapa_vast_vetorizado.svg')

DATA_PROC_CSVFILE = os.path.join(SRC_DIR, 'data', 'data.csv')
DATA_HEAT_CSVFILE = os.path.join(SRC_DIR, 'data', 'heat_freq.csv')
DATA_SRC_CSVFILE  = os.path.join(ROOT_DIR, 'MC3', 'data', 'YInt.csv')
REPLACE_FILE      = os.path.join(ROOT_DIR, 'src', 'replace.txt')
USELESS_FILE      = os.path.join(ROOT_DIR, 'src', 'w_useless.txt')
USEFUL_FILE       = os.path.join(ROOT_DIR, 'src', 'w_useful.txt')
KEYPREFS_FILE     = os.path.join(ROOT_DIR, 'src', 'keywords.txt')
BLACKLIST_FILE    = os.path.join(ROOT_DIR, 'src', 'blacklist.txt')
STOPWORDS_FILE    = os.path.join(ROOT_DIR, 'src', 'stopwords.txt')
SYNCLUSTER_FILE   = os.path.join(ROOT_DIR, 'src', 'synonyms.txt')

HBAR_PNG    = os.path.join(IMG_DIR, 'hbar.png')
USER_PNG    = os.path.join(IMG_DIR, 'user.png')
MENTION_PNG = os.path.join(IMG_DIR, 'mention.png')
SVGMAP_PNG  = os.path.join(IMG_DIR, 'map.png')
HEATKW_PNG  = os.path.join(IMG_DIR, 'keyheatmap.png')
