from bokeh.layouts import layout, row
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Div, Button, RadioButtonGroup, Select, Slider
from bokeh.events import ButtonClick
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.models import Range1d, PanTool, ResetTool, HoverTool, WheelZoomTool

import re
from termcolor import cprint

from svg import SVG

svg = SVG()
def file_callback():
    svg.svg_struct['oldtown']['style'] = re.sub('fill:#(.*?);', 
                    'fill:#ff0000;', svg.svg_struct['oldtown']['style'])
    notification = Div(text=svg.join_attrs(svg.svg_struct), width=550, height=500)
    layout = curdoc().get_model_by_name('mainLayout')
    layout.children.pop()
    layout.children.append(notification)

button_2 = Button(label="vai caralho")
button_2.on_click(file_callback)

# put the results in a row
notification = Div(text=svg.raw_text, width=550, height=500)

f = figure(x_range = [], plot_height=250, title="Some Plot", toolbar_location=None, tools="", name = 'plot')
f.vbar([], top=[], width=0.9, color=Spectral6)
f.y_range.start = 0
f.tools = [PanTool(),ResetTool()]
f.toolbar_location = 'above'
f.plot_width=800
f.plot_height=500

lay = row(button_2, f, width=800,name='mainLayout')
lay.children.pop()
lay.children.append(notification)

curdoc().add_root(lay)
curdoc().title = "Word Count"
