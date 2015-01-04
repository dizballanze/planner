"""
Structural object.
Container of all plan objects.
"""
from svgwrite import Drawing as SVGDrawing, mm


class Drawing(object):

    """ Container of plan objects """

    SIZES = {
        "A0": (1189, 841),
        "A1": (841, 594),
        "A2": (594, 420),
        "A3": (420, 297),
        "A4": (297, 210),
        "A5": (210, 148),
        "A6": (148, 105),
        "A7": (105, 74),
        "A8": (74, 52),
        "A9": (52, 37),
        "A10": (37, 26)}

    def __init__(self, size="A3"):
        """
         -  size can be:
             - tuple with 2 values (width, height)
             - series of size (ISO 216): A0-A10
        """
        # Save size of plan
        if size in Drawing.SIZES:
            self.size = Drawing.SIZES[size]
        else:
            self.size = size
        # Init container
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def __str__(self):
        draw = SVGDrawing(size=(self.size[0] * mm, self.size[1] * mm), profile='full', viewBox="0 0 {} {}".format(self.size[0], self.size[1]))
        for obj in self.objects:
            drawed = obj._draw()
            # object can consists of several objects
            if hasattr(drawed, '__iter__'):
                for svg_obj in drawed:
                    draw.add(svg_obj)
            else:
                draw.add(drawed)
            # object can contain masks or clips
            mask = obj._mask()
            if mask:
                draw.defs.add(mask)
        return draw.tostring()
