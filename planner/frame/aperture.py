from planner.frame.polygon import Polygon
from svgwrite import shapes


class Aperture(Polygon):

    """
    Aperture (door, window, etc) in a wall (only horizontal and vertical walls supported for now)
    """

    def __init__(self, start_point, width, wall_start_point, wall_end_point, wall_width, **attribs):
        """
        Create aperture. Parameters:
        start_point - coordinates of top-left aperture corner (tuple x, y)
        width - aperture width
        wall_start_point, wall_end_point - coordinates of wall border
        """
        if not self._is_point_on_line(wall_start_point, wall_end_point, start_point):
            raise ValueError(
                "Coordinates {}, {} of aperture left corner not located on the wall border".format(*start_point))
        if not self._is_point_on_line(wall_start_point, wall_end_point, (start_point[0] + width, start_point[1])) \
           and not self._is_point_on_line(wall_start_point, wall_end_point, (start_point[0], start_point[1] + width)):
            raise ValueError("Aperture width exceed wall sizes")
        self.start_point = start_point
        self.width = width
        self.wall_start_point = wall_start_point
        self.wall_end_point = wall_end_point
        self.wall_width = wall_width
        self.attribs = attribs

    def _draw(self):
        attribs = {"stroke": "#000", "stroke-width": "2", "fill": "#fff"}
        attribs.update(self.attribs)
        # vertical (x coordinates equal)
        if self.wall_start_point[0] == self.wall_end_point[0]:
            width = self.wall_width
            height = self.width
        # horizontal
        else:
            width = self.width
            height = self.wall_width
        return shapes.Rect((self.start_point[0], self.start_point[1]), (width, height), **attribs)

    @classmethod
    def match_wall_and_create(cls, start_point, width, walls, wall_width, **attribs):
        """
        Aperture factory. Creates aperture in a wall from list if start point located on wall border.
        walls - list of sequences with coordinates of border in form ((x1, y1), (x2, y2))
        """
        for wall in walls:
            if cls._is_point_on_line(wall[0], wall[1], start_point):
                return Aperture(start_point, width, wall[0], wall[1], wall_width, **attribs)
        return False
