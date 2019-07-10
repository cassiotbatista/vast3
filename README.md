# Disaster at St. Himark! VAST 2019 Mini Challenge 3
This repo hosts the tools that were exclusively built to answer the questions of 
the [3rd mini-challenge](https://vast-challenge.github.io/2019/MC3.html) of the 
2019 version of the [VAST Challenge](https://vast-challenge.github.io/2019/).

![1st tool](screenshots/grafico1.gif)

![2nd tool](screenshots/grafico2.gif)

## Execution Instructions
```
$ bokeh serve --show <DIR>
```
where `<DIR>` can be either `grafico1/` or `gui/`.

## Tools and Libraries
- [Python](https://www.python.org/downloads/) (v3.5.3)
- [Bokeh](https://bokeh.pydata.org/en/latest/) (v1.2.0)
- [NLTK](https://www.nltk.org/) (v3.4.1)
- [TextBlob](https://textblob.readthedocs.io/en/dev/) (v0.15.3)
- [NumPy](https://www.numpy.org/) (v1.16.0)
- [pandas](https://pandas.pydata.org/) (v0.24.2)
- [Matplotlib](https://matplotlib.org/) (v3.0.2)
- [word_cloud](https://github.com/amueller/word_cloud) (v1.5.0)
- [scikit-learn](https://scikit-learn.org/stable/) (v0.20.2)
- [Node.js](https://nodejs.org/en/download/) (v10.16.0)
- [PhantomJS](https://phantomjs.org/) (v2.1.1) ([wget](https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2))
- [Selenium](https://selenium-python.readthedocs.io/) (v3.141.0)
- [termcolor](https://pypi.org/project/termcolor/) (v1.1.0)

## Browsers
- [Google Chrome](https://www.google.com/chrome/) (v75.0.3770.100)

## OS
- Debian Stretch 9.9 :penguin:

## Instalation (Debian)
```bash
$ sudo apt-get install python3 python3-pip
$ sudo -H pip3 install --upgrade pip
$ sudo -H pip3 install --upgrade \
    bokeh nltk pandas numpy matplotlib termcolor sklearn textblob wordcloud selenium
```
:warning: **Node.js** must be downloaded from browser, extracted and then
manually copied (with root permissions) to `/usr/bin`.

:warning: **PhantomJS** must be downloaded from browser, extracted and then
manually copied (with root permissions) to `/usr/bin`.

## Authors:
- Ana Larissa Dias - larissa.engcomp@gmail.com
- Cassio Batista   - cassio.batista.13@gmail.com 
- Edwin Rueda      - ejrueda95g@gmail.com
- Erick Campos     - erick.c.modesto@gmail.com
