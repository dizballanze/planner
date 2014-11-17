from tests import BaseTestCase
import unittest


class TestFrame(BaseTestCase):

    """ Functional test of drawing frames with coordinates """

    pass


class TestPolygon(BaseTestCase):

    """ Test base class for all frames """

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

    @unittest.skip("Not yet implemented")
    def test_hatching(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_hatching_id(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_filling(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_filling_hatching_replace(self):
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

    @unittest.skip("Not yet implemented")
    def test_hatching(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_filling(self):
        pass


@unittest.skip("Not yet implemented")
class TestRect(BaseTestCase):

    """ Test rectangle shape """
    pass
