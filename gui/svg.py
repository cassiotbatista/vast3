import sys
import os
import re
from svgpathtools import svg2paths

class SVG:
    SVGFILE = '../MC3/maps/cassomap.svg'
    def __init__(self):
        super(SVG, self).__init__()
        self.raw_text = self.load()
        self.svg_text = self.raw_text
        self.paths, self.attrs, self.metadata = svg2paths(
                        self.SVGFILE, return_svg_attributes=True)
        self.svg_struct = self.split_attrs(self.attrs)

    def load(self):
        with open(self.SVGFILE, 'r') as f:
            svg = f.read()
        return svg

    def split_attrs(self, attributes):
        if not isinstance(attributes, list):
            print('there\'s something really wrong around here')
        svg = {}
        for path_tag in attributes:
            identifier = path_tag['id']
            svg[identifier] = {}
            for key, value in path_tag.items():
                if key != 'id':
                    svg[identifier][key] = value
        return svg

    def join_attrs(self, svgdict):
        if not isinstance(svgdict, dict):
            print('there\'s something really wrong around here')
        svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + '\n'
        svg += '<svg' + '\n'
        for key, value in self.metadata.items():
            svg += '    %s="%s"' % (key, value) + '\n'
        svg = svg.rstrip() + '>' + '\n' 
        svg += '    <g>' + '\n' # FIXME I'm losing metadata here
        for identifier in svgdict:
            svg += '        <path id="%s"' % identifier + '\n'
            for key, value in svgdict[identifier].items():
                svg += '            %s="%s"' % (key, value) + '\n'
            svg = svg.rstrip() + '/>' + '\n' 
        svg += '    </g>' + '\n'
        svg += '</svg>'
        return svg

    def change_fill_color(self, neigh, html_code):
        self.svg_struct[neigh]['style'] = re.sub('fill:#(.*?);', 
                    'fill:#{};'.format(html_code.lower().strip('#')),
                    self.svg_struct[neigh]['style'])

    def update_svg_text(self):
        self.svg_text = self.join_attrs(self.svg_struct)

    def get_text(self):
        return self.svg_text

    def get_struct(self):
        return self.svg_struct
