import unittest

from recipeformats import mxp


class TestTestMetadata(unittest.TestCase):

    def test_when_empty(self):
        actual = mxp._test_metadata('')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_colon(self):
        actual = mxp._test_metadata(':')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_no_attribute_name(self):
        actual = mxp._test_metadata('    : value')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_text_without_colon(self):
        actual = mxp._test_metadata('   Chill before serving.   ')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_no_value(self):
        actual = mxp._test_metadata(' Recipe By: ')
        expected = True, 'Recipe By', ''
        self.assertEqual(actual, expected)

    def test_when_normal(self):
        actual = mxp._test_metadata('Recipe By     : Sam')
        expected = True, 'Recipe By', 'Sam'
        self.assertEqual(actual, expected)

    def test_when_extra_spaces(self):
        actual = mxp._test_metadata('    Recipe   By     :     Aunt   Salli   ')
        expected = True, 'Recipe   By', 'Aunt   Salli'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()