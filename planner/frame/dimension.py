from svgwrite import shapes


class BaseDimension(object):

    """
    Abstract base class for dimensions objects
    """

    DEFAULT_ATTRIBS = {"stroke-width": "0.5", "stroke": "#000000"}
    DEFAULT_ARROW_ATTRIBS = {"fill": "#000000"}
    DEFAULT_FONT = ""
    ARROW_LENGTH = 6
    ARROW_WIDTH = 2

    def __init__(self, start_point, end_point, label, font=None, **attribs):
        self.start_point = start_point
        self.end_point = end_point
        self.label = label
        self.attribs = self.DEFAULT_ATTRIBS
        self.attribs.update(attribs)
        self.font = font or self.DEFAULT_FONT

    def _get_middle_point(self, start_point, end_point, distance):
        """
        Calculate point on line specified with 2 points on specified distance.
        """
        x1, y1 = start_point
        x2, y2 = end_point
        line_length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        directing_vector = (x2 - x1, y2 - y1)
        unit_vector = (directing_vector[0] / line_length, directing_vector[1] / line_length)
        middle_point = (x1 + unit_vector[0] * distance, y1 + unit_vector[1] * distance)
        return middle_point

    def _create_arrow(self, start_point, end_point, middle_point, **attribs):
        """
        Create arrow svg object from 3 points specified.
        """
        x1, y1 = start_point
        x2, y2 = end_point
        k = (y2 - y1) / (x2 - x1)
        kp = -(1 / k)
        xp = middle_point[0] + 1  # arbitrary selected x coord for perpendicular line
        yp = kp * (xp - middle_point[0]) + middle_point[1]
        directing_vector_p = (middle_point[0] - xp, middle_point[1] - yp)
        line_length_p = ((middle_point[0] - xp) ** 2  + (middle_point[1] - yp) ** 2) ** 0.5
        unit_vector_p = (directing_vector_p[0] / line_length_p, directing_vector_p[1] / line_length_p)
        tail1 = (middle_point[0] + unit_vector_p[0] * self.ARROW_WIDTH, middle_point[1] + unit_vector_p[1] * self.ARROW_WIDTH)
        tail2 = (middle_point[0] - unit_vector_p[0] * self.ARROW_WIDTH, middle_point[1] - unit_vector_p[1] * self.ARROW_WIDTH)
        attribs_merged = self.DEFAULT_ARROW_ATTRIBS
        attribs_merged.update(attribs)
        return shapes.Polygon([start_point, tail1, tail2, start_point], **attribs_merged)

    def _draw(self):
        """
        SVG draw logic.
        """
        raise NotImplementedError("Draw method is not yet implemented")

    def _mask(self):
        return False


class LinearDimension(BaseDimension):

    """
    Linear dimensions.
    """

    def __init__(self, start_point, end_point, label, font=None, direction=None, **attribs):
        super(LinearDimension, self).__init__(start_point, end_point, label, font, **attribs)
        self.direction = direction

    def _draw(self):
        res = []
        start_middle_point = self._get_middle_point(self.start_point, self.end_point, self.ARROW_LENGTH)
        end_middle_point = self._get_middle_point(self.end_point, self.start_point, self.ARROW_LENGTH)
        # Prepare svg elements
        arrow_start = self._create_arrow(self.start_point, self.end_point, start_middle_point)
        arrow_end = self._create_arrow(self.end_point, self.start_point, end_middle_point)
        line = shapes.Line(start_middle_point, end_middle_point, **self.attribs)
        # Create list with correct sequence of svg objects
        res.append(line)
        res.append(arrow_start)
        res.append(arrow_end)
        return res
