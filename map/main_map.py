from bokeh.layouts import widgetbox, layout, row
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Div, Button, RadioButtonGroup, Select, Slider
from bokeh.events import ButtonClick
import io
import base64
import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.models import Range1d, PanTool, ResetTool, HoverTool, WheelZoomTool

SVGFILE = '../MC3/maps/cassomap.svg'
with open(SVGFILE, 'r') as f:
    svg = f.read()

def file_callback():
    layout = curdoc().get_model_by_name('mainLayout')
    curdoc().title = "File Uploading....."
    layout.children.pop()
    layout.children.append(notification)

button_2 = Button(label="Plot")
button_2.on_click(file_callback)

# put the results in a row
notification = Div(text=svg, width=550,height=500) # display Processing...

f = figure(x_range = [], plot_height=250, title="Some Plot", toolbar_location=None, tools="", name = 'plot')
f.vbar([], top=[], width=0.9, color=Spectral6)
f.y_range.start = 0
f.tools = [PanTool(),ResetTool()]
f.toolbar_location = 'above'
f.plot_width=800
f.plot_height=500

lay = row(button_2, f, width=800,name='mainLayout')

curdoc().add_root(lay)
curdoc().title = "Word Count"
