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

from xml.dom import minidom
import re

import config

class SVG:
    def __init__(self):
        super(SVG, self).__init__()
        doc  = minidom.parse(config.SVGFILE)
        root = doc.getElementsByTagName(config.SVG_NODE_HIERARCHY[0])[0]
        self.svg = SVGNode(root)

    def rescale(self, factor):
        self.svg.rescale(factor)

    def to_string(self):
        return self.svg.to_string()

    def change_fill_color(self, neigh, html_code):
        path = self.svg.find_path_by_id(self.svg, neigh)
        path.metadata['style']['fill'] = html_code.lower()

class SVGNode:
    def __init__(self, root):
        super(SVGNode, self).__init__()
        self.root     = root
        self.tag      = self.root.nodeName
        self.metadata = {}
        self.children = []
        self.level    = 0

        if isinstance(self.root, minidom.Element):
            self.level = config.SVG_NODE_HIERARCHY.index(self.tag)
            if self.root.hasAttributes():
                self.metadata = dict(self.root.attributes.items())
        elif isinstance(self.root, minidom.Text):
            self.level = config.SVG_NODE_HIERARCHY.index('tspan') + 1
            self.metadata['text'] = self.root.data

        if 'style' in self.metadata:
            self.metadata['style'] = dict(tuple(pair.split(':')) \
                    for pair in self.metadata['style'].split(';'))

        if self.root.hasChildNodes():
            for child in self.root.childNodes:
                if isinstance(child, minidom.Element):
                    self.children.append(SVGNode(child))
                elif isinstance(child, minidom.Text):
                    if self.tag == 'tspan':
                        self.children.append(SVGNode(child))

    # NOTE: assumes 'mm' as universal unit
    def rescale(self, factor):
        if not isinstance(factor, float) or factor < 0 or factor > 1:
            print('it is wrong')
        self.metadata['width']  = '%.5fmm' % (factor * \
                    float(re.findall('\d+.\d+', self.metadata['width'])[0]))
        self.metadata['height'] = '%.5fmm' % (factor * \
                    float(re.findall('\d+.\d+', self.metadata['height'])[0]))

    def to_tag(self):
        string = '%s -> %s \n' %(self.tag, self.metadata['id'] if 'id' in self.metadata else self.metadata['text'])
        for child in self.children:
            string += child.to_tag()
        return string

    def to_string(self):
        if 'text' in self.metadata:
            return self.metadata['text'] 
        indent = '\t' * self.level
        string = indent + '<' + self.tag + '\n'
        indent += '\t'
        for key, value in self.metadata.items():
            if key == 'style':
                string += indent + '%s="' % key
                for k, v in value.items():
                    string += '%s:%s;' % (k,v)
                string += '"\n'
                continue
            string += indent +  '%s="%s"\n' % (key, value)
        string = string.rstrip() + '>'
        if self.tag != 'tspan':
            string += '\n'
        for child in self.children:
            string += child.to_string()
        indent = '\t' * self.level
        if self.tag == 'text' or self.tag == 'tspan':
            indent = ''
        string += indent + '</' + self.tag + '>'
        if self.tag != 'tspan':
            string += '\n'
        return string

    def find_path_by_id(self, node, idd):
        for child in node.children:
            if child.tag == 'path' and child.metadata['id'] == idd:
                return child
        for child in node.children:
            return self.find_path_by_id(child, idd)

if __name__=='__main__':
    doc  = minidom.parse(config.SVGFILE)
    root = doc.getElementsByTagName(config.SVG_NODE_HIERARCHY[0])[0]
    svg  = SVGNode(root)
    print(svg.to_tag())
