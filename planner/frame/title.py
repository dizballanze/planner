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

    def _get_borders(self):
        left_top = (20, 10)
        right_top = (self.width - 10, 10)
        left_bottom = (20, self.height - 10)
        right_bottom = (self.width - 10, self.height - 10)
        return shapes.Polygon([left_top, right_top, right_bottom, left_bottom, left_top], **self.LINE_ATTRIBS)

    def _draw(self):
        res = []
        # Borders
        res.append(self._get_borders())
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


class SampleLogoTitle(SampleTitle):

    """
    Sample title block with logo.
    """

    DEFAULT_LABEL_ATTRIBS = {"font-size": 5, "text-anchor": "middle", "font-family": "Arial"}

    def __init__(self, width, height, title="Sample drawning",
                 project_title="Sample project", field_title="Date", field_value="01.08.2015"):
        super(SampleLogoTitle, self).__init__(width, height, title)
        self.project_title = project_title
        self.field_title = field_title
        self.field_value = field_value
        self._base_point = (20, self.height - 10 - 25)

    def _get_table_line(self, start, end):
        """
        Create table line with relative coordinates
        """
        return shapes.Line((start[0] + self._base_point[0], start[1] + self._base_point[1]),
                           (end[0] + self._base_point[0], end[1] + self._base_point[1]), **self.LINE_ATTRIBS)

    def _get_logo(self):
        """
        Return list of svg elements represented company logo
        """
        return None

    def _draw(self):
        res = []
        # Borders
        res.append(self._get_borders())
        # Title table
        res.append(self._get_table_line((0, 0), (self.width - 30, 0)))
        res.append(self._get_table_line((self.width - 30 - 65, 0), (self.width - 30 - 65, 25)))
        res.append(self._get_table_line((self.width - 30 - 165, 0), (self.width - 30 - 165, 25)))
        res.append(self._get_table_line((self.width - 30 - 265, 0), (self.width - 30 - 265, 25)))
        res.append(self._get_table_line((self.width - 30 - 245, 18), (self.width - 30 - 245, 25)))
        res.append(self._get_table_line((self.width - 30 - 265, 18), (self.width - 30 -165, 18)))
        # Text
        # project title
        project_title_insert_point = (self.width - 30 - 195, self._base_point[1] + 11)
        res.append(text.Text(self.project_title, project_title_insert_point, **self.DEFAULT_LABEL_ATTRIBS))
        # drawing title
        title_insert_point = (self.width - 30 - 95, self._base_point[1] + 15)
        res.append(text.Text(self.title, title_insert_point, **self.DEFAULT_LABEL_ATTRIBS))
        # field title
        field_title_insert_point = (self.width - 10 - 255, self._base_point[1] + 23)
        res.append(text.Text(self.field_title, field_title_insert_point, **self.DEFAULT_LABEL_ATTRIBS))
        # field value
        field_value_insert_point = (self.width - 10 - 205, self._base_point[1] + 23)
        res.append(text.Text(self.field_value, field_value_insert_point, **self.DEFAULT_LABEL_ATTRIBS))
        # Logo
        logo = self._get_logo()
        if logo is not None:
            res = res + logo
        return res
