from tests import BaseTestCase


class TestParseUnitsTools(BaseTestCase):

    """
    Test generic tools.
    """

    @classmethod
    def setUpClass(cls):
        from planner.tools import parse_measure_units
        cls.parse_measure_units = parse_measure_units

    def test_parsing_wrong_values(self):
        """
        Should raise Value Error on wrong values.
        """
        with self.assertRaises(ValueError):
            TestParseUnitsTools.parse_measure_units('mm20mm')
        with self.assertRaises(ValueError):
            TestParseUnitsTools.parse_measure_units('mm')
        with self.assertRaises(ValueError):
            TestParseUnitsTools.parse_measure_units('50.5.5')
        with self.assertRaises(ValueError):
            TestParseUnitsTools.parse_measure_units('.5')

    def test_parsing_ints(self):
        """
        Should correctly parsing ints.
        """
        val, unit = TestParseUnitsTools.parse_measure_units('50cm')
        self.assertEqual(val, 50)
        self.assertEqual(unit, 'cm')

    def test_default_units(self):
        """
        Should return default units if it not provided in values.
        """
        val, unit = TestParseUnitsTools.parse_measure_units('1005', default_unit='km')
        self.assertEqual(val, 1005)
        self.assertEqual(unit, 'km')

    def test_parsing_floats(self):
        """
        Should correctly parsing floats.
        """
        val, unit = TestParseUnitsTools.parse_measure_units('10.5')
        self.assertEqual(val, 10.5)
        self.assertEqual(unit, 'mm')
