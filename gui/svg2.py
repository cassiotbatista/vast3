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
import config

INDENT_SIZE = 4

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

    def to_tag(self):
        print(INDENT_SIZE*' '*self.level, self.tag, ' ->', end='\t')
        print(self.metadata['id']) if 'id' in self.metadata else print()

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

if __name__=='__main__':
    doc  = minidom.parse(config.SVGFILE)
    root = doc.getElementsByTagName(config.SVG_NODE_HIERARCHY[0])[0]
    svg  = SVGNode(root)
    print(svg.to_string())
