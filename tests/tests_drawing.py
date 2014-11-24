from tests import BaseTestCase
import unittest


class TestDrawing(BaseTestCase):

    """
    Test container of plan
    """

    @classmethod
    def setUpClass(cls):
        from planner.drawing import Drawing
        cls.Drawing = Drawing

    def setUp(self):
        self.drawing = self.Drawing()

    def test_format_sizes(self):
        """
        Check that specified format sizes are confined
        """
        drawing = self.Drawing("A3")
        self.assertSequenceEqual(drawing.size, (420, 297))
        drawing = self.Drawing("A2")
        self.assertSequenceEqual(drawing.size, (594, 420))
        drawing = self.Drawing("A4")
        self.assertSequenceEqual(drawing.size, (297, 210))

    def test_add(self):
        """
        Test adding objects to drawing
        """
        from planner.frame import RectFrame
        frame = RectFrame()
        self.drawing.add(frame)
        self.assertIn(frame, self.drawing.objects)

    def test_render(self):
        """
        Check that rendered code contained code of every drawing element
        """
        from planner.frame import RectFrame, Rect
        rect = Rect()
        rect_frame = RectFrame()
        self.drawing.add(rect)
        self.drawing.add(rect_frame)
        rendered = str(self.drawing)
        for element in [rect, rect_frame]:
            for shape in element._draw():
                self.assertIn(shape.tostring(), rendered)
