import unittest

import mmf


class TestIsMmfHeader(unittest.TestCase):

    def test_when_empty(self):
        actual = mmf._is_mmf_header('')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_normal(self):
        actual = mmf._is_mmf_header('---------- Recipe via Meal-Master (tm) v8.05')
        expected = True
        self.assertEqual(actual, expected)
    
    def test_when_MMMMM(self):
        actual = mmf._is_mmf_header('MMMMM----- Recipe via Meal-Master (tm) v8.05')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_mmmmm(self):
        actual = mmf._is_mmf_header('mmmmm----- Recipe via Meal-Master (tm) v8.05')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_extra_dash(self):
        actual = mmf._is_mmf_header('----------- Recipe via Meal-Master (tm) v8.05')
        expected = False
        self.assertEqual(actual, expected)
    
    def test_when_extra_M(self):
        actual = mmf._is_mmf_header('MMMMMM----- Recipe via Meal-Master (tm) v8.05')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_missing_dash(self):
        actual = mmf._is_mmf_header('--------- Recipe via Meal-Master (tm) v8.05')
        expected = False
        self.assertEqual(actual, expected)
    
    def test_when_missing_M(self):
        actual = mmf._is_mmf_header('MMMM----- Recipe via Meal-Master (tm) v8.05')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_leading_space(self):
        actual = mmf._is_mmf_header(' ---------- Recipe via Meal-Master (tm) v8.05')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_trailing_space(self):
        actual = mmf._is_mmf_header('---------- Recipe via Meal-Master (tm) v8.05 ')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_only_dashes(self):
        actual = mmf._is_mmf_header('----------')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_only_dashes_and_space(self):
        actual = mmf._is_mmf_header('---------- ')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_other_text(self):
        actual = mmf._is_mmf_header('---------- Anything goes here')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_only_MMMMM_and_dashes(self):
        actual = mmf._is_mmf_header('MMMMM-----')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_only_MMMMM_and_dashes_and_space(self):
        actual = mmf._is_mmf_header('MMMMM----- ')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_MMMMM_other_text(self):
        actual = mmf._is_mmf_header('MMMMM----- Anything goes here')
        expected = True
        self.assertEqual(actual, expected)


class TestIsMmfFooter(unittest.TestCase):

    # only '-----' and 'MMMMM' should be considerd valid

    def test_when_normal(self):
        actual = mmf._is_mmf_footer('-----')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_MMMMM(self):
        actual = mmf._is_mmf_footer('MMMMM')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_empty(self):
        actual = mmf._is_mmf_footer('')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_leading_space(self):
        actual = mmf._is_mmf_footer(' -----')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_trailing_space(self):
        actual = mmf._is_mmf_footer('----- ')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_extra_dash(self):
        actual = mmf._is_mmf_footer('------')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_missing_dash(self):
        actual = mmf._is_mmf_footer('----')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_trailing_text(self):
        actual = mmf._is_mmf_footer('-----TEXT')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_MMMMM_leading_space(self):
        actual = mmf._is_mmf_footer(' MMMMM')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_MMMMM_trailing_space(self):
        actual = mmf._is_mmf_footer('MMMMM ')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_MMMMM_extra_M(self):
        actual = mmf._is_mmf_footer('MMMMMM')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_MMMMM_missing_M(self):
        actual = mmf._is_mmf_footer('MMMM')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_MMMMM_trailing_text(self):
        actual = mmf._is_mmf_footer('MMMMMTEXT')
        expected = False
        self.assertEqual(actual, expected)


class TestTestMetadata(unittest.TestCase):

    def test_when_empty(self):
        actual = mmf._test_metadata('')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_colon(self):
        actual = mmf._test_metadata(':')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_no_attribute_name(self):
        actual = mmf._test_metadata('    : value')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_text_without_colon(self):
        actual = mmf._test_metadata('   Chill before serving.   ')
        expected = False, '', ''
        self.assertEqual(actual, expected)

    def test_when_no_value(self):
        actual = mmf._test_metadata(' Categories: ')
        expected = True, 'Categories', ''
        self.assertEqual(actual, expected)

    def test_when_normal(self):
        actual = mmf._test_metadata(' Title: 21 Club Rice Pudding')
        expected = True, 'Title', '21 Club Rice Pudding'
        self.assertEqual(actual, expected)

    def test_when_extra_spaces(self):
        actual = mmf._test_metadata('    Recipe   By     :     Aunt   Salli   ')
        expected = True, 'Recipe   By', 'Aunt   Salli'
        self.assertEqual(actual, expected)


