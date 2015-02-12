from tests import BaseTestCase


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
        self.assertLength(svg_objects, 6)
        top, left, right, bottom, outer, inner = svg_objects
        from svgwrite import shapes
        self.assertIsInstance(top, shapes.Rect)
        self.assertIsInstance(left, shapes.Rect)
        self.assertIsInstance(right, shapes.Rect)
        self.assertIsInstance(bottom, shapes.Rect)
        self.assertIsInstance(outer, shapes.Rect)
        self.assertIsInstance(inner, shapes.Rect)
        # Check sizes and coordinates
        self.assertAttrib(outer, 'x', self.CORNER[0])
        self.assertAttrib(outer, 'y', self.CORNER[1])
        self.assertAttrib(outer, 'width', self.SIZES[0])
        self.assertAttrib(outer, 'height', self.SIZES[1])
        self.assertAttrib(inner, 'x', (self.CORNER[0] + self.WALL_WIDTH))
        self.assertAttrib(inner, 'y', (self.CORNER[1] + self.WALL_WIDTH))
        self.assertAttrib(inner, 'width', (self.SIZES[0] - 2 * self.WALL_WIDTH))
        self.assertAttrib(inner, 'height', (self.SIZES[1] - 2 * self.WALL_WIDTH))
        # Check border background rect
        self.assertAttrib(top, 'x', self.CORNER[0])
        self.assertAttrib(top, 'y', self.CORNER[1])
        self.assertAttrib(top, 'width', self.SIZES[0])
        self.assertAttrib(top, 'height', self.WALL_WIDTH)
        self.assertAttrib(left, 'x', self.CORNER[0])
        self.assertAttrib(left, 'y', self.CORNER[1])
        self.assertAttrib(left, 'width', self.WALL_WIDTH)
        self.assertAttrib(left, 'height', self.SIZES[1])
        self.assertAttrib(right, 'x', self.CORNER[0] + self.SIZES[0] - self.WALL_WIDTH)
        self.assertAttrib(right, 'y', self.CORNER[1])
        self.assertAttrib(right, 'width', self.WALL_WIDTH)
        self.assertAttrib(right, 'height', self.SIZES[1])
        self.assertAttrib(bottom, 'x', self.CORNER[0])
        self.assertAttrib(bottom, 'y', self.CORNER[1] + self.SIZES[1] - self.WALL_WIDTH)
        self.assertAttrib(bottom, 'width', self.SIZES[0])
        self.assertAttrib(bottom, 'height', self.WALL_WIDTH)

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

    def test_add_aperture_coordinates_validation(self):
        """
        Test aperture coordinates validation
        """
        with self.assertRaisesRegex(ValueError, "not located on the wall border"):
            self.rect_frame.add_aperture(0, 0, 50)

    def test_add_aperture_with_correct_coordinates(self):
        """
        Test apperture with correct coordinates
        """
        try:
            self.rect_frame.add_aperture(10, 50, 50)  # left
            self.rect_frame.add_aperture(55, 20, 50)  # top
            self.rect_frame.add_aperture(335, 60, 50)  # right
            self.rect_frame.add_aperture(45, 245, 50)  # bottom
        except ValueError as err:
            self.fail(
                'Should not throw any exceptions on correct coordinates and width. Error message: {}'.format(str(err)))

    def test_wrong_width_validation(self):
        """
        Test validation of aperture with (should not exceed wall sizes)
        """
        # left
        with self.assertRaisesRegex(ValueError, "Aperture width exceed wall sizes"):
            self.rect_frame.add_aperture(10, 50, 250)
        # top
        with self.assertRaisesRegex(ValueError, "Aperture width exceed wall sizes"):
            self.rect_frame.add_aperture(55, 20, 350)
        # right
        with self.assertRaisesRegex(ValueError, "Aperture width exceed wall sizes"):
            self.rect_frame.add_aperture(335, 60, 250)
        # bottom
        with self.assertRaisesRegex(ValueError, "Aperture width exceed wall sizes"):
            self.rect_frame.add_aperture(45, 245, 350)

    def test_aperture_draw(self):
        """
        Test that added aperture correctly drawed
        """
        from svgwrite import shapes
        # left
        self.rect_frame.add_aperture(10, 50, 50)
        svg_objects = self.rect_frame._draw()
        self.assertLength(svg_objects, 7)
        aperture = svg_objects[6]
        self.assertIsInstance(aperture, shapes.Rect)
        self.assertAttrib(aperture, 'x', 10)
        self.assertAttrib(aperture, 'y', 50)
        self.assertAttrib(aperture, 'width', self.WALL_WIDTH)
        self.assertAttrib(aperture, 'height', 50)
        # top
        self.rect_frame.add_aperture(55, 20, 50)
        svg_objects = self.rect_frame._draw()
        self.assertLength(svg_objects, 8)
        aperture = svg_objects[7]
        self.assertIsInstance(aperture, shapes.Rect)
        self.assertAttrib(aperture, 'x', 55)
        self.assertAttrib(aperture, 'y', 20)
        self.assertAttrib(aperture, 'width', 50)
        self.assertAttrib(aperture, 'height', self.WALL_WIDTH)

    def test_add_horizontal_bulkhead(self):
        """
        Test adding horizontal bulkhead to the frame
        """
        from planner.frame.bulkhead import Bulkhead
        bulkhead = self.rect_frame.add_bulkhead(35, 70, 30)
        self.assertIsInstance(bulkhead, Bulkhead)
        self.assertLength(self.rect_frame.bulkheads, 1)
        self.assertEqual(bulkhead, self.rect_frame.bulkheads[0])
        self.assertEqual(bulkhead.x, 35)
        self.assertEqual(bulkhead.y, 70)
        self.assertEqual(bulkhead.width, self.SIZES[0] - 2 * self.WALL_WIDTH)
        self.assertEqual(bulkhead.height, 30)

    def test_add_vertical_bulkhead(self):
        """
        Test adding vertical bulkhead to frame
        """
        from planner.frame.bulkhead import Bulkhead
        bulkhead = self.rect_frame.add_bulkhead(70, 45, 30)
        self.assertIsInstance(bulkhead, Bulkhead)
        self.assertLength(self.rect_frame.bulkheads, 1)
        self.assertEqual(bulkhead, self.rect_frame.bulkheads[0])
        self.assertEqual(bulkhead.x, 70)
        self.assertEqual(bulkhead.y, 45)
        self.assertEqual(bulkhead.width, 30)
        self.assertEqual(bulkhead.height, self.SIZES[1] - 2 * self.WALL_WIDTH)

    def test_add_wrong_coordinates_bulkhead(self):
        """
        Should raise exception if top-left corner not lay on left or right top inner wall border
        """
        with self.assertRaisesRegex(ValueError, 'left-top corner should lay on left or top inner wall border'):
            self.rect_frame.add_bulkhead(10, 10, 30)

    def test_draw_bulkhead(self):
        """
        Should draw all added bulkheads
        """
        bulkhead1 = self.rect_frame.add_bulkhead(70, 45, 30)
        bulkhead2 = self.rect_frame.add_bulkhead(35, 70, 30)
        from planner.drawing import Drawing
        drawing = Drawing()
        drawing.add(self.rect_frame)
        drawed = str(drawing)
        self.assertIn(bulkhead1._draw()[0].tostring(), drawed)
        self.assertIn(bulkhead1._draw()[1].tostring(), drawed)
        self.assertIn(bulkhead2._draw()[0].tostring(), drawed)
        self.assertIn(bulkhead2._draw()[1].tostring(), drawed)
