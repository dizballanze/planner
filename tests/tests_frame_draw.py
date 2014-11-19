from tests import BaseTestCase
import unittest


class TestFrame(BaseTestCase):

    """ Functional test of drawing frames with coordinates """

    @classmethod
    def setUpClass(cls):
        from planner.frame import Frame
        cls.Frame = Frame

    def setUp(self):
        self.frame = self.Frame()

    def test_add_rect(self):
        """
        Should correctly add rectangle
        """
        self.frame.add_rect()
        self.assertLength(self.frame._plines, 1)
        from planner.frame import Rect
        self.assertIsInstance(self.frame._plines[0], Rect)

    def test_add_rect_frame(self):
        """
        Should correctly add rectangle frame
        """
        self.frame.add_rect_frame()
        self.assertLength(self.frame._plines, 1)
        from planner.frame import RectFrame
        self.assertIsInstance(self.frame._plines[0], RectFrame)


class TestPolygon(BaseTestCase):

    """ Test base class for all frames """

    ANGLE = 30
    DISTANCE = 5
    WIDTH = 2
    COLOR = "black"

    @classmethod
    def setUpClass(cls):
        from planner.frame import Polygon
        cls.Polygon = Polygon

    def setUp(self):
        self.polygon = self.Polygon()

    def test_uuid_generation(self):
        """ Should return same uuid on each call of uuid property method """
        uuid = self.polygon.uuid
        uuid2 = self.polygon.uuid
        self.assertEqual(uuid, uuid2)

    def test_draw(self):
        """ Should raise exception cause _draw method is not implemented in abstract class """
        with self.assertRaises(NotImplementedError):
            self.polygon._draw()

    def test_hatching(self):
        """
        Test hatching pattern svg elements
        """
        from svgwrite import pattern, mm
        import math
        # Check pattern element
        self.polygon.add_hatching(self.ANGLE, self.DISTANCE, self.WIDTH, self.COLOR)
        hatch = self.polygon.hatch
        self.assertIsInstance(hatch, pattern.Pattern)
        self.assertAttrib(hatch, 'x', 0 * mm)
        self.assertAttrib(hatch, 'y', 0 * mm)
        width = (self.DISTANCE / math.sin(math.radians(self.ANGLE)))
        self.assertAttrib(hatch, 'width', width * mm)
        height = width * math.tan(math.radians(self.ANGLE))
        self.assertAttrib(hatch, 'height', height * mm)
        self.assertAttrib(hatch, 'id', self.polygon._hatching_id)
        # Check inner elements
        self.assertLength(hatch.elements, 4)
        self.assertStyle(hatch.elements[1], 'stroke', self.COLOR)
        self.assertStyle(hatch.elements[1], 'width', self.WIDTH * mm)

    def test_hatching_id(self):
        """
        Hatching id should contain polygon uuid
        """
        self.polygon.add_hatching(self.ANGLE, self.DISTANCE, self.WIDTH, self.COLOR)
        self.assertIn(self.polygon.uuid, self.polygon._hatching_id)

    def test_filling(self):
        """
        Test polygon filling (with solid color)
        """
        self.polygon.add_filling(self.COLOR)
        self.assertEqual(self.polygon.filling, self.COLOR)

    def test_filling_hatching_replace(self):
        """
        Test that only latest setted filling/hatching is used.
        """
        self.assertFalse(hasattr(self.polygon, 'hatch'))
        self.assertFalse(hasattr(self.polygon, 'filling'))
        self.polygon.add_hatching(self.ANGLE, self.DISTANCE, self.WIDTH, self.COLOR)
        self.assertTrue(hasattr(self.polygon, 'hatch'))
        self.assertFalse(hasattr(self.polygon, 'filling'))
        self.polygon.add_filling(self.COLOR)
        self.assertFalse(hasattr(self.polygon, 'hatch'))
        self.assertTrue(hasattr(self.polygon, 'filling'))
        self.polygon.add_hatching(self.ANGLE, self.DISTANCE, self.WIDTH, self.COLOR)
        self.assertTrue(hasattr(self.polygon, 'hatch'))
        self.assertFalse(hasattr(self.polygon, 'filling'))


