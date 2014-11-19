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

    @unittest.skip("Not implemented")
    def test_add(self):
        pass

    @unittest.skip("Not implemented")
    def test_render(self):
        pass
