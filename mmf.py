"""Recipe parsing for Meal-Master format (.mmf) files.

Use parse_recipes to parse multiple recipes.
Use parse_recipe to parse a single recipe.
Use split_recipe_lines to yield a list of lines for each recipe that can be
passed into parse_recipe to parse only a single recipe out of multiple recipes.

You may run into issues with text encoding, as Meal-Master is an old program.
You may have to use something like encoding='cp437' depending on the file.
"""

import re

__all__ = ['Recipe', 'Ingredient', 'parse_recipes', 'parse_recipe',
           'split_recipe_lines']

class Recipe:
    """Represents a Meal-Master recipe.

    Attributes:
        title: A string for the recipe title.
        categories: A list of strings for each category.
        yield_: A string (perhaps empty) for the yield (e.g. '24 muffins').
        servings: An integer (perhaps 0) of the number of servings specified.
        ingredients: A list of Ingredient objects.
        directions: A list of strings representing steps or paragraphs.
    """

    def __init__(self):
        """Initializes Recipe with default values."""
        self.title = ''
        self.categories = []
        self.yield_ = ''
        self.servings = 0
        self.ingredients = []
        self.directions = []


class Ingredient:
    """Represents an ingredient or ingredient heading from a Meal-Master recipe."""

    def __init__(self, quantity, unit, text, is_heading):
        """Initializes Ingredient with the specified values.

        Args:
            quantity: String (perhaps empty) for the quantity (e.g. '12 1/2')
            unit: String (0-2 characters) for the unit (e.g. 'tb')
            text: String for the text or heading text (e.g. 'apples')
            is_heading: Boolean indicating if this is heading text (True) or
                ingredient text (False)
        """
        self.quantity = quantity
        self.unit = unit
        self.text = text
        self.is_heading = is_heading

    def __repr__(self):
        """Returns representation of ingredient (different for heading or not)."""
        if self.is_heading:
            r = '----- %s -----' % self.text 
        else:
            r = '{%s} {%s} {%s}' % (self.quantity, self.unit, self.text)
        return r

    def __str__(self):
        """Returns ingredient text concatenated back together."""
        if self.is_heading:
            return self.text
        else:
            return (self.quantity + ' ' + (self.unit + ' ' + self.text).strip()).strip()


def parse_recipes(lines):
    """Parses multiple recipes from the given lines.

    Parses multiple recipes when given an iterable of strings. The lines
    are allowed to have trailing newline characters and these will be removed.

    Args:
        lines: An iterable of strings containing the lines of multiple recipes.

    Yields:
        A Recipe corresponding to each of the recipes in the given lines.
    """
    return (parse_recipe(recipe_lines) for recipe_lines in split_recipe_lines(lines))


def split_recipe_lines(lines):
    """Breaks up multiple recipes into lists of lines for each recipe.
    
    Takes an iterable of lines corresponding to multiple recipes and yields
    a list of lines for each of the recipes. Removes trailing whitespace
    including newline characters from the end of each line.

    Args:
        lines: An iterable of strings containing the lines of multiple recipes.

    Yields:
        A list of strings for each recipe.
    """
    found_recipe = False
    recipe_lines = []
    for line in lines:
        line = line.rstrip()
        if _is_mmf_header(line):
            found_recipe = True
            recipe_lines = []
        recipe_lines.append(line)
        if found_recipe and _is_mmf_footer(line):
            found_recipe = False
            yield recipe_lines


def parse_recipe(lines):
    """Parses a recipe from the given lines.

    Parses a single recipe when given an iterable of strings. These lines
    should not have a trailing newline character.

    Args:
        lines: An iterable of strings containing the lines of the recipe.

    Returns:
        A Recipe corresponding to the given lines.
    """
    recipe = Recipe()
    it = iter(lines)
    current = ''
    try:
        current = _parse_mmf_header(it, current, recipe)
        current = _parse_title(it, current, recipe)
        current = _parse_categories(it, current, recipe)
        current = _parse_yield(it, current, recipe)
        current = _parse_ingredients(it, current, recipe)
        current = _parse_directions(it, current, recipe)
    except StopIteration:
        pass
    return recipe


