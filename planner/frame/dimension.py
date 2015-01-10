from planner.frame.figure import Figure
from svgwrite import shapes, text, path, container
import math


class BaseDimension(Figure):

    """
    Abstract base class for dimensions objects
    """

    DEFAULT_ATTRIBS = {"stroke-width": "0.5", "stroke": "#000000"}
    DEFAULT_ARROW_ATTRIBS = {"fill": "#000000"}
    DEFAULT_LABEL_ATTRIBS = {"font-size": "4", "text-anchor": "middle", "font-family": "Arial"}
    ARROW_LENGTH = 6
    ARROW_WIDTH = 1.5
    ARROW_PADDING = 1

    def __init__(self, start_point, end_point, label, label_attribs=None, **attribs):
        self.start_point = start_point
        self.end_point = end_point
        self.label = label
        self.attribs = self.DEFAULT_ATTRIBS
        self.attribs.update(attribs)
        self.label_attribs = label_attribs or {}

    def _get_length(self, p1, p2):
        return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

    def _get_middle_point(self, start_point, end_point, distance=None):
        """
        Calculate point on line specified with 2 points on specified distance.
        If `distance == None` it calculated as `length / 2`
        """
        x1, y1 = start_point
        x2, y2 = end_point
        line_length = self._get_length(start_point, end_point)
        if distance is None:
            distance = line_length / 2
        directing_vector = (x2 - x1, y2 - y1)
        unit_vector = (directing_vector[0] / line_length, directing_vector[1] / line_length)
        middle_point = (x1 + unit_vector[0] * distance, y1 + unit_vector[1] * distance)
        return middle_point

    def _get_perpendicular_unit_vector(self, start_point, end_point, middle_point):
        x1, y1 = start_point
        x2, y2 = end_point
        if (x2 - x1) != 0:
            k = (y2 - y1) / (x2 - x1)
            if k != 0:
                k = -(1 / k)
                x = middle_point[0] + 1  # arbitrary selected x coord for perpendicular line
                y = k * (x - middle_point[0]) + middle_point[1]
            else:
                x = middle_point[0]
                y = middle_point[1] + 1
        else:
            x = middle_point[0] + 1
            y = middle_point[1]
        directing_vector = (middle_point[0] - x, middle_point[1] - y)
        line_length = self._get_length((x, y), middle_point)
        unit_vector = (directing_vector[0] / line_length, directing_vector[1] / line_length)
        return unit_vector

    def _create_arrow(self, start_point, end_point, middle_point, **attribs):
        """
        Create arrow svg object from 3 points specified.
        """
        unit_vector_p = self._get_perpendicular_unit_vector(start_point, end_point, middle_point)
        tail1 = (middle_point[0] + unit_vector_p[0] * self.ARROW_WIDTH,
                 middle_point[1] + unit_vector_p[1] * self.ARROW_WIDTH)
        tail2 = (middle_point[0] - unit_vector_p[0] * self.ARROW_WIDTH,
                 middle_point[1] - unit_vector_p[1] * self.ARROW_WIDTH)
        attribs_merged = self.DEFAULT_ARROW_ATTRIBS
        attribs_merged.update(attribs)
        return shapes.Polygon([start_point, tail1, tail2, start_point], **attribs_merged)

    def _render_text(self, start_point, end_point, padding=True):
        middle_point = self._get_middle_point(start_point, end_point)
        attribs = self.DEFAULT_LABEL_ATTRIBS.copy()
        attribs.update(self.label_attribs)
        if (end_point[0] - start_point[0]) != 0:
            tan_angle = (end_point[1] - start_point[1]) / (end_point[0] - start_point[0])
            angle = math.degrees(math.atan(tan_angle))
        else:
            angle = -90
        unit_vector = self._get_perpendicular_unit_vector(start_point, end_point, middle_point)
        if padding:
            draw_text_center_point = (middle_point[0] + unit_vector[0] * self.ARROW_PADDING,
                                      middle_point[1] + unit_vector[1] * self.ARROW_PADDING)
        else:
            draw_text_center_point = middle_point
        attribs['transform'] = "rotate({}, {}, {})".format(angle, draw_text_center_point[0], draw_text_center_point[1])
        return text.Text(self.label, draw_text_center_point, **attribs)

    def _draw(self):
        """
        SVG draw logic.
        """
        raise NotImplementedError("Draw method is not yet implemented")


class LinearDimension(BaseDimension):

    """
    Linear dimensions.
    """

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
        res.append(self._render_text(self.start_point, self.end_point))
        return res