class TestSplitCategories(unittest.TestCase):

    def test_when_none(self):
        actual = mmf._split_categories('None')
        expected = []
        self.assertEqual(actual, expected)

    def test_when_none_mixed_caps(self):
        actual = mmf._split_categories('noNE')
        expected = []
        self.assertEqual(actual, expected)

    def test_when_one_category(self):
        actual = mmf._split_categories('Dessert')
        expected = ['Dessert']
        self.assertEqual(actual, expected)

    def test_when_multiple_categories(self):
        actual = mmf._split_categories('Dessert,Italian,Easy')
        expected = ['Dessert', 'Italian', 'Easy']
        self.assertEqual(actual, expected)

    def test_when_multiple_categories_with_space(self):
        actual = mmf._split_categories('Dessert, Italian, Easy')
        expected = ['Dessert', 'Italian', 'Easy']
        self.assertEqual(actual, expected)

    def test_when_multiple_categories_with_more_space(self):
        actual = mmf._split_categories(' Dessert , Italian , Easy   ')
        expected = ['Dessert', 'Italian', 'Easy']
        self.assertEqual(actual, expected)


class TestGetYieldAndServings(unittest.TestCase):

    def test_when_empty(self):
        actual = mmf._get_yield_and_servings('')
        expected = '', 0
        self.assertEqual(actual, expected)

    def test_when_number(self):
        actual = mmf._get_yield_and_servings('10')
        expected = '', 10
        self.assertEqual(actual, expected)

    def test_when_number_and_unit(self):
        actual = mmf._get_yield_and_servings('24 cookies')
        expected = '24 cookies', 0
        self.assertEqual(actual, expected)


class TestGetIngredientHeading(unittest.TestCase):
    
    def test_when_empty(self):
        actual = mmf._get_ingredient_heading('')
        expected = ''
        self.assertEqual(actual, expected)
    
    def test_when_not_marked_up(self):
        actual = mmf._get_ingredient_heading('This is some text.')
        expected = ''
        self.assertEqual(actual, expected)

    def test_when_heading(self):
        actual = mmf._get_ingredient_heading('---------------------------------SPAM---------------------------------')
        expected = 'SPAM'
        self.assertEqual(actual, expected)

    def test_when_minimum(self):
        actual = mmf._get_ingredient_heading('-----BAR-----')
        expected = 'BAR'
        self.assertEqual(actual, expected)

    def test_when_MMMMM_heading(self):
        actual = mmf._get_ingredient_heading('MMMMM---------------------------QUICK OATS--------------------------------')
        expected = 'QUICK OATS'
        self.assertEqual(actual, expected)

    def test_when_MMMMM_minimum(self):
        actual = mmf._get_ingredient_heading('MMMMM-----JARS-----')
        expected = 'JARS'
        self.assertEqual(actual, expected)

    def test_when_spaces(self):
        actual = mmf._get_ingredient_heading('-------------------------  This is a  heading.        --------------------------------')
        expected = 'This is a  heading.'
        self.assertEqual(actual, expected)


