import unittest

from recipeformats import mxp


class TestIsMxpHeader(unittest.TestCase):

    def test_when_empty(self):
        actual = mxp._is_mxp_header('')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_typo(self):
        actual = mxp._is_mxp_header('* Exported frm MasterCook *')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_no_asterisks(self):
        actual = mxp._is_mxp_header('Exported from MasterCook')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_typical(self):
        actual = mxp._is_mxp_header('* Exported from MasterCook *')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_typical_2(self):
        actual = mxp._is_mxp_header('*  Exported from  MasterCook II  *')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_outer_whitespace(self):
        actual = mxp._is_mxp_header('                * Exported from MasterCook *                      ')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_inner_whitespace(self):
        actual = mxp._is_mxp_header('                *      Exported from MasterCook          *                      ')
        expected = True
        self.assertEqual(actual, expected)


class TestIsMxpFooter(unittest.TestCase):

    def test_when_empty(self):
        actual = mxp._is_mxp_footer('')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_text(self):
        actual = mxp._is_mxp_footer('Publisher: Golden West Publishers')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_not_enough_dashes(self):
        actual = mxp._is_mxp_footer('- - - - - - - - - - - - - - - - -')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_minimum_dashes(self):
        actual = mxp._is_mxp_footer('- - - - - - - - - - - - - - - - - -')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_outer_whitespace(self):
        actual = mxp._is_mxp_footer('                - - - - - - - - - - - - - - - - - - -                     ')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_more_dashes(self):
        actual = mxp._is_mxp_footer('           - - - - - - - - - - - - - - - - - - - - - -                   ')
        expected = True
        self.assertEqual(actual, expected)


class TestTestServingSizePreparationTime(unittest.TestCase):

    def test_when_empty(self):
        actual = mxp._test_serving_size_preparation_time('')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_1(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  : 2     Preparation Time :1:25')
        expected = True, '2', '1:25'
        self.assertEqual(actual, expected)

    def test_2(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  :       Preparation Time :1:25')
        expected = True, '', '1:25'
        self.assertEqual(actual, expected)

    def test_3(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  : 2     Preparation Time :')
        expected = True, '2', ''
        self.assertEqual(actual, expected)

    def test_4(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  : 2     Preparation Time :        ')
        expected = True, '2', ''
        self.assertEqual(actual, expected)

    def test_5(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  :123456 Preparation Time : 2:57')
        expected = True, '123456', '2:57'
        self.assertEqual(actual, expected)

    def test_6(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  : 2    Preparation Time :1:25')
        expected = True, '2', '1:25'
        self.assertEqual(actual, expected)

    def test_7(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  :      Preparation Time :1:25')
        expected = True, '', '1:25'
        self.assertEqual(actual, expected)

    def test_8(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  : 2    Preparation Time :')
        expected = True, '2', ''
        self.assertEqual(actual, expected)

    def test_9(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  : 2    Preparation Time :        ')
        expected = True, '2', ''
        self.assertEqual(actual, expected)

    def test_10(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  :12345 Preparation Time : 2:57')
        expected = True, '12345', '2:57'
        self.assertEqual(actual, expected)

    def test_11(self):
        actual = mxp._test_serving_size_preparation_time('Serving Size  :       Preparation Time :')
        expected = True, '', ''
        self.assertEqual(actual, expected)


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