class ExtensionableLinearDimension(BaseDimension):

    """
    Linear dimensions with extension lines.
    """

    EXTENSION_TAIL = 2

    def __init__(self, start_point, end_point, label, font=None, direction=1, extension_size=12, **attribs):
        """
        `direction` argument sets extension lines direction:
            direction >= 0 - extension lines in coordinates increase direction
            direction < 0 - extension lines in coordinates decrease direction
        """
        super(ExtensionableLinearDimension, self).__init__(start_point, end_point, label, font, **attribs)
        self._direction = direction >= 0
        self.extension_size = extension_size

    def _draw(self):
        res = []
        # Draw lines
        unit_vector = self._get_perpendicular_unit_vector(self.start_point, self.end_point, self.start_point)
        # inverse unit vector if needed
        if self._direction:
            unit_vector = [-part for part in unit_vector]
        start_extension_point = (self.start_point[0] + unit_vector[0] * self.extension_size,
                                 self.start_point[1] + unit_vector[1] * self.extension_size)
        end_extension_point = (self.end_point[0] + unit_vector[0] * self.extension_size,
                               self.end_point[1] + unit_vector[1] * self.extension_size)
        start_extension_line = shapes.Line(self.start_point, start_extension_point, **self.attribs)
        end_extension_line = shapes.Line(self.end_point, end_extension_point, **self.attribs)
        dimension_size = self.extension_size - self.EXTENSION_TAIL
        start_dimension_point = (self.start_point[0] + unit_vector[0] * dimension_size,
                                 self.start_point[1] + unit_vector[1] * dimension_size)
        end_dimension_point = (self.end_point[0] + unit_vector[0] * dimension_size,
                               self.end_point[1] + unit_vector[1] * dimension_size)
        dimension_line = shapes.Line(start_dimension_point, end_dimension_point, **self.attribs)
        res += [start_extension_line, end_extension_line, dimension_line]
        # Draw arrows
        start_arrow_point = self._get_middle_point(start_dimension_point, end_dimension_point, self.ARROW_LENGTH)
        end_arrow_point = self._get_middle_point(end_dimension_point, start_dimension_point, self.ARROW_LENGTH)
        res.append(self._create_arrow(start_dimension_point, end_dimension_point, start_arrow_point))
        res.append(self._create_arrow(end_dimension_point, start_dimension_point, end_arrow_point))
        # Draw text
        res.append(self._render_text(start_dimension_point, end_dimension_point))
        return res


class TinyExtensionableLinearDimension(ExtensionableLinearDimension):

    """
    Tiny linear dimension, label located on the outter part of
        elongate dimension line.
    """

    def __init__(self, start_point, end_point, label, font=None, direction=1,
                 extension_size=12, label_position='start', elongation=15, **attribs):
        """
        `direction` argument sets extension lines direction:
            direction >= 0 - extension lines in coordinates increase direction
            direction < 0 - extension lines in coordinates decrease direction
        `label_position` - define position of label on elongate dimension line:
            label_position == 'start' - label located close to start_point
            label_position != 'start' - label located close to end_point
        """
        super(TinyExtensionableLinearDimension, self).__init__(
            start_point, end_point, label, font, direction, extension_size, **attribs)
        self._start_position = label_position == 'start'
        self.elongation = elongation

    def _draw(self):
        res = []
        # Draw lines
        unit_vector = self._get_perpendicular_unit_vector(self.start_point, self.end_point, self.start_point)
        # inverse unit vector if needed
        if self._direction:
            unit_vector = [-part for part in unit_vector]
        start_extension_point = (self.start_point[0] + unit_vector[0] * self.extension_size,
                                 self.start_point[1] + unit_vector[1] * self.extension_size)
        end_extension_point = (self.end_point[0] + unit_vector[0] * self.extension_size,
                               self.end_point[1] + unit_vector[1] * self.extension_size)
        start_extension_line = shapes.Line(self.start_point, start_extension_point, **self.attribs)
        end_extension_line = shapes.Line(self.end_point, end_extension_point, **self.attribs)
        dimension_size = self.extension_size - self.EXTENSION_TAIL
        start_dimension_middle_point = (self.start_point[0] + unit_vector[0] * dimension_size,
                                        self.start_point[1] + unit_vector[1] * dimension_size)
        end_dimension_middle_point = (self.end_point[0] + unit_vector[0] * dimension_size,
                                      self.end_point[1] + unit_vector[1] * dimension_size)
        if self._start_position:
            start_dimension_point = self._get_middle_point(
                start_dimension_middle_point, end_dimension_middle_point, -(self.elongation + self.ARROW_LENGTH))
            end_dimension_point = self._get_middle_point(
                end_dimension_middle_point, start_dimension_middle_point, -(self.ARROW_LENGTH + 2))
        else:
            end_dimension_point = self._get_middle_point(
                end_dimension_middle_point, start_dimension_middle_point, -(self.elongation + self.ARROW_LENGTH))
            start_dimension_point = self._get_middle_point(
                start_dimension_middle_point, end_dimension_middle_point, -(self.ARROW_LENGTH + 2))
        dimension_line = shapes.Line(start_dimension_point, end_dimension_point, **self.attribs)
        res += [start_extension_line, end_extension_line, dimension_line]
        # Draw arrows
        start_arrow_point = self._get_middle_point(
            start_dimension_middle_point, start_dimension_point, self.ARROW_LENGTH)
        end_arrow_point = self._get_middle_point(end_dimension_middle_point, end_dimension_point, self.ARROW_LENGTH)
        res.append(self._create_arrow(start_dimension_middle_point, start_dimension_point, start_arrow_point))
        res.append(self._create_arrow(end_dimension_middle_point, end_dimension_point, end_arrow_point))
        # Draw text
        if self._start_position:
            start_text_point = start_dimension_point
            end_text_point = start_arrow_point
        else:
            start_text_point = end_arrow_point
            end_text_point = end_dimension_point
        res.append(self._render_text(start_text_point, end_text_point))
        return res


