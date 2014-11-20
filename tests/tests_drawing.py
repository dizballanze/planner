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
        from planner.frame import Frame
        frame = Frame()
        self.drawing.add(frame)
        self.assertIn(frame, self.drawing.objects)

    def test_render(self):
        """
        Check that rendered code contained code of every drawing element
        """
        from planner.frame import Frame
        frame = Frame()
        rect = frame.add_rect()
        rect_frame = frame.add_rect_frame()
        self.drawing.add(frame)
        frame2 = Frame()
        rect2 = frame2.add_rect(x=10, y=10)
        self.drawing.add(frame2)
        rendered = str(self.drawing)
        for element in [rect, rect_frame, rect2]:
            for shape in element._draw():
                self.assertIn(shape.tostring(), rendered)
