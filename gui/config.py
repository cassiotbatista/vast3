from termcolor import cprint

TAG = 'cfg'

DO_LEMMATIZE = False
if not DO_LEMMATIZE:
    cprint('%s: lemmatize will be skipped to speed up processing' % TAG, 
            'red', attrs=['bold'])

NUM_WORDS = 10
MIN_WLEN  = 3

SVGFILE = '../MC3/maps/cassomap.svg'

DATA_CSVFILE = '../MC3/data/YInt.csv'
REPLACE_FILE = '../src/replace.txt'
USELESS_FILE = '../src/w_useless.txt'
USEFUL_FILE  = '../src/w_useful.txt'