def _skip_empty(it, current):
    """Skips empty lines from the iterator and returns the current (non-empty) line."""
    while _is_empty(current):
        current = next(it)
    return current


def _is_empty(line):
    """Returns whether a line is empty (contains only white space)."""
    return not line.strip()


def _is_mmf_header(line):
    """Returns whether a line is a valid MMF header."""
    return line.startswith('---------- ') or line.startswith('MMMMM----- ')


def _is_mmf_footer(line):
    """Returns whether a line is a valid MMF footer."""
    return line == '-----' or line == 'MMMMM'


def _test_metadata(line):
    """Returns a tuple indicating whether a line contains recipe metadata
    as well as the attribute name and value.

    A line is considered to contain recipe metadata if it contains a colon.
    The attribute name comes before the colon and the value comes after.
    """
    index = line.find(':')
    if index >= 0:
        return True, line[:index].strip(), line[index+1:].strip()
    else:
        return False, '', ''


def _parse_mmf_header(it, current, recipe):
    """Parses the MMF header and moves to the next line if found."""
    current = _skip_empty(it, current)
    if _is_mmf_header(current):
        current = next(it)
    return current


def _parse_title(it, current, recipe):
    """Parses the Title line and moves to the next line if found."""
    current = _skip_empty(it, current)
    is_metadata, attribute, value = _test_metadata(current)
    if is_metadata and attribute.lower() == 'title':
        recipe.title = value
        current = next(it)
    return current


def _parse_categories(it, current, recipe):
    """Parses the Categories line and moves to the next line if found."""
    current = _skip_empty(it, current)
    is_metadata, attribute, value = _test_metadata(current)
    if is_metadata and attribute.lower() == 'categories':
        recipe.categories = _split_categories(value)
        current = next(it)
    return current


def _split_categories(value):
    """Splits the categories on comma. Returns a list of categories or if
    there is one category named 'none' returns an empty list."""
    categories = [c.strip() for c in value.split(',')]
    if len(categories) == 1 and categories[0].lower() == 'none':
        return []
    return categories


def _parse_yield(it, current, recipe):
    """Parses the Yield or Servings line and moves to the next line if found."""
    current = _skip_empty(it, current)
    is_metadata, attribute, value = _test_metadata(current)
    if is_metadata and attribute.lower() in ['servings', 'yield']:
        recipe.yield_, recipe.servings = _get_servings_and_yield(value)
        current = next(it)
    return current


def _get_servings_and_yield(value):
    """Returns a tuple consisting of the yield value and servings value.

    Only one of these has a meaningful value while the other is set to a
    default value. If there is an integer followed optionally by the word
    'serving' or 'servings' then return this integer value as the number
    of servings, otherwise return the input value as the yield.
    """
    if value.lower().endswith('servings'):
        servings = value[:-8].strip()
    elif value.lower().endswith('serving'):
        servings = value[:-7].strip()
    else:
        servings = value

    try:
        return '', int(servings)
    except ValueError:
        return value, 0


def _parse_ingredients(it, current, recipe):
    """Parses valid ingredient lines and advances to the first line that
    is not a valid ingredient line.

    Valid ingredient lines are ingredient heading lines, ingredient lines,
    and empty lines.
    """
    ingredients = [] # list of tuples (text, is_heading)
    try:
        while True:
            heading = _get_ingredient_heading(current)
            if heading:
                ingredients.append((heading, True))
            elif _is_ingredient(current):
                ingredients.append((current, False))
            elif _is_empty(current):
                pass
            else:
                break
            current = next(it)
    finally:
        # Add the ingredients even if we reach end of iterable
        # and StopIteration is raised.
        recipe.ingredients = _get_ingredients(ingredients)
    return current


# ingredient starts with:
# 7 digits, periods, slashes or spaces
# followed by a space
# followed by 2 digits or spaces
# followed by a space
_ingredient_re = re.compile(r'^[\d\./ ]{7} [A-Za-z ]{2} ')


def _is_ingredient(line):
    """Tests whether a line is an ingredient line."""
    return bool(_ingredient_re.match(line))


# heading starts with:
# optional MMMMM
# followed by at least 5 -
# followed by at least 1 non - character
# followed by at least 5 -
_heading_re = re.compile(r'^(?:MMMMM)?-----+([^-]+)-----+')


def _get_ingredient_heading(line):
    """Returns the heading from a heading line or an empty string if this
    is not an ingredient heading line."""
    match = _heading_re.match(line)
    if not match:
        return ''
    return match.group(1).strip()


def _get_ingredients(line_pairs):
    """Gets a list of Ingredient from provided ingredients.

    Args:
        A list of tuples (text, is_heading)

    Returns:
        A list of Ingredient parsed from the provided lines.
    """
    ingredients = []

    # Text may or may not be multiple columns.
    # We know if there are multiple columns if the line is more than
    # 41 characters long.
    column1 = [] # list of text from column 1 since last heading found
    column2 = [] # list of text from column 2 since last heading found

    # Add headings right away.
    # In between headings, store up values from column1 and column2
    # When we find another heading or the end of the ingredients, then
    # process column1 and column2.
    for line, is_heading in line_pairs:
        if is_heading:
            _add_ingredients(ingredients, column1, column2)
            if line:
                ingredients.append(Ingredient('', '', line, True))
        else:
            if len(line.rstrip()) <= 41:
                column1.append(line)
            else:
                column1.append(line[:41])
                column2.append(line[41:])
    _add_ingredients(ingredients, column1, column2)

    return ingredients


def _add_ingredients(ingredients, column1, column2):
    """Add ingredients from two columns."""
    # Process down then across. It's possible that the file was exported
    # to read across then down, but we're ignoring that possibility.
    # This could be a flag we could pass in.
    column1.extend(column2)

    # A line where the first non-whitespace character is a '-' is a
    # convention that indicates that this line should be appended to the
    # previous line. As a result, we never append the ingredient right away.
    # Instead wait until we find a line that does not begin with '-' and
    # then add the ingredient.
    previous = ''
    for ingredient in column1:
        if ingredient.lstrip().startswith('-'):
            previous += ' ' + ingredient.lstrip()[1:].strip()
        else:
            if previous.lstrip():
                ingredients.append(_get_ingredient(previous))
            previous = ingredient
    if previous.lstrip():
        ingredients.append(_get_ingredient(previous))
    column1[:] = [] # clear
    column2[:] = [] # clear


def _get_ingredient(ingredient):
    """Parse ingredient line into Ingredient."""
    # Format of line: "QQQQQQQ UU TTTTTTTTTTTTTTTTTTTTTTTTTTT..."
    quantity = ingredient[:7].strip()
    unit = ingredient[8:10].strip()
    text = ingredient[11:].strip()
    return Ingredient(quantity, unit, text, False)


def _parse_directions(it, current, recipe):
    """Parse directions section by adding lines until we reach the footer."""
    directions = []
    try:
        while not _is_mmf_footer(current):
            directions.append(current)
            current = next(it)
    finally:
        # Add the directions even if we reach end of iterable
        # and StopIteration is raised.
        recipe.directions = _paragraphize_directions(directions)
    return current


def _paragraphize_directions(lines):
    """Group directions lines into paragraphs."""
    # Current algorithm adds a paragraph when there is an empty line.
    # Also add a paragraph when we see the character \x14 which is used
    # in some files to indicate a paragraph break. We could have smarter
    # grouping that creates new paragraphs when a line is "short", which
    # indicates that the next line ought to start a new paragraph.
    directions = []
    current = ''
    for line in lines:
        if _is_empty(line):
            if current:
                directions.append(current)
                current = ''
        elif line.endswith('\x14'):
            if current: current += ' '
            current += line[:-1].strip()
            if current:
                directions.append(current)
                current = ''
        else:
            if current: current += ' '
            current += line.strip()
    if current:
        directions.append(current)
    return directions


if __name__ == '__main__':
    with open('c:/Code/python/recipe/.samples/v1.mmf', encoding='cp437') as v1:
        print()
        for recipe in list(parse_recipes(v1))[:]:
            print('Title:       %s' % recipe.title)
            print('Categories:  %s' % recipe.categories)
            print('Yield:       %s' % recipe.yield_)
            print('Servings:    %s' % recipe.servings)
            print('Ingredients: %s' % recipe.ingredients)
            print('Directions:  %s' % recipe.directions)
            print()