class TestGetIngredient(unittest.TestCase):

    def test_when_empty(self):
        actual = mmf._get_ingredient('')
        self.assertEqual(actual.quantity, '')
        self.assertEqual(actual.unit, '')
        self.assertEqual(actual.text, '')
        self.assertEqual(actual.is_heading, False)

    def test_when_whitespace(self):
        actual = mmf._get_ingredient('                   ')
        self.assertEqual(actual.quantity, '')
        self.assertEqual(actual.unit, '')
        self.assertEqual(actual.text, '')
        self.assertEqual(actual.is_heading, False)

    def test_1(self):
        actual = mmf._get_ingredient('      1 qt Milk')
        self.assertEqual(actual.quantity, '1')
        self.assertEqual(actual.unit, 'qt')
        self.assertEqual(actual.text, 'Milk')
        self.assertEqual(actual.is_heading, False)

    def test_2(self):
        actual = mmf._get_ingredient('    1/2 qt Milk')
        self.assertEqual(actual.quantity, '1/2')
        self.assertEqual(actual.unit, 'qt')
        self.assertEqual(actual.text, 'Milk')
        self.assertEqual(actual.is_heading, False)

    def test_3(self):
        actual = mmf._get_ingredient('  3 1/2 qt Milk')
        self.assertEqual(actual.quantity, '3 1/2')
        self.assertEqual(actual.unit, 'qt')
        self.assertEqual(actual.text, 'Milk')
        self.assertEqual(actual.is_heading, False)

    def test_4(self):
        actual = mmf._get_ingredient('    1.5 qt Milk')
        self.assertEqual(actual.quantity, '1.5')
        self.assertEqual(actual.unit, 'qt')
        self.assertEqual(actual.text, 'Milk')
        self.assertEqual(actual.is_heading, False)

    def test_5(self):
        actual = mmf._get_ingredient('     .5 qt Milk')
        self.assertEqual(actual.quantity, '.5')
        self.assertEqual(actual.unit, 'qt')
        self.assertEqual(actual.text, 'Milk')
        self.assertEqual(actual.is_heading, False)

    def test_6(self):
        actual = mmf._get_ingredient('    3/4 c  Long-grained rice')
        self.assertEqual(actual.quantity, '3/4')
        self.assertEqual(actual.unit, 'c')
        self.assertEqual(actual.text, 'Long-grained rice')
        self.assertEqual(actual.is_heading, False)

    def test_7(self):
        actual = mmf._get_ingredient('           Raisins (optional)')
        self.assertEqual(actual.quantity, '')
        self.assertEqual(actual.unit, '')
        self.assertEqual(actual.text, 'Raisins (optional)')
        self.assertEqual(actual.is_heading, False)

    def test_8(self):
        actual = mmf._get_ingredient('      1    Egg yolk')
        self.assertEqual(actual.quantity, '1')
        self.assertEqual(actual.unit, '')
        self.assertEqual(actual.text, 'Egg yolk')
        self.assertEqual(actual.is_heading, False)


class TestIsIngredient(unittest.TestCase):

    def test_when_empty(self):
        actual = mmf._is_ingredient('')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_direction(self):
        actual = mmf._is_ingredient('In large bowl, blend oil and sugars on low until well mixed. Add')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_invalid_quantity(self):
        actual = mmf._is_ingredient('     ab qt Milk')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_invalid_unit(self):
        actual = mmf._is_ingredient('        21 Apples')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_spacing_off(self):
        actual = mmf._is_ingredient('     1 qt Milk')
        expected = False
        self.assertEqual(actual, expected)

    def test_when_1(self):
        actual = mmf._is_ingredient('      1 qt Milk')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_2(self):
        actual = mmf._is_ingredient('  1 1/2 c  Whipped cream')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_3(self):
        actual = mmf._is_ingredient('      1    Vanilla bean')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_4(self):
        actual = mmf._is_ingredient('           Raisins (optional)')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_5(self):
        actual = mmf._is_ingredient('    1.5 qt Milk')
        expected = True
        self.assertEqual(actual, expected)

    def test_when_6(self):
        actual = mmf._is_ingredient('      1 c  Oil                                 1 t  Baking soda')
        expected = True
        self.assertEqual(actual, expected)


