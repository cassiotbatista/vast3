import numpy as np
from bokeh.plotting import figure, output_file
from bokeh.io import show
from bokeh.models import ColumnDataSource, Range1d, HoverTool
from bokeh.models.layouts import Column
from bokeh.palettes import Category10_6

NPOINTS = 100
PLOT_WIDTH  = 1200
PLOT_HEIGHT = 150
PLOT_ALPHA  = 0.7

source = ColumnDataSource(dict(
        x  = np.arange(NPOINTS),
        y1 = np.zeros(NPOINTS),
        y2 = np.random.rand(NPOINTS),
    ))

# first figure: vbar ######################################################
vbar_hover_at_fig = figure(plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, 
        toolbar_location='right',
        tools=[HoverTool(tooltips=[
                ('x', '@x'),
            ], point_policy='follow_mouse')])

vbar_hover_at_fig.vbar(x='x', top='y2', width=0.85,
               fill_color=Category10_6[0], fill_alpha=PLOT_ALPHA, source=source)

# second figure: vbar #####################################################
vbar_hover_per_render = figure(plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, 
        toolbar_location='right')

renderer = vbar_hover_per_render.vbar(x='x', top='y2', width=0.85,
               fill_color=Category10_6[1], fill_alpha=PLOT_ALPHA, source=source)

hover = HoverTool(tooltips=[
        ('y','@y2')
    ], renderers=[renderer])
vbar_hover_per_render.add_tools(hover)

# third figure: varea #####################################################
varea_hover_at_fig = figure(plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, 
        toolbar_location='right',
        tools=[HoverTool(tooltips=[
                ('x', '@x'),
            ], point_policy='follow_mouse')])

varea_hover_at_fig.varea(x='x', y1='y1', y2='y2',
               fill_color=Category10_6[2], fill_alpha=PLOT_ALPHA, source=source)

# fourth figure: varea #####################################################
varea_hover_per_render = figure(plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, 
        #tools='hover', tooltips=[('y','@y2')], # TODO: comment?
        toolbar_location='right')

renderer2 = varea_hover_per_render.varea(x='x', y1='y1', y2='y2', 
        fill_color=Category10_6[3], fill_alpha=PLOT_ALPHA, source=source)

hover2 = HoverTool(tooltips=[
        ('y','@y2')
    ], renderers=[renderer2])
varea_hover_per_render.add_tools(hover2)

# fifth figure: line ######################################################
line_hover_at_fig = figure(plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, 
        toolbar_location='right',
        tools=[HoverTool(tooltips=[
                ('x', '@x'),
            ], point_policy='follow_mouse')])

line_hover_at_fig.line(x='x', y='y2', line_width=5.00,
               line_color=Category10_6[4], line_alpha=PLOT_ALPHA, source=source)

# sixt figure: line #####################################################
line_hover_per_render = figure(plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, 
        toolbar_location='right')

renderer3 = line_hover_per_render.line(x='x', y='y2', line_width=5.00,
               line_color=Category10_6[5], line_alpha=PLOT_ALPHA, source=source)

hover3 = HoverTool(tooltips=[
        ('y','@y2')
    ], renderers=[renderer3])
line_hover_per_render.add_tools(hover3)

###########################################################################
lay = Column(children=[
        vbar_hover_at_fig,
        vbar_hover_per_render,
        varea_hover_at_fig,
        varea_hover_per_render,
        line_hover_at_fig,
        line_hover_per_render,
    ])

show(lay)
