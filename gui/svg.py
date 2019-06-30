#!/usr/bin/env python3
#
# VAST Challenge 2019: Disaster at St. Himark!
# https://vast-challenge.github.io/2019/index.html
#
# Federal University of Pará (UFPA)
#
# author: june 2019
# cassio batista - cassio.batista.13@gmail.com
# edwin jueda - 
# erick campos - 

import sys
import os
import re
from svgpathtools import svg2paths

import config

class SVG:
    def __init__(self):
        super(SVG, self).__init__()
        self.raw_text = self.load()
        self.svg_text = self.raw_text
        self.paths, self.attrs, self.metadata = svg2paths(
                        config.SVGFILE, return_svg_attributes=True)
        self.svg_struct = self.split_attrs(self.attrs)

    def load(self):
        with open(config.SVGFILE, 'r') as f:
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

    def rescale(self, factor):
        if not isinstance(factor, float) or factor < 0 or factor > 1:
            print('it is wrong')
        meta_width  = self.metadata['width']
        meta_height = self.metadata['height']
        new_width  = float(re.search('^(.*?)mm$', meta_width).groups()[0])  * factor
        new_height = float(re.search('^(.*?)mm$', meta_height).groups()[0]) * factor
        self.metadata['width']  = '%.5fmm' % new_width
        self.metadata['height'] = '%.5fmm' % new_height

    def update_svg_text(self):
        self.svg_text = self.join_attrs(self.svg_struct)

    def get_text(self):
        return self.svg_text

    def get_struct(self):
        return self.svg_struct

    def get_paths(self):
        return self.paths
