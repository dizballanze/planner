from tests import BaseTestCase


class TestFrame(BaseTestCase):

    """ Functional test of drawing frames with coordinates """

    pass


class TestRectFrame(BaseTestCase):

    """ Test of rectangle frame """

    CORNER = (10, 20)  # Corner coordinates
    SIZES = (350, 250)  # Sizes (WIDTH x HEIGHT)
    WALL_WIDTH = 25

    @classmethod
    def setUpClass(cls):
        from planner.frame import RectFrame
        cls.RectFrame = RectFrame

    def test_draw(self):
        """ Test frame drawing. Should create correct SVG objects. """
        rect_frame = self.RectFrame(self.CORNER[0], self.CORNER[1], self.SIZES[0], self.SIZES[1], self.WALL_WIDTH)
        svg_objects = rect_frame._draw()
        self.assertLength(svg_objects, 2)
        outer, inner = svg_objects
        from svgwrite import shapes, mm
        self.assertIsInstance(outer, shapes.Rect)
        self.assertIsInstance(inner, shapes.Rect)
        # Check sizes and coordinates
        self.assertAttrib(outer, 'x', self.CORNER[0] * mm)
        self.assertAttrib(outer, 'y', self.CORNER[1] * mm)
        self.assertAttrib(outer, 'width', self.SIZES[0] * mm)
        self.assertAttrib(outer, 'height', self.SIZES[1] * mm)
        self.assertAttrib(inner, 'x', (self.CORNER[0] + self.WALL_WIDTH) * mm)
        self.assertAttrib(inner, 'y', (self.CORNER[1] + self.WALL_WIDTH) * mm)
        self.assertAttrib(inner, 'width', (self.SIZES[0] - 2 * self.WALL_WIDTH) * mm)
        self.assertAttrib(inner, 'height', (self.SIZES[1] - 2 * self.WALL_WIDTH) * mm)
