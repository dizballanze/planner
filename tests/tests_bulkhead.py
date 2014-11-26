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
        from svgwrite import shapes, mm
        rect = self.bulkhead._draw()
        self.assertIsInstance(rect, shapes.Rect)
        self.assertAttrib(rect, 'x', self.LEFT_TOP[0] * mm)
        self.assertAttrib(rect, 'y', self.LEFT_TOP[1] * mm)
        self.assertAttrib(rect, 'width', self.bulkhead.width * mm)
        self.assertAttrib(rect, 'height', self.bulkhead.height * mm)
        self.assertAttrib(rect, 'fill', '#6F6')
