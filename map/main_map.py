from bokeh.layouts import layout, row
from bokeh.io import curdoc
from bokeh.models.widgets import Div, Button
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.models import ResetTool, HoverTool

import re
from termcolor import cprint

from svg import SVG

svg = SVG()
def file_callback():
    svg.change_fill_color('oldtown', 'ff0000')
    svg.update_svg_text()
    notification = Div(text=svg.get_text(), width=550, height=500)
    layout = curdoc().get_model_by_name('mainLayout')
    layout.children.pop()
    layout.children.append(notification)

button_2 = Button(label="vai caralho")
button_2.on_click(file_callback)

# put the results in a row
notification = Div(text=svg.raw_text, width=50, height=50)

f = figure(x_range = [], plot_height=250, title="Some Plot", toolbar_location=None, tools="", name = 'plot')

lay = row(button_2, f, width=800,name='mainLayout')
lay.children.pop()
lay.children.append(notification)

curdoc().add_root(lay)
