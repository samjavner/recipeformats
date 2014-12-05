import unittest

from recipeformats import mxp


class TestParseRecipe(unittest.TestCase):

    def assert_equal(self, actual, expected_title, expected_recipe_by,
                     expected_serving_size, expected_preparation_time,
                     expected_categories, expected_ingredients,
                     expected_directions, expected_notes):
        actual_ingredients = [repr(i) for i in actual.ingredients]
        self.assertEqual(actual.title, expected_title)
        self.assertEqual(actual.recipe_by, expected_recipe_by)
        self.assertEqual(actual.serving_size, expected_serving_size)
        self.assertEqual(actual.preparation_time, expected_preparation_time)
        self.assertEqual(actual.categories, expected_categories)
        self.assertEqual(actual_ingredients, expected_ingredients)
        self.assertEqual(actual.directions, expected_directions)
        self.assertEqual(actual.notes, expected_notes)

    # Variations on this recipe follow it.
    def test_1(self):
        lines = [
            '* Exported from MasterCook *',
            '',
            '                               Test Recipe',
            '',
            'Recipe By     :Sam',
            'Serving Size  : 2     Preparation Time :1:25',
            'Categories    : Burgers                         Fish',
            '                Meat',
            '',
            '  Amount  Measure       Ingredient -- Preparation Method',
            '--------  ------------  --------------------------------',
            '                        Heading:',
            '  1                cup  milk -- please',
            '                            -- Heading:',
            '     1/2           cup     ',
            '  2                     eggs',
            '                 pound     ',
            '',
            'Direction 1.',
            '',
            'Direction 2.',
            '',
            'Description:',
            '  "Description!"',
            'Source:',
            '  "Internet"',
            'Copyright:',
            '  "2014"',
            'Yield:',
            '  "1 cake"',
            'Start to Finish Time:',
            '  "2:22"',
            '                                    - - - - - - - - - - - - - - - - - - - ',
            '',
            'Per Serving (excluding unknown items): 149 Calories; 9g Fat (55.4% calories from fat); 10g Protein; 6g Carbohydrate; 0g Dietary Fiber; 229mg Cholesterol; 130mg Sodium.  Exchanges: 1 Lean Meat; 1/2 Non-Fat Milk; 1 Fat.',
            '',
            'Suggested Wine: Cabernet',
            '',
            'Serving Ideas : Serve me this way!',
            '',
            'NOTES : Notely notes notes.',
            '',
            'Nutr. Assoc. : 0 0 0 0 0 0 0',
            ]
        expected_title = 'Test Recipe'
        expected_recipe_by = 'Sam'
        expected_serving_size = '2'
        expected_preparation_time = '1:25'
        expected_categories = ['Burgers', 'Fish', 'Meat']
        expected_ingredients = [
            '{} {} {Heading:} {}',
            '{1} {cup} {milk} {please}',
            '{} {} {-- Heading:} {}',
            '{1/2} {cup} {} {}',
            '{2} {} {eggs} {}',
            '{} {pound} {} {}',
            ]
        expected_directions = [
            'Direction 1.',
            'Direction 2.',
            'Description:',
            '"Description!"',
            'Source:',
            '"Internet"',
            'Copyright:',
            '"2014"',
            'Yield:',
            '"1 cake"',
            'Start to Finish Time:',
            '"2:22"',
            ]
        expected_notes = [
            'Per Serving (excluding unknown items): 149 Calories; 9g Fat (55.4% calories from fat); 10g Protein; 6g Carbohydrate; 0g Dietary Fiber; 229mg Cholesterol; 130mg Sodium.  Exchanges: 1 Lean Meat; 1/2 Non-Fat Milk; 1 Fat.', 
            'Suggested Wine: Cabernet',
            'Serving Ideas : Serve me this way!',
            'NOTES : Notely notes notes.',
            'Nutr. Assoc. : 0 0 0 0 0 0 0',
            ]
        actual = mxp.parse_recipe(lines)
        self.assert_equal(actual, expected_title, expected_recipe_by,
                          expected_serving_size, expected_preparation_time,
                          expected_categories, expected_ingredients,
                          expected_directions, expected_notes)
    
    def test_1_no_directions(self):
        lines = [
            '* Exported from MasterCook *',
            '',
            '                               Test Recipe',
            '',
            'Recipe By     :Sam',
            'Serving Size  : 2     Preparation Time :1:25',
            'Categories    : Burgers                         Fish',
            '                Meat',
            '',
            '  Amount  Measure       Ingredient -- Preparation Method',
            '--------  ------------  --------------------------------',
            '                        Heading:',
            '  1                cup  milk -- please',
            '                            -- Heading:',
            '     1/2           cup     ',
            '  2                     eggs',
            '                 pound     ',
            '',
            '                                    - - - - - - - - - - - - - - - - - - - ',
            '',
            'Suggested Wine: Cabernet',
            ]
        expected_title = 'Test Recipe'
        expected_recipe_by = 'Sam'
        expected_serving_size = '2'
        expected_preparation_time = '1:25'
        expected_categories = ['Burgers', 'Fish', 'Meat']
        expected_ingredients = [
            '{} {} {Heading:} {}',
            '{1} {cup} {milk} {please}',
            '{} {} {-- Heading:} {}',
            '{1/2} {cup} {} {}',
            '{2} {} {eggs} {}',
            '{} {pound} {} {}',
            ]
        expected_directions = []
        expected_notes = [
            'Suggested Wine: Cabernet'
            ]
        actual = mxp.parse_recipe(lines)
        self.assert_equal(actual, expected_title, expected_recipe_by,
                          expected_serving_size, expected_preparation_time,
                          expected_categories, expected_ingredients,
                          expected_directions, expected_notes)

    def test_1_no_ingredients(self):
        lines = [
            '* Exported from MasterCook *',
            '',
            '                               Test Recipe',
            '',
            'Recipe By     :Sam',
            'Serving Size  : 2     Preparation Time :1:25',
            'Categories    : Burgers                         Fish',
            '                Meat',
            '',
            '  Amount  Measure       Ingredient -- Preparation Method',
            '--------  ------------  --------------------------------',
            '',
            'Direction 1.',
            '',
            'Direction 2.',
            '                                    - - - - - - - - - - - - - - - - - - - ',
            '',
            'Suggested Wine: Cabernet',
            ]
        expected_title = 'Test Recipe'
        expected_recipe_by = 'Sam'
        expected_serving_size = '2'
        expected_preparation_time = '1:25'
        expected_categories = ['Burgers', 'Fish', 'Meat']
        expected_ingredients = []
        expected_directions = [
            'Direction 1.',
            'Direction 2.',
            ]
        expected_notes = [
            'Suggested Wine: Cabernet'
            ]
        actual = mxp.parse_recipe(lines)
        self.assert_equal(actual, expected_title, expected_recipe_by,
                          expected_serving_size, expected_preparation_time,
                          expected_categories, expected_ingredients,
                          expected_directions, expected_notes)
    
    def test_1_no_notes(self):
        lines = [
            '* Exported from MasterCook *',
            '',
            '                               Test Recipe',
            '',
            'Recipe By     :Sam',
            'Serving Size  : 2     Preparation Time :1:25',
            'Categories    : Burgers                         Fish',
            '                Meat',
            '',
            '  Amount  Measure       Ingredient -- Preparation Method',
            '--------  ------------  --------------------------------',
            '                        Heading:',
            '  1                cup  milk -- please',
            '                            -- Heading:',
            '     1/2           cup     ',
            '  2                     eggs',
            '                 pound     ',
            '',
            'Direction 1.',
            '',
            'Direction 2.',
            '                                    - - - - - - - - - - - - - - - - - - - ',
            ]
        expected_title = 'Test Recipe'
        expected_recipe_by = 'Sam'
        expected_serving_size = '2'
        expected_preparation_time = '1:25'
        expected_categories = ['Burgers', 'Fish', 'Meat']
        expected_ingredients = [
            '{} {} {Heading:} {}',
            '{1} {cup} {milk} {please}',
            '{} {} {-- Heading:} {}',
            '{1/2} {cup} {} {}',
            '{2} {} {eggs} {}',
            '{} {pound} {} {}',
            ]
        expected_directions = [
            'Direction 1.',
            'Direction 2.',
            ]
        expected_notes = []
        actual = mxp.parse_recipe(lines)
        self.assert_equal(actual, expected_title, expected_recipe_by,
                          expected_serving_size, expected_preparation_time,
                          expected_categories, expected_ingredients,
                          expected_directions, expected_notes)
    
    def test_1_extra_lines(self):
        lines = [
            '',
            '',
            '',
            '* Exported from MasterCook *',
            '',
            '                               Test Recipe',
            '',
            'Recipe By     :Sam',
            '',
            'Serving Size  : 2     Preparation Time :1:25',
            '',
            'Categories    : Burgers                         Fish',
            '                Meat',
            '',
            '  Amount  Measure       Ingredient -- Preparation Method',
            '--------  ------------  --------------------------------',
            '                        Heading:',
            '  1                cup  milk -- please',
            '                            -- Heading:',
            '     1/2           cup     ',
            '  2                     eggs',
            '                 pound     ',
            '',
            '',
            '',
            'Direction 1.',
            '',
            'Direction 2.',
            '',
            '',
            '                                    - - - - - - - - - - - - - - - - - - - ',
            '',
            'Suggested Wine: Cabernet',
            ]
        expected_title = 'Test Recipe'
        expected_recipe_by = 'Sam'
        expected_serving_size = '2'
        expected_preparation_time = '1:25'
        expected_categories = ['Burgers', 'Fish', 'Meat']
        expected_ingredients = [
            '{} {} {Heading:} {}',
            '{1} {cup} {milk} {please}',
            '{} {} {-- Heading:} {}',
            '{1/2} {cup} {} {}',
            '{2} {} {eggs} {}',
            '{} {pound} {} {}',
            ]
        expected_directions = [
            'Direction 1.',
            'Direction 2.',
            ]
        expected_notes = [
            'Suggested Wine: Cabernet',
            ]
        actual = mxp.parse_recipe(lines)
        self.assert_equal(actual, expected_title, expected_recipe_by,
                          expected_serving_size, expected_preparation_time,
                          expected_categories, expected_ingredients,
                          expected_directions, expected_notes)

    def test_1_no_metadata(self):
        lines = [
            '* Exported from MasterCook *',
            '',
            '                               Test Recipe',
            '',
            '  Amount  Measure       Ingredient -- Preparation Method',
            '--------  ------------  --------------------------------',
            '                        Heading:',
            '  1                cup  milk -- please',
            '                            -- Heading:',
            '     1/2           cup     ',
            '  2                     eggs',
            '                 pound     ',
            '',
            'Direction 1.',
            '',
            'Direction 2.',
            '                                    - - - - - - - - - - - - - - - - - - - ',
            '',
            'Suggested Wine: Cabernet',
            ]
        expected_title = 'Test Recipe'
        expected_recipe_by = ''
        expected_serving_size = ''
        expected_preparation_time = ''
        expected_categories = []
        expected_ingredients = [
            '{} {} {Heading:} {}',
            '{1} {cup} {milk} {please}',
            '{} {} {-- Heading:} {}',
            '{1/2} {cup} {} {}',
            '{2} {} {eggs} {}',
            '{} {pound} {} {}',
            ]
        expected_directions = [
            'Direction 1.',
            'Direction 2.',
            ]
        expected_notes = [
            'Suggested Wine: Cabernet',
            ]
        actual = mxp.parse_recipe(lines)
        self.assert_equal(actual, expected_title, expected_recipe_by,
                          expected_serving_size, expected_preparation_time,
                          expected_categories, expected_ingredients,
                          expected_directions, expected_notes)
    
    def test_1_no_header_and_footer(self):
        lines = [
            '',
            '                               Test Recipe',
            '',
            'Recipe By     :Sam',
            'Serving Size  : 2     Preparation Time :1:25',
            'Categories    : Burgers                         Fish',
            '                Meat',
            '',
            '  Amount  Measure       Ingredient -- Preparation Method',
            '--------  ------------  --------------------------------',
            '                        Heading:',
            '  1                cup  milk -- please',
            '                            -- Heading:',
            '     1/2           cup     ',
            '  2                     eggs',
            '                 pound     ',
            '',
            'Direction 1.',
            '',
            'Direction 2.',
            ]
        expected_title = 'Test Recipe'
        expected_recipe_by = 'Sam'
        expected_serving_size = '2'
        expected_preparation_time = '1:25'
        expected_categories = ['Burgers', 'Fish', 'Meat']
        expected_ingredients = [
            '{} {} {Heading:} {}',
            '{1} {cup} {milk} {please}',
            '{} {} {-- Heading:} {}',
            '{1/2} {cup} {} {}',
            '{2} {} {eggs} {}',
            '{} {pound} {} {}',
            ]
        expected_directions = [
            'Direction 1.',
            'Direction 2.',
            ]
        expected_notes = []
        actual = mxp.parse_recipe(lines)
        self.assert_equal(actual, expected_title, expected_recipe_by,
                          expected_serving_size, expected_preparation_time,
                          expected_categories, expected_ingredients,
                          expected_directions, expected_notes)
    
    def test_1_only_header_footer_and_metadata(self):
        lines = [
            '* Exported from MasterCook *',
            '',
            '                               Test Recipe',
            '',
            'Recipe By     :Sam',
            'Serving Size  : 2     Preparation Time :1:25',
            'Categories    : Burgers                         Fish',
            '                Meat',
            '',
            '                                    - - - - - - - - - - - - - - - - - - - ',
            ]
        expected_title = 'Test Recipe'
        expected_recipe_by = 'Sam'
        expected_serving_size = '2'
        expected_preparation_time = '1:25'
        expected_categories = ['Burgers', 'Fish', 'Meat']
        expected_ingredients = []
        expected_directions = []
        expected_notes = []
        actual = mxp.parse_recipe(lines)
        self.assert_equal(actual, expected_title, expected_recipe_by,
                          expected_serving_size, expected_preparation_time,
                          expected_categories, expected_ingredients,
                          expected_directions, expected_notes)
    
    def test_when_empty(self):
        lines = []
        expected_title = ''
        expected_recipe_by = ''
        expected_serving_size = ''
        expected_preparation_time = ''
        expected_categories = []
        expected_ingredients = []
        expected_directions = []
        expected_notes = []
        actual = mxp.parse_recipe(lines)
        self.assert_equal(actual, expected_title, expected_recipe_by,
                          expected_serving_size, expected_preparation_time,
                          expected_categories, expected_ingredients,
                          expected_directions, expected_notes)

    def test_when_just_some_text(self):
        lines = [
            '                               Test Recipe',
            'Direction 1.',
            '',
            'Direction 2.',
            ]
        expected_title = 'Test Recipe'
        expected_recipe_by = ''
        expected_serving_size = ''
        expected_preparation_time = ''
        expected_categories = []
        expected_ingredients = []
        expected_directions = [
            'Direction 1.',
            'Direction 2.',
            ]
        expected_notes = []
        actual = mxp.parse_recipe(lines)
        self.assert_equal(actual, expected_title, expected_recipe_by,
                          expected_serving_size, expected_preparation_time,
                          expected_categories, expected_ingredients,
                          expected_directions, expected_notes)


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
    
    def test_when_footer(self):
        actual = mxp._test_ingredient('                                    - - - - - - - - - - - - - - - - - - - ')
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