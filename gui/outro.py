from __future__ import print_function

from datetime import date

from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.resources import INLINE
from bokeh.util.browser import view
from bokeh.models.layouts import Row, Column
from bokeh.models.widgets import DateRangeSlider

date_range_slider = DateRangeSlider(
            value  = (date(2014, 1, 1), date(2018, 12, 31)), 
            start  = date(2010, 1, 1), 
            end    = date(2020, 1, 1), 
            step   = 1)

sliders = Row(children=[
    Column(children=[
        date_range_slider,
    ]),
])

doc = Document()
doc.add_root(sliders)

if __name__ == "__main__":
    doc.validate()
    filename = "sliders.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "sliders"))
    view(filename)