class TestRectFrame(BaseTestCase):

    """ Test of rectangle frame """

    # Constructor params
    CORNER = (10, 20)  # Corner coordinates
    SIZES = (350, 250)  # Sizes (WIDTH x HEIGHT)
    WALL_WIDTH = 25
    # Hatching / filling params
    ANGLE = 30
    DISTANCE = 5
    WIDTH = 2
    COLOR = "black"

    @classmethod
    def setUpClass(cls):
        from planner.frame import RectFrame
        cls.RectFrame = RectFrame

    def setUp(self):
        self.rect_frame = self.RectFrame(self.CORNER[0], self.CORNER[1], self.SIZES[0], self.SIZES[1], self.WALL_WIDTH)

    def test_draw(self):
        """ Test frame drawing. Should create correct SVG objects. """
        svg_objects = self.rect_frame._draw()
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

    def test_additional_attribs(self):
        """
        Should accept additional attributes for outer rectangle
        """
        attribs = {'opacity': 0.5, 'fill': "#55FF66"}
        rect_frame = self.RectFrame(
            self.CORNER[0], self.CORNER[1], self.SIZES[0], self.SIZES[1], self.WALL_WIDTH, **attribs)
        svg_objects = rect_frame._draw()
        outer_rect = svg_objects[0]
        for attr, value in attribs.items():
            self.assertAttrib(outer_rect, attr, value)

    def test_hatching(self):
        """
        Test that hatching appends to frame
        """
        self.rect_frame.add_hatching(self.ANGLE, self.DISTANCE, self.WIDTH, self.COLOR)
        svg_objects = self.rect_frame._draw()
        self.assertEqual(self.rect_frame.hatch, svg_objects[0])
        self.assertStyle(svg_objects[1], 'fill', 'url(#{})'.format(self.rect_frame._hatching_id))

    def test_filling(self):
        """
        Test that filling appends to frame
        """
        self.rect_frame.add_filling(self.COLOR)
        svg_objects = self.rect_frame._draw()
        self.assertAttrib(svg_objects[0], 'fill', self.COLOR)


class TestRect(BaseTestCase):

    """ Test rectangle shape """
    
    # Constructor params
    CORNER = (10, 20)  # Corner coordinates
    SIZES = (350, 250)  # Sizes (WIDTH x HEIGHT)
    # Hatching / filling params
    ANGLE = 30
    DISTANCE = 5
    WIDTH = 2
    COLOR = "black"

    @classmethod
    def setUpClass(cls):
        from planner.frame import Rect
        cls.Rect = Rect

    def setUp(self):
        self.rect = self.Rect(self.CORNER[0], self.CORNER[1], self.SIZES[0], self.SIZES[1])

    def test_draw(self):
        """ Test rect drawing """
        svg_objects = self.rect._draw()
        svg_object = svg_objects[0]
        # Check instance
        from svgwrite import shapes, mm
        self.assertIsInstance(svg_object, shapes.Rect)
        # Check coordinates and sizes
        self.assertAttrib(svg_object, 'x', self.CORNER[0] * mm)
        self.assertAttrib(svg_object, 'y', self.CORNER[1] * mm)
        self.assertAttrib(svg_object, 'width', self.SIZES[0] * mm)
        self.assertAttrib(svg_object, 'height', self.SIZES[1] * mm)

    def test_additional_attribs(self):
        """
        Should accept additional attributes for rectangle
        """
        attribs = {'opacity': 0.5, 'fill': "#55FF66"}
        rect = self.Rect(self.CORNER[0], self.CORNER[1], self.SIZES[0], self.SIZES[1], **attribs)
        svg_objects = rect._draw()
        for attr, value in attribs.items():
            self.assertAttrib(svg_objects[0], attr, value)

    def test_hatching(self):
        """
        Test that hatching appends to polygon
        """
        self.rect.add_hatching(self.ANGLE, self.DISTANCE, self.WIDTH, self.COLOR)
        svg_objects = self.rect._draw()
        self.assertEqual(self.rect.hatch, svg_objects[0])
        self.assertStyle(svg_objects[1], 'fill', 'url(#{})'.format(self.rect._hatching_id))

    def test_filling(self):
        """
        Test that filling appends to polygon
        """
        self.rect.add_filling(self.COLOR)
        svg_objects = self.rect._draw()
        self.assertAttrib(svg_objects[0], 'fill', self.COLOR)
