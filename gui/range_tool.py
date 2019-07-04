import numpy as np

from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool, Range1d
from bokeh.plotting import figure
from bokeh.sampledata.stocks import AAPL

dates = np.array(AAPL['date'], dtype=np.datetime64)
closes = AAPL['adj_close']
source = ColumnDataSource(data=dict(date=dates, close=closes))

select = figure(
        title="Drag the middle and edges of the selection box",
        plot_height=130, plot_width=800, 
        tools="", toolbar_location=None,
        #y_range=p.y_range, y_axis_type=None,
        x_axis_type="datetime",
        background_fill_color="#efefef")

range_tool = RangeTool(x_range=Range1d(dates[1500], dates[2500]))
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('date', 'close', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

show(column(select))