class AngleDimension(BaseDimension):

    """
    Angle dimension without extension lines.
    """

    DEFAULT_ATTRIBS = {"stroke-width": "0.5", "stroke": "#000000", "fill-opacity": "0", "stroke-linecap": "butt"}

    def get_marker_id(self, position):
        return "marker-{}-{}".format(position, self.uuid)

    def _defs(self):
        markers = []
        marker_start = container.Marker(size=(self.ARROW_LENGTH, self.ARROW_WIDTH * 2),
                                        id=self.get_marker_id('start'), orient="auto", refX=0, refY=self.ARROW_WIDTH)
        marker_start.add(
            path.Path(["M", (0, self.ARROW_WIDTH), (self.ARROW_LENGTH, 0), (self.ARROW_LENGTH, self.ARROW_WIDTH * 2),
                      (0, self.ARROW_WIDTH)], **{"stroke": "#000", "stroke-width": 0.5}))
        markers.append(marker_start)
        marker_end = container.Marker(size=(self.ARROW_LENGTH, self.ARROW_WIDTH * 2), id=self.get_marker_id('end'),
                                      orient="auto", refX=self.ARROW_LENGTH, refY=self.ARROW_WIDTH)
        marker_end.add(
            path.Path(["M", (0, 0), (0, self.ARROW_WIDTH * 2), (self.ARROW_LENGTH, self.ARROW_WIDTH), (0, 0)],
                      **{"stroke": "#000", "stroke-width": 0.5}))
        markers.append(marker_end)
        return markers

    def _draw(self):
        res = []
        # Arc
        self.attribs.update({"marker-start": "url(#{})".format(self.get_marker_id('start')),
                             "marker-end": "url(#{})".format(self.get_marker_id('end'))})
        arc = path.Path(**self.attribs)
        arc.push("M")
        arc.push(self.start_point)
        arc_r = length = self._get_length(self.start_point, self.end_point)
        arc.push_arc(self.end_point, 0, arc_r, large_arc=False, absolute=True)
        res.append(arc)
        # Text
        chord = (length ** 2 - (length ** 2) / 4) ** 0.5
        middle_point = self._get_middle_point(self.start_point, self.end_point)
        directing_vector = (self.end_point[0] - self.start_point[0], self.end_point[1] - self.start_point[1])
        unit_vector = (directing_vector[0] / length, directing_vector[1] / length)
        ortogonal_vector = (chord * (-unit_vector[1]), chord * unit_vector[0])
        center = (middle_point[0] + ortogonal_vector[0], middle_point[1] + ortogonal_vector[1])

        radius_vector = ((middle_point[0] - center[0]) / chord, (middle_point[1] - center[1]) / chord)
        radius_ortogonal_vector = (-radius_vector[1], radius_vector[0])
        arc_center = (center[0] + radius_vector[0] * (length + self.ARROW_PADDING),
                      center[1] + radius_vector[1] * (length + self.ARROW_PADDING))
        text_line_start = (arc_center[0] - radius_ortogonal_vector[0] * 10,
                           arc_center[1] - radius_ortogonal_vector[1] * 10)
        text_line_end = (arc_center[0] + radius_ortogonal_vector[0] * 10,
                         arc_center[1] + radius_ortogonal_vector[1] * 10)
        res.append(self._render_text(text_line_start, text_line_end, padding=False))
        return res
