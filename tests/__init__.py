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

    def assertStyle(self, svg_obj, style, value):
        """
        Check that specified style of svg object is has specified value.
        """
        styles = svg_obj.attribs["style"]
        styles = styles.split(";")
        styles_dict = {}
        for style_pair in styles:
            style_key, style_value = [val.strip() for val in style_pair.split(":")]
            styles_dict[style_key] = style_value
        if style not in styles_dict:
            self.fail("Style {style} not found".format(style=style))
        if styles_dict[style] != value:
            self.fail("Style {style} has value {value} but expected value is {expected_value}".format(
                style=style, value=styles_dict[style], expected_value=value))
