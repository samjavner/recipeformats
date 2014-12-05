"""Recipe parsing for MasterCook 5+ format (.mx2) files.

Use parse_file to parse a file.
"""

import xml.etree.ElementTree as ET

__all__ = ['Info', 'Recipe', 'Rating', 'Ingredient', 'parse_file']


class Info:
    """Represents file-level information for a MasterCook 5+ .mx2 file.

    Attributes:
        source: File source application (e.g. 'MasterCook').
        date: Date string (e.g. 'September 19, 2014').
    """

    def __init__(self, source, date):
        """Initializes Info with provided values."""
        self.source = source
        self.date = date


class Recipe:
    """Represents a recipe in a MasterCook 5+ .mx2 file.

    Attributes:
        name: Recipe name string.
        author: Author string.
        source: Source string.
        copyright: Copyright string.
        servings: Number of servings string.
        preparation_time: Preparation time string.
        total_time: Total recipe time string.
        cuisine: Type of cuisine string (e.g. 'Chinese').
        description: Recipe description string.
        note: Recipe note string.
        serving_ideas: Recipe serving ideas string.
        suggested_wine: Wine suggestion string.
        yield_: Recipe yield string (e.g. '24 muffins').
        alternate_source: Source other than source/author (e.g. 'www.example.com').
        alternate_source_label: Label for alternate source (e.g. 'Web Page').
        alternate_time: Amount of time other than preparation/total.
        alternate_time_label: Label for alternate time (e.g. 'Cooking Time').
        categories: List of category strings.
        ratings: List of Rating objects.
        ingredients: List of Ingredient objects.
        directions: List of direction strings.
    """

    def __init__(self):
        """Initializes Recipe with default values."""
        self.name = ''
        self.author = ''
        self.source = ''
        self.copyright = ''
        self.servings = ''
        self.preparation_time = ''
        self.total_time = ''
        self.cuisine = ''
        self.description = ''
        self.note = ''
        self.serving_ideas = ''
        self.suggested_wine = ''
        self.yield_ = ''
        self.alternate_source = ''
        self.alternate_source_label = ''
        self.alternate_time = ''
        self.alternate_time_label = ''
        self.categories = []
        self.ratings = []
        self.ingredients = []
        self.directions = []


class Rating:
    """Represents a recipe rating.

    Attributes:
        name: Name of the rating (e.g. 'Difficulty', 'Taste').
        value: Integer value (0-10).
    """

    def __init__(self, name, value):
        """Initializes Rating with provided values."""
        self.name = name
        self.value = value

    def __repr__(self):
        """Provides default string representation of Rating."""
        return self.name + ': ' + str(self.value)


class Ingredient:
    """Represents a recipe ingredient.

    Attributes:
        quantity: Amount string (e.g. '1/2', '2', '').
        unit: Measure of unit string (e.g. 'cup', 'tablespoons', '').
        name: Ingredient name (e.g. 'apple', 'salt').
        preparation: Preparation method (e.g. 'chopped', '').
        code: Ingredient code:
            'I' or '' = Ingredient
            'R' = Recipe
            'S' = Subtitle
            'T' = Text
    """

    def __init__(self, quantity, unit, name, preparation, code):
        """Initializes Ingredient with provided values."""
        self.quantity = quantity
        self.unit = unit
        self.name = name
        self.preparation = preparation
        self.code = code

    def __repr__(self):
        """Provides default string representation of Ingredient."""
        return '{%s} {%s} {%s} {%s} {%s}' % (self.quantity, self.unit, self.name, self.preparation, self.code)


def parse_file(filename):
    """Parses a .mx2 file.

    Args:
        filename: File name of the .mx2 file to parse.

    Returns: 
        A tuple containing an Info object and a list of Recipe objects.
    """
    with open(filename) as f:
        s = _load_mx2_into_string(f)
    return _parse_string(s)


def _load_mx2_into_string(file):
    """Loads a .mx2 file into a string. Fixes the XML declaration if necessary."""
    return ''.join(_get_mx2_iterator(file))


def _get_mx2_iterator(file):
    """Fixes the XML declaration on the first line of the file and then returns
    the rest of the lines unchanged.

    MasterCook outputs files with an XML declaration that is not well-formed.
    """
    first = True
    for line in file:
        if first and line == '<?xml version="1.0" standalone="yes" encoding="ISO-8859-1"?>\n':
            yield '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n'
        else:
            first = False
            yield line


def _parse_string(string):
    """Parses a mx2 XML string.

    Args:
        string: XML content to parse with root 'mx2' element.

    Returns: 
        A tuple containing an Info object and a list of Recipe objects.
    """
    mx2 = ET.fromstring(string)
    return _parse_info(mx2), _parse_recipes(mx2)


def _parse_info(mx2):
    """Parses Info from an 'mx2' Element."""
    source = mx2.get('source', '')
    date = mx2.get('date', '')
    return Info(source, date)


def _parse_recipes(mx2):
    """Parses a list of Recipe objects from an 'mx2' Element."""
    recipes = []
    for rcpe in mx2.iter('RcpE'):
        # TODO: Next recipe could be embedded recipe
        recipes.append(_parse_recipe(rcpe))
    return recipes


def _parse_recipe(rcpe):
    """Parses a Recipe from a 'RcpE' Element."""
    recipe = Recipe()

    recipe.name = rcpe.get('name', '')
    recipe.author = rcpe.get('author', '')
    recipe.source = rcpe.findtext('Srce', '').strip()
    recipe.copyright = rcpe.findtext('CpyR', '').strip()
    recipe.cuisine = rcpe.findtext('Natn', '').strip()
    recipe.description = rcpe.findtext('Desc', '').strip()
    recipe.note = rcpe.findtext('Note', '').strip()
    recipe.serving_ideas = rcpe.findtext('SrvI', '').strip()
    recipe.suggested_wine = rcpe.findtext('Wine', '').strip()
    recipe.servings = _findget(rcpe, 'Serv', 'qty', '')
    recipe.preparation_time = _findget(rcpe, 'PrpT', 'elapsed', '')
    recipe.total_time = _findget(rcpe, 'TTim', 'elapsed', '')

    yield_ = _find(rcpe, 'Yield')
    qty = yield_.get('qty', '')
    unit = yield_.get('unit', '')
    recipe.yield_ = (qty + ' ' + unit).strip()

    alts = _find(rcpe, 'AltS')
    recipe.alternate_source = alts.get('source', '')
    recipe.alternate_source_label = alts.get('label', '')

    altt = _find(rcpe, 'AltT')
    recipe.alternate_time = altt.get('elapsed', '')
    recipe.alternate_time_label = altt.get('label', '')

    for catt in _find(rcpe, 'CatS').iter('CatT'):
        recipe.categories.append(catt.text.strip())

    for rats in _find(rcpe, 'RatS').iter('RatE'):
        name = rats.get('name', '')
        try:
            value = int(rats.get('value', ''))
        except ValueError:
            pass
        else:
            recipe.ratings.append(Rating(name, value))

    for ingr in rcpe.iter('IngR'):
        quantity = ingr.get('qty', '')
        unit = ingr.get('unit', '')
        name = ingr.get('name', '')
        preparation = ingr.findtext('IPrp', '').strip()
        code = ingr.get('code', '')
        # TODO: INtI, IERp
        recipe.ingredients.append(Ingredient(quantity, unit, name, preparation, code))

    for dirt in _find(rcpe, 'DirS').iter('DirT'):
        # TODO: img
        # TODO: replace '\r\n' with '\n' ??
        recipe.directions.append(dirt.text.strip())

    # TODO: img
    # TODO: Nutr

    return recipe


def _find(element, tag):
    """Finds the first subelement with the given tag name.

    Returns the subelement, or an empty element with no attributes or
    subelements if no subelement with the given tag name was found.
    """
    subelement = element.find(tag)
    if subelement is None:
        return ET.Element(tag)
    else:
        return subelement


def _findget(element, tag, key, default=None):
    """Finds the first subelement with the given tag name and gets its
    element attribute named key.

    Returns the attribute value, or default if the subelement with the given
    tag name was not found or the attribute was not found.
    """
    subelement = element.find(tag)
    if subelement is None:
        return default
    else:
        return subelement.get(key, default)


if __name__ == '__main__':

    info, recipes = parse_file('c:/Code/python/recipeformats/.samples/f.mx2')

    print()

    lines = [
        'Source:       %s' % info.source,
        'Date:         %s' % info.date,
    ]

    for line in lines:
        print(line)

    print()

    for recipe in recipes:

        lines = [
            'Name:         %s' % recipe.name,
            'Author:       %s' % recipe.author,
            'Source:       %s' % recipe.source,
            'Copyright:    %s' % recipe.copyright,
            'Cuisine:      %s' % recipe.cuisine,
            'Description:  %s' % recipe.description,
            'Note:         %s' % recipe.note,
            'Serving Idea: %s' % recipe.serving_ideas,
            'Wine:         %s' % recipe.suggested_wine,
            'Servings:     %s' % recipe.servings,
            'Prep Time:    %s' % recipe.preparation_time,
            'Total Time:   %s' % recipe.total_time,
            'Yield:        %s' % recipe.yield_,
            'Alt S Label:  %s' % recipe.alternate_source_label,
            'Alt Source:   %s' % recipe.alternate_source,
            'Alt T Label:  %s' % recipe.alternate_time_label,
            'Alt Time:     %s' % recipe.alternate_time,
            'Categories:   %s' % recipe.categories,
            'Ratings:      %s' % recipe.ratings,
            'Ingredients:  %s' % recipe.ingredients,
            'Directions:   %s' % recipe.directions,
        ]

        for line in lines:
            print(line)

        print()