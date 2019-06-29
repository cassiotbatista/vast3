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

    def join_attrs(self, svg_structure):
        if not isinstance(svg_structure, dict):
            print('there\'s something really wrong around here')
        svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + '\n'
        svg += '<svg' + '\n'
        for key, value in self.metadata.items():
            svg += '    %s="%s"' % (key, value) + '\n'
        svg = svg.rstrip() + '>' + '\n' 
        svg += '    <g>' + '\n' # FIXME I'm losing metadata here
        for identifier in svg_structure:
            svg += '        <path id="%s"' % identifier + '\n'
            for key, value in svg_structure[identifier].items():
                svg += '            %s="%s"' % (key, value) + '\n'
            svg = svg.rstrip() + '/>' + '\n' 
        svg += '    </g>' + '\n'
        svg += '</svg>'
        return svg
