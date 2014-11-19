from tests import BaseTestCase
import unittest


class TestFrame(BaseTestCase):

    """ Functional test of drawing frames with coordinates """

    pass


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


@unittest.skip("Not yet implemented")
class TestRect(BaseTestCase):

    """ Test rectangle shape """
    pass