class TestGetIngredients(unittest.TestCase):

    def test_when_none(self):
        lines = []
        expected = []
        actual = [repr(i) for i in mmf._get_ingredients(lines)]
        self.assertEqual(actual, expected)

    def test_when_empty_line(self):
        lines = [
            ('  ', False),
            ]
        expected = []
        actual = [repr(i) for i in mmf._get_ingredients(lines)]
        self.assertEqual(actual, expected)

    def test_when_empty_lines(self):
        lines = [
            ('  ', False),
            ('  ', False),
            ('  ', False),
            ]
        expected = []
        actual = [repr(i) for i in mmf._get_ingredients(lines)]
        self.assertEqual(actual, expected)

    def test_when_one_column(self):
        lines = [
            ('      1 qt Milk', False),
            ('      1 pt Heavy cream', False),
            ('    1/2 ts Salt', False),
            ('      1    Vanilla bean', False),
            ('    3/4 c  Long-grained rice', False),
            ('      1 c  Granulated sugar', False),
            ('      1    Egg yolk', False),
            ('  1 1/2 c  Whipped cream', False),
            ('           Raisins (optional)', False),
            ]
        expected = [
            '{1} {qt} {Milk}',
            '{1} {pt} {Heavy cream}',
            '{1/2} {ts} {Salt}',
            '{1} {} {Vanilla bean}',
            '{3/4} {c} {Long-grained rice}',
            '{1} {c} {Granulated sugar}',
            '{1} {} {Egg yolk}',
            '{1 1/2} {c} {Whipped cream}',
            '{} {} {Raisins (optional)}',
            ]
        actual = [repr(i) for i in mmf._get_ingredients(lines)]
        self.assertEqual(actual, expected)

    def test_when_one_column_with_extra_lines(self):
        lines = [
            ('  ', False),
            ('      1 qt Milk', False),
            ('      1 pt Heavy cream', False),
            ('    1/2 ts Salt', False),
            ('      1    Vanilla bean', False),
            ('    3/4 c  Long-grained rice', False),
            ('  ', False),
            ('      1 c  Granulated sugar', False),
            ('      1    Egg yolk', False),
            ('  1 1/2 c  Whipped cream', False),
            ('           Raisins (optional)', False),
            ('  ', False),
            ]
        expected = [
            '{1} {qt} {Milk}',
            '{1} {pt} {Heavy cream}',
            '{1/2} {ts} {Salt}',
            '{1} {} {Vanilla bean}',
            '{3/4} {c} {Long-grained rice}',
            '{1} {c} {Granulated sugar}',
            '{1} {} {Egg yolk}',
            '{1 1/2} {c} {Whipped cream}',
            '{} {} {Raisins (optional)}',
            ]
        actual = [repr(i) for i in mmf._get_ingredients(lines)]
        self.assertEqual(actual, expected)

    def test_when_one_column_with_headings(self):
        lines = [
            ('FOR THE PIE', True),
            ('  1 1/2 c  All-Purpose Flour', False),
            ('    1/2 ts Salt', False),
            ('    1/2 c  Shortening', False),
            ('      5 tb ICE Water', False),
            ('      8 c  Apples [peeled & sliced]', False),
            ('    1/4 c  Granulated Sugar', False),
            ('      2 tb All-Purpose Flour', False),
            ('    1/2 ts Nutmeg, Ground', False),
            ('      2 tb Lemon Juice', False),
            ('      1 ts Cinnamon, Ground', False),
            ('', False),
            ('FOR THE TOPPING', True),
            ('    1/2 c  Granulated Sugar', False),
            ('    1/2 c  All-Purpose Flour', False),
            ('    1/3 c  Butter', False),
            ('      1 lg Paper Bag', False),
            ('           Vanilla Ice Cream', False),
            ]
        expected = [
            '----- FOR THE PIE -----',
            '{1 1/2} {c} {All-Purpose Flour}',
            '{1/2} {ts} {Salt}',
            '{1/2} {c} {Shortening}',
            '{5} {tb} {ICE Water}',
            '{8} {c} {Apples [peeled & sliced]}',
            '{1/4} {c} {Granulated Sugar}',
            '{2} {tb} {All-Purpose Flour}',
            '{1/2} {ts} {Nutmeg, Ground}',
            '{2} {tb} {Lemon Juice}',
            '{1} {ts} {Cinnamon, Ground}',
            '----- FOR THE TOPPING -----',
            '{1/2} {c} {Granulated Sugar}',
            '{1/2} {c} {All-Purpose Flour}',
            '{1/3} {c} {Butter}',
            '{1} {lg} {Paper Bag}',
            '{} {} {Vanilla Ice Cream}',
            ]
        actual = [repr(i) for i in mmf._get_ingredients(lines)]
        self.assertEqual(actual, expected)

    def test_when_two_columns(self):
        lines = [
            ('  1 1/2 lb Hamburger                           1 ds Salt', False),
            ('      1 c  Onion; chopped                    1/2 c  Water', False),
            ('      1 c  Green pepper; chopped             1/8 t  Hot pepper sauce', False),
            ('      1 T  Oil                           ', False),
            ]
        expected = [
            '{1 1/2} {lb} {Hamburger}',
            '{1} {c} {Onion; chopped}',
            '{1} {c} {Green pepper; chopped}',
            '{1} {T} {Oil}',
            '{1} {ds} {Salt}',
            '{1/2} {c} {Water}',
            '{1/8} {t} {Hot pepper sauce}',
            ]
        actual = [repr(i) for i in mmf._get_ingredients(lines)]
        self.assertEqual(actual, expected)

    def test_when_two_columns_with_headings(self):
        lines = [
            ('HEADING 1', True),
            ('  1 1/2 lb Hamburger                           1 ds Salt', False),
            ('      1 c  Onion; chopped                    1/2 c  Water', False),
            ('HEADING 2', True),
            ('      1 c  Green pepper; chopped             1/8 t  Hot pepper sauce', False),
            ('      1 T  Oil                           ', False),
            ('HEADING 3', True),
            ('      7 oz Jack/Mozz. cheese slices          1/2 c  Parmesan cheese; grated', False),
            ]
        expected = [
            '----- HEADING 1 -----',
            '{1 1/2} {lb} {Hamburger}',
            '{1} {c} {Onion; chopped}',
            '{1} {ds} {Salt}',
            '{1/2} {c} {Water}',
            '----- HEADING 2 -----',
            '{1} {c} {Green pepper; chopped}',
            '{1} {T} {Oil}',
            '{1/8} {t} {Hot pepper sauce}',
            '----- HEADING 3 -----',
            '{7} {oz} {Jack/Mozz. cheese slices}',
            '{1/2} {c} {Parmesan cheese; grated}',
            ]
        actual = [repr(i) for i in mmf._get_ingredients(lines)]
        self.assertEqual(actual, expected)

    def test_when_one_column_with_line_continuations(self):
        lines = [
            ('      1 ts Salt', False),
            ('           Fresh ground', False),
            ('           -black pepper to', False),
            ('           -taste', False),
            ('      1 cn (6-oz) tomato paste', False),
            ('      1 cn (30-oz) red kidney beans', False),
            ('           -drained', False),
            ]
        expected = [
            '{1} {ts} {Salt}',
            '{} {} {Fresh ground black pepper to taste}',
            '{1} {cn} {(6-oz) tomato paste}',
            '{1} {cn} {(30-oz) red kidney beans drained}',
            ]
        actual = [repr(i) for i in mmf._get_ingredients(lines)]
        self.assertEqual(actual, expected)

    def test_when_two_columns_with_line_continuations(self):
        lines = [
            ('      1 lg Artichoke; -=OR=-                        - and thinly sliced', False),
            ('      2 md -Artichokes                         6    Leaves butter lettuce', False),
            ('      1 c  Water; acidulated with                   - sliced into 1/4" strips', False),
            ('           - the juice of                           -=OR=- a handful of', False),
            ('      1    Lemon                                    - Sorrel leaves, sliced', False),
            ('      2    Garlic cloves                       1 tb Chopped parsley', False),
            ('      1 tb Virgin olive oil                    2    Mint leaves; chopped', False),
            ('      1 lg Leek; white part only -=OR=-             Salt', False),
            ('      2 md Leeks, white part only          5 1/2 c  Water', False),
            ('           - washed and sliced                 1 lb Fresh peas; shucked, -=OR=-', False),
            ('      1 sm New potato; quartered               1 c  -Frozen peas', False),
            ]
        expected = [
            '{1} {lg} {Artichoke; -=OR=-}',
            '{2} {md} {-Artichokes}',
            '{1} {c} {Water; acidulated with the juice of}',
            '{1} {} {Lemon}',
            '{2} {} {Garlic cloves}',
            '{1} {tb} {Virgin olive oil}',
            '{1} {lg} {Leek; white part only -=OR=-}',
            '{2} {md} {Leeks, white part only washed and sliced}',
            '{1} {sm} {New potato; quartered and thinly sliced}',
            '{6} {} {Leaves butter lettuce sliced into 1/4" strips =OR=- a handful of Sorrel leaves, sliced}',
            '{1} {tb} {Chopped parsley}',
            '{2} {} {Mint leaves; chopped}',
            '{} {} {Salt}',
            '{5 1/2} {c} {Water}',
            '{1} {lb} {Fresh peas; shucked, -=OR=-}',
            '{1} {c} {-Frozen peas}',
            ]
        actual = [repr(i) for i in mmf._get_ingredients(lines)]
        self.assertEqual(actual, expected)


class TestParagraphizeDirections(unittest.TestCase):

    def test_when_none(self):
        lines = []
        expected = []
        actual = mmf._paragraphize_directions(lines)
        self.assertEqual(actual, expected)

    def test_when_empty(self):
        lines = ['']
        expected = []
        actual = mmf._paragraphize_directions(lines)
        self.assertEqual(actual, expected)

    def test_when_single_line(self):
        lines = ['  Brown cut up pieces of meat.']
        expected = ['Brown cut up pieces of meat.']
        actual = mmf._paragraphize_directions(lines)
        self.assertEqual(actual, expected)

    def test_when_extra_lines(self):
        lines = ['  ', '  Brown cut up pieces of meat.', '  ']
        expected = ['Brown cut up pieces of meat.']
        actual = mmf._paragraphize_directions(lines)
        self.assertEqual(actual, expected)

    def test_when_more_extra_lines(self):
        lines = [
            '   ',
            '  ',
            '  Brown cut up pieces of meat.',
            '    ',
            '  Brown cut up pieces of meat!',
            '   ',
            '  ',
            '   ',
            ]
        expected = [
            'Brown cut up pieces of meat.',
            'Brown cut up pieces of meat!',
            ]
        actual = mmf._paragraphize_directions(lines)
        self.assertEqual(actual, expected)

    def test_when_paragraph(self):
        lines = [
            '  Brown cut up pieces of meat.Season with chili powder,salt and black',
            '  pepper.Add chopped vegetables and V - 8 vegetable juice. Add ketchup',
            '  and Worcestershire sauce to taste.',
            ]
        expected = [
            'Brown cut up pieces of meat.Season with chili powder,salt and black pepper.Add chopped vegetables and V - 8 vegetable juice. Add ketchup and Worcestershire sauce to taste.',
            ]
        actual = mmf._paragraphize_directions(lines)
        self.assertEqual(actual, expected)

    def test_when_multiple_paragraphs(self):
        lines = [
            '  The kind of chiles that you use determine the final flavor, you can',
            '  experiment with different kinds or mixing the different kinds of chiles.',
            '  But this is the basic recipe for prepare salsas with dry chiles.',
            '  ',
            '  Wash the chiles in water and discard the seeds and threads of chiles. Let',
            '  stand in water at least 2 or 3 hours or all the night, if you do not have',
            '  time let the chiles in warm water at least 30 min.',
            '  ',
            '  Then ground with the other ingredients.',
            ]
        expected = [
            'The kind of chiles that you use determine the final flavor, you can experiment with different kinds or mixing the different kinds of chiles. But this is the basic recipe for prepare salsas with dry chiles.',
            'Wash the chiles in water and discard the seeds and threads of chiles. Let stand in water at least 2 or 3 hours or all the night, if you do not have time let the chiles in warm water at least 30 min.',
            'Then ground with the other ingredients.',
            ]
        actual = mmf._paragraphize_directions(lines)
        self.assertEqual(actual, expected)

    def test_when_multiple_paragraphs_separated_by_paragraph_marker(self):
        lines = [
            '  The kind of chiles that you use determine the final flavor, you can',
            '  experiment with different kinds or mixing the different kinds of chiles.',
            '  But this is the basic recipe for prepare salsas with dry chiles.\x14',
            '  Wash the chiles in water and discard the seeds and threads of chiles. Let',
            '  stand in water at least 2 or 3 hours or all the night, if you do not have',
            '  time let the chiles in warm water at least 30 min.\x14',
            '  Then ground with the other ingredients.',
            ]
        expected = [
            'The kind of chiles that you use determine the final flavor, you can experiment with different kinds or mixing the different kinds of chiles. But this is the basic recipe for prepare salsas with dry chiles.',
            'Wash the chiles in water and discard the seeds and threads of chiles. Let stand in water at least 2 or 3 hours or all the night, if you do not have time let the chiles in warm water at least 30 min.',
            'Then ground with the other ingredients.',
            ]
        actual = mmf._paragraphize_directions(lines)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()