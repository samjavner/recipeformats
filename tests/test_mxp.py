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


class TestTestCategories(unittest.TestCase):

    def test_when_empty(self):
        actual = mxp._test_categories('')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_15_spaces(self):
        actual = mxp._test_categories('               ')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_16_spaces(self):
        actual = mxp._test_categories('                ')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_17_spaces(self):
        actual = mxp._test_categories('                 ')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_48_spaces(self):
        actual = mxp._test_categories('                                                ')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_no_categories(self):
        actual = mxp._test_categories('Categories    : ')
        expected = True, '', ''
        self.assertEqual(actual, expected)

    def test_when_one_category_1(self):
        actual = mxp._test_categories('Categories    : Bread Machine')
        expected = True, 'Bread Machine', ''
        self.assertEqual(actual, expected)

    def test_when_one_category_2(self):
        actual = mxp._test_categories('Categories    : Bread Machine                   Nuts')
        expected = True, 'Bread Machine', 'Nuts'
        self.assertEqual(actual, expected)

    def test_when_two_categories_2(self):
        actual = mxp._test_categories('                Bread Machine                   Nuts')
        expected = True, 'Bread Machine', 'Nuts'
        self.assertEqual(actual, expected)


class TestTestIngredient(unittest.TestCase):
    
    def test_when_empty(self):
        actual = mxp._test_ingredient('')
        expected = None
        self.assertEqual(actual, expected)

    def test_when_whitespace(self):
        actual = mxp._test_ingredient('                                                ')
        expected = None
        self.assertEqual(actual, expected)

    def test_when_amount_misaligned_1(self):
        actual = mxp._test_ingredient('2/3                Cup  Apples')
        expected = None
        self.assertEqual(actual, expected)

    def test_when_amount_misaligned_2(self):
        actual = mxp._test_ingredient('      2/3          Cup  Apples')
        expected = None
        self.assertEqual(actual, expected)

    def test_when_measure_misaligned_1(self):
        actual = mxp._test_ingredient('     2/3 Cup            Apples')
        expected = None
        self.assertEqual(actual, expected)

    def test_when_measure_misaligned_2(self):
        actual = mxp._test_ingredient('     2/3            Cup Apples')
        expected = None
        self.assertEqual(actual, expected)

    def test_when_ingredient_misaligned(self):
        actual = mxp._test_ingredient('     2/3           Cup Apples')
        expected = None
        self.assertEqual(actual, expected)
    
    def test_test_1(self):
        actual = mxp._test_ingredient('     2/3           Cup  Apples')
        expected = '{2/3} {Cup} {Apples} {}'
        self.assertEqual(repr(actual), expected)
    
    def test_test_2(self):
        actual = mxp._test_ingredient('       3                Apples')
        expected = '{3} {} {Apples} {}'
        self.assertEqual(repr(actual), expected)
    
    def test_test_3(self):
        actual = mxp._test_ingredient('                  Some  Apples')
        expected = '{} {Some} {Apples} {}'
        self.assertEqual(repr(actual), expected)
    
    def test_test_4(self):
        actual = mxp._test_ingredient('                        Apples')
        expected = '{} {} {Apples} {}'
        self.assertEqual(repr(actual), expected)
    
    def test_test_5(self):
        actual = mxp._test_ingredient('  11 3/4  tablespoons+  Apple pie spice')
        expected = '{11 3/4} {tablespoons+} {Apple pie spice} {}'
        self.assertEqual(repr(actual), expected)
    
    def test_test_6(self):
        actual = mxp._test_ingredient('     2/3           Cup      Apples    ')
        expected = '{2/3} {Cup} {Apples} {}'
        self.assertEqual(repr(actual), expected)
    
    def test_test_7(self):
        actual = mxp._test_ingredient('     1/4           Cup  Margarine Or Butter -- softened')
        expected = '{1/4} {Cup} {Margarine Or Butter} {softened}'
        self.assertEqual(repr(actual), expected)
    
    def test_test_8(self):
        actual = mxp._test_ingredient('                        -- softened')
        expected = '{} {} {-- softened} {}'
        self.assertEqual(repr(actual), expected)
    
    def test_test_9(self):
        actual = mxp._test_ingredient('                            -- softened')
        expected = '{} {} {-- softened} {}'
        self.assertEqual(repr(actual), expected)
    
    def test_test_10(self):
        actual = mxp._test_ingredient('     1/4           Cup  Margarine Or Butter--softened')
        expected = '{1/4} {Cup} {Margarine Or Butter--softened} {}'
        self.assertEqual(repr(actual), expected)


if __name__ == '__main__':
    unittest.main()