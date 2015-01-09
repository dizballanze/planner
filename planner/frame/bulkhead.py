from planner.frame.figure import Figure
from svgwrite import shapes
from planner.tools import parse_measure_units


class Bulkhead(Figure):

    """
    Inner walls representation.
    Only horizontal and vertical bulkheads supported for now.
    """

    DEFAULT_PARAMS = {"stroke": "#000", "stroke-width": "2", "fill": "#fff"}

    def __init__(self, left_top_point, right_bottom_point, **attribs):
        """
        left_top_point - coordinates of left-top Bulkhead corner
        right_bottom_point - coordinates of right-bottom Bulkhead corner
        """
        self.x = left_top_point[0]
        self.y = left_top_point[1]
        self.width = right_bottom_point[0] - left_top_point[0]
        self.height = right_bottom_point[1] - left_top_point[1]
        self.attribs = attribs

    def _draw(self):
        # Prepare border
        border_params = self.DEFAULT_PARAMS.copy()
        border_params.update(self.attribs)
        border_params['fill'] = '#fff'  # For border stroke background should be white
        border = shapes.Rect((self.x, self.y), (self.width, self.height), **border_params)
        res = [border]
        # Prepare background
        stroke_width = border_params.get('stroke-width')
        value, unit = parse_measure_units(stroke_width)
        bg_params = self.DEFAULT_PARAMS.copy()
        bg_params.update(self.attribs)
        del bg_params['stroke-width']
        del bg_params['stroke']
        # Hatching and filling
        if hasattr(self, "hatch") and self.hatch:
            bg_params['style'] = "fill: url(#{})".format(self._hatching_id)
            res.append(self.hatch)
        if hasattr(self, "filling"):
            bg_params['fill'] = self.filling
        else:
            if 'fill' not in bg_params:
                bg_params['fill'] = "#fff"
        background = shapes.Rect(
            (self.x + float(value) / 2, self.y + float(value) / 2),
            (self.width - value, self.height - value), **bg_params)
        res.append(background)
        return res
