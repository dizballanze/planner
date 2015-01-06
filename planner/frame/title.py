from planner.frame.polygon import Polygon
from svgwrite import shapes, text


class SampleTitle(Polygon):

    """
    Sample title block.
    """

    LINE_ATTRIBS = {"stroke-width": 0.5, "stroke": "#000", "fill-opacity": 0}
    DEFAULT_LABEL_ATTRIBS = {"font-size": 7, "text-anchor": "middle", "font-family": "Arial"}

    def __init__(self, width, height, title="Sample drawning"):
        self.width = width
        self.height = height
        self.title = title

    def _get_table_line(self, start, end):
        """
        Create table line with relative coordinates
        """
        base = (self.width - 10 - 185, self.height - 10 - 55)
        return shapes.Line((start[0] + base[0], start[1] + base[1]),
                           (end[0] + base[0], end[1] + base[1]), **self.LINE_ATTRIBS)

    def _draw(self):
        res = []
        # Borders
        left_top = (20, 10)
        right_top = (self.width - 10, 10)
        left_bottom = (20, self.height - 10)
        right_bottom = (self.width - 10, self.height - 10)
        res.append(shapes.Polygon([left_top, right_top, right_bottom, left_bottom, left_top], **self.LINE_ATTRIBS))
        # Title table
        title_insert_point = (self.width - 10 - 185, self.height - 10 - 55)
        res.append(shapes.Rect(title_insert_point, (185, 55), **self.LINE_ATTRIBS))
        res.append(self._get_table_line((0, 5), (65, 5)))
        res.append(self._get_table_line((0, 10), (65, 10)))
        res.append(self._get_table_line((0, 15), (185, 15)))
        res.append(self._get_table_line((0, 20), (65, 20)))
        res.append(self._get_table_line((0, 25), (65, 25)))
        res.append(self._get_table_line((0, 30), (65, 30)))
        res.append(self._get_table_line((0, 35), (65, 35)))
        res.append(self._get_table_line((0, 40), (185, 40)))
        res.append(self._get_table_line((0, 45), (65, 45)))
        res.append(self._get_table_line((0, 50), (65, 50)))

        res.append(self._get_table_line((7, 0), (7, 25)))
        res.append(self._get_table_line((17, 0), (17, 55)))
        res.append(self._get_table_line((40, 0), (40, 55)))
        res.append(self._get_table_line((55, 0), (55, 55)))
        res.append(self._get_table_line((65, 0), (65, 55)))
        res.append(self._get_table_line((135, 15), (135, 55)))

        res.append(self._get_table_line((135, 20), (185, 20)))
        res.append(self._get_table_line((135, 35), (185, 35)))

        res.append(self._get_table_line((140, 20), (140, 35)))
        res.append(self._get_table_line((145, 20), (145, 35)))
        res.append(self._get_table_line((150, 15), (150, 35)))
        res.append(self._get_table_line((167, 15), (167, 35)))
        res.append(self._get_table_line((155, 35), (155, 40)))

        # Text
        res.append(text.Text(self.title,
                   (title_insert_point[0] + 100, title_insert_point[1] + 30), **self.DEFAULT_LABEL_ATTRIBS))
        return res
