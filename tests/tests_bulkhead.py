from tests import BaseTestCase


class TestBulkhead(BaseTestCase):

    """
    Test bulkhead (inner wall) representation class
    """

    LEFT_TOP = (10, 20)
    RIGHT_BOTTOM = (110, 40)
    ATTRIBS = dict(fill="#6F6")

    @classmethod
    def setUpClass(cls):
        from planner.frame.bulkhead import Bulkhead
        cls.Bulkhead = Bulkhead

    def setUp(self):
        self.bulkhead = self.Bulkhead(self.LEFT_TOP, self.RIGHT_BOTTOM, **self.ATTRIBS)

    def test_init(self):
        """
        Test that object correctly initialized
        """
        self.assertEqual(self.bulkhead.x, self.LEFT_TOP[0])
        self.assertEqual(self.bulkhead.y, self.LEFT_TOP[1])
        self.assertEqual(self.bulkhead.width, 100)
        self.assertEqual(self.bulkhead.height, 20)

    def test_draw(self):
        """
        Test bulkhead drawing
        """
        from svgwrite import shapes
        rect_border, rect_bg = self.bulkhead._draw()
        # Test border rect
        self.assertIsInstance(rect_border, shapes.Rect)
        self.assertAttrib(rect_border, 'x', self.LEFT_TOP[0])
        self.assertAttrib(rect_border, 'y', self.LEFT_TOP[1])
        self.assertAttrib(rect_border, 'width', self.bulkhead.width)
        self.assertAttrib(rect_border, 'height', self.bulkhead.height)
        self.assertAttrib(rect_border, 'fill', '#fff')  # border rect should be white
        # Test background rect
        self.assertIsInstance(rect_bg, shapes.Rect)
        self.assertAttrib(rect_bg, 'x', float(self.LEFT_TOP[0] + 1))
        self.assertAttrib(rect_bg, 'y', float(self.LEFT_TOP[1] + 1))
        self.assertAttrib(rect_bg, 'width', (self.bulkhead.width - 2))
        self.assertAttrib(rect_bg, 'height', (self.bulkhead.height - 2))
        self.assertAttrib(rect_bg, 'fill', '#6F6')
