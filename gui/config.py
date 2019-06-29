from termcolor import cprint

TAG = 'cfg'

DO_LEMMATIZE = False
if not DO_LEMMATIZE:
    cprint('%s: lemmatize will be skipped to speed up the process' % TAG, 
            'red', attrs=['bold'])

NUM_WORDS = 10
MIN_WLEN  = 3

SVGFILE = '../MC3/maps/custom/neigh_labels.svg'

DATA_CSVFILE = '../MC3/data/YInt.csv'
REPLACE_FILE = '../src/replace.txt'
USELESS_FILE = '../src/w_useless.txt'
USEFUL_FILE  = '../src/w_useful.txt'
