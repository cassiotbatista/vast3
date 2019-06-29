from svgpathtools import svg2paths

class SVG:
    SVGFILE = '../MC3/maps/cassomap.svg'
    def __init__(self):
        super(SVG, self).__init__()
        self.raw_text = self.load()
        self.paths, self.attrs, self.metadata = svg2paths(
                        self.SVGFILE, return_svg_attributes=True)
        self.svg = self.split_attrs()

    def load(self):
        with open(self.SVGFILE, 'r') as f:
            svg = f.read()
        return svg

    def split_attrs(self):
        svg = {}
        for pathtag in self.attrs:
            identifier = pathtag['id']
            svg[identifier] = {}
            for key, value in pathtag.items():
                if key != 'id':
                    svg[identifier][key] = value
        return svg

    def join_attrs(self):
        svg = {}
        for pathtag in self.attrs:
            identifier = pathtag['id']
            svg[identifier] = {}
            for key, value in pathtag.items():
                if key != 'id':
                    svg[identifier][key] = value
        return svg
