from tests import BaseTestCase


class TestFigure(BaseTestCase):

    """ Test base class for all frames """

    ANGLE = 30
    DISTANCE = 5
    WIDTH = 2
    COLOR = "black"

    @classmethod
    def setUpClass(cls):
        from planner.frame import Figure
        cls.Figure = Figure

    def setUp(self):
        self.figure = self.Figure()

    def test_uuid_generation(self):
        """ Should return same uuid on each call of uuid property method """
        uuid = self.figure.uuid
        uuid2 = self.figure.uuid
        self.assertEqual(uuid, uuid2)

    def test_draw(self):
        """ Should raise exception cause _draw method is not implemented in abstract class """
        with self.assertRaises(NotImplementedError):
            self.figure._draw()

    def test_hatching(self):
        """
        Test hatching pattern svg elements
        """
        from svgwrite import pattern
        import math
        # Check pattern element
        self.figure.add_hatching(self.ANGLE, self.DISTANCE, self.WIDTH, self.COLOR)
        hatch = self.figure.hatch
        self.assertIsInstance(hatch, pattern.Pattern)
        self.assertAttrib(hatch, 'x', 0)
        self.assertAttrib(hatch, 'y', 0)
        width = (self.DISTANCE / math.sin(math.radians(self.ANGLE)))
        self.assertAttrib(hatch, 'width', width)
        height = width * math.tan(math.radians(self.ANGLE))
        self.assertAttrib(hatch, 'height', height)
        self.assertAttrib(hatch, 'id', self.figure._hatching_id)
        # Check inner elements
        self.assertLength(hatch.elements, 4)
        self.assertStyle(hatch.elements[1], 'stroke', self.COLOR)
        self.assertStyle(hatch.elements[1], 'stroke-width', str(self.WIDTH))

    def test_hatching_id(self):
        """
        Hatching id should contain figure uuid
        """
        self.figure.add_hatching(self.ANGLE, self.DISTANCE, self.WIDTH, self.COLOR)
        self.assertIn(self.figure.uuid, self.figure._hatching_id)

    def test_filling(self):
        """
        Test figure filling (with solid color)
        """
        self.figure.add_filling(self.COLOR)
        self.assertEqual(self.figure.filling, self.COLOR)

    def test_filling_hatching_replace(self):
        """
        Test that only latest setted filling/hatching is used.
        """
        self.assertFalse(hasattr(self.figure, 'hatch'))
        self.assertFalse(hasattr(self.figure, 'filling'))
        self.figure.add_hatching(self.ANGLE, self.DISTANCE, self.WIDTH, self.COLOR)
        self.assertTrue(hasattr(self.figure, 'hatch'))
        self.assertFalse(hasattr(self.figure, 'filling'))
        self.figure.add_filling(self.COLOR)
        self.assertFalse(hasattr(self.figure, 'hatch'))
        self.assertTrue(hasattr(self.figure, 'filling'))
        self.figure.add_hatching(self.ANGLE, self.DISTANCE, self.WIDTH, self.COLOR)
        self.assertTrue(hasattr(self.figure, 'hatch'))
        self.assertFalse(hasattr(self.figure, 'filling'))

    def test_is_point_on_line_not(self):
        """
        Test "is point lay on the line" help function with point not on the line
        """
        lp1 = (0, 0)
        lp2 = (10, 10)
        point = (5, 6)
        self.assertFalse(self.figure._is_point_on_line(lp1, lp2, point))
        lp1 = (0, 0)
        lp2 = (0, 10)
        point = (0, 11)
        self.assertFalse(self.figure._is_point_on_line(lp1, lp2, point))
        lp1 = (0, 0)
        lp2 = (0, 10)
        point = (0, -1)
        self.assertFalse(self.figure._is_point_on_line(lp1, lp2, point))

    def test_is_point_on_line(self):
        """
        Test "is point lay on the line" help function with point on the line
        """
        lp1 = (0, 0)
        lp2 = (10, 10)
        point = (5, 5)
        self.assertTrue(self.figure._is_point_on_line(lp1, lp2, point))
