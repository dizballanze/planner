from unittest import TestCase


class BaseTestCase(TestCase):

    """
    Abstract base Test Case with additional asserts and common useful methods.
    """

    def assertLength(self, seq, length):
        """ Assert that length of specified sequence is equal to specified number """
        if len(seq) != length:
            self.fail("Sequence length is {} but expected length is {}".format(len(seq), length))

    def assertAttrib(self, svg_obj, attrib, value):
        """
        Check that specified attribute of svg object is has specified value.
        """
        if svg_obj.attribs[attrib] != value:
            msg = "SVG object has attribute {attr_name}={attr_value}, but expected value is {expected_value}".format(
                attr_name=attrib,
                attr_value=svg_obj.attribs[attrib],
                expected_value=value)
            self.fail(msg)
