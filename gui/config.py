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

from termcolor import cprint

TAG = 'cfg'

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

NUM_WORD_BARS = 10
PREFIX_LEN  = 3

MIN_NUM_TWEETS = 11
NUM_MENTIONS = 22

SVGFILE = '../MC3/maps/custom/neigh_labels.svg'
SVGTEST = '../MC3/maps/mapa_vast_vetorizado.svg'
SVG_NODE_HIERARCHY = ['svg', 'g', 'path', 'text', 'tspan']

DATA_SRC_CSVFILE  = '../MC3/data/YInt.csv'
DATA_PROC_CSVFILE = 'data/data.csv'
DATA_HORIZ_CSVFILE = 'data/out.csv'
REPLACE_FILE      = '../src/replace.txt'
USELESS_FILE      = '../src/w_useless.txt'
USEFUL_FILE       = '../src/w_useful.txt'
KEYPREFS_FILE     = '../src/keywords.txt'
BLACKLIST_FILE    = '../src/blacklist.txt'
STOPWORDS_FILE    = '../src/stopwords.txt'
