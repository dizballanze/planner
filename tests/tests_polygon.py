from tests import BaseTestCase


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

    def test_is_point_on_line_not(self):
        """
        Test "is point lay on the line" help function with point not on the line
        """
        lp1 = (0, 0)
        lp2 = (10, 10)
        point = (5, 6)
        self.assertFalse(self.polygon._is_point_on_line(lp1, lp2, point))
        lp1 = (0, 0)
        lp2 = (0, 10)
        point = (0, 11)
        self.assertFalse(self.polygon._is_point_on_line(lp1, lp2, point))
        lp1 = (0, 0)
        lp2 = (0, 10)
        point = (0, -1)
        self.assertFalse(self.polygon._is_point_on_line(lp1, lp2, point))

    def test_is_point_on_line(self):
        """
        Test "is point lay on the line" help function with point on the line
        """
        lp1 = (0, 0)
        lp2 = (10, 10)
        point = (5, 5)
        self.assertTrue(self.polygon._is_point_on_line(lp1, lp2, point))