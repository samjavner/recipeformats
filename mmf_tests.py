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


if __name__ == '__main__':
    unittest.main()