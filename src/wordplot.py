import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def transform_format(val):
	if val == 0:
		return 255
	else:
		return val

wine_mask = np.array(Image.open("map_white.png"))
data = pd.read_csv('../MC3/data/YInt.csv')

contas = data.account.values

users = ' '.join(map(str, contas))


words = \
	'grafemas graphemes ' + \
	'palavras words ' + \
	'frases phrases ' + \
	'fonemas phonemes ' + \
	'sílaba syllables ' + \
	'vogal vowel ' + \
	'consoantes consonants ' + \
	'conversor converter ' + \
	'separador ' + \
	'alinhador aligner ' + \
	'fonético phonetic ' + \
	'regras rules ' + \
	'tônica stress ' + \
	'gramática grammar ' + \
	'NLP NLP NLP NLP NLP NLP' + \
	'processamento processamento processamento ' + \
	'linguagem linguagem linguagem ' + \
	'natural natural natural ' + \
	'expressão expression regular ' + \
	'aprendizado learning ' + \
	'conhecimento knowledge ' + \
	'Português Brasileiro ' + \
	'Brazilian Portuguese ' + \
	'Universidade Federal Pará Belém UFPA UFPA ' + \
	'automático automatic ' + \
	'token tagger label classe ' + \
	'extração extraction probabilidade probability' 



wordcloud = WordCloud(max_font_size=200, max_words=100, mode='RGB',
	mask=wine_mask,
	colormap=plt.cm.Set1,
	contour_width=8, contour_color='firebrick',
	background_color="white").generate(users)

# Display the generated image:
#plt.figure(figsize=(4.8,4.8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
plt.show()

