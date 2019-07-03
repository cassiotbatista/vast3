from bokeh.plotting import figure, output_file, show

plot = figure(plot_width=300, plot_height=300)
plot.varea(x=[1, 2, 3, 4], y1=[0, 0, 0, 0], 
        y2=[1, 3, 2, 4],         fill_color="red", alpha=0.2)
plot.varea(x=[1, 2, 3, 4], y1=[0, 0, 0, 0], 
        y2=[1/2, 3/2, 2/2, 4/2], fill_color="red", alpha=0.25)
plot.varea(x=[1, 2, 3, 4], y1=[0, 0, 0, 0], 
        y2=[1/4, 3/4, 2/4, 4/4], fill_color="red", alpha=0.3)
plot.varea(x=[1, 2, 3, 4], y1=[0, 0, 0, 0], 
        y2=[1/8, 3/8, 2/8, 4/8], fill_color="red", alpha=0.35)
show(plot)