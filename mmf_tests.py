import unittest

import mmf

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



if __name__ == '__main__':
    unittest.main()