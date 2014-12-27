from tests import BaseTestCase


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
