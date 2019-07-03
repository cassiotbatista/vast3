from bokeh.core.properties import Instance, Override
from bokeh.models import HTMLBox, Slider

class Custom(HTMLBox):
    __implementation__ = 'custom.ts'

    slider = Instance(Slider)
    margin = Override(default=5)
