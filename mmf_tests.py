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



if __name__ == '__main__':
    unittest.main()