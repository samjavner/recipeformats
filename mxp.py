"""Recipe parsing for MasterCook 1-4 format (.mxp) files.

Use parse_recipes to parse multiple recipes.
Use parse_recipe to parse a single recipe.
Use split_recipe_lines to yield a list of lines for each recipe that can be
passed into parse_recipe to parse only a single recipe out of multiple recipes.
"""

import re

__all__ = ['Recipe', 'Ingredient', 'parse_recipes', 'parse_recipe',
           'split_recipe_lines']

class Recipe:
    """Represents a MasterCook 1-4 recipe.

    Attributes:
        title: A string for the recipe title.
        recipe_by: A string for the recipe source/author.
        serving_size: A string for the serving size.
        preparation_time: A string for the preparation time.
        categories: A list of strings for each category.
        ingredients: A list of Ingredient objects.
        directions: A list of strings representing steps or paragraphs.
        notes: A list of strings representing notes.
    """

    def __init__(self):
        """Initializes Recipe with default values."""
        self.title = ''
        self.recipe_by = ''
        self.serving_size = ''
        self.preparation_time = ''
        self.categories = []
        self.ingredients = []
        self.directions = []
        self.notes = []


class Ingredient:
    """Represents an ingredient from a MasterCook 1-4 recipe."""

    def __init__(self, amount, measure, ingredient, preparation_method):
        """Initializes Ingredient with the specified values.

        Args:
            amount: String (0-6 characters) for the quantity (e.g. '12 1/2')
            measure: String (0-12 characters) for the unit (e.g. 'tb')
            ingredient: String for the ingredient text.
            preparation_method: String for the preparation method.
        """
        self.amount = amount
        self.measure = measure
        self.ingredient = ingredient
        self.preparation_method = preparation_method

    def __repr__(self):
        """Returns representation of ingredient (different for heading or not)."""
        # Tests rely on this representation format, so think again before
        # changing this format.
        return '{%s} {%s} {%s} {%s}' % (self.amount, self.measure, self.ingredient, self.preparation_method)

    def __str__(self):
        """Returns ingredient text concatenated back together."""
        text = (self.amount + ' ' + (self.measure + ' ' + self.ingredient).strip()).strip()
        if preparation_method:
            text += ' -- ' + preparation_method
        return text


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
    found_first_recipe = False
    recipe_lines = []
    for line in lines:
        line = line.rstrip()
        if _is_mxp_header(line):
            if found_first_recipe:
                yield recipe_lines
            found_first_recipe = True
            recipe_lines = []
        recipe_lines.append(line)
    if found_first_recipe and recipe_lines:
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
        current = _parse_mxp_header(it, current, recipe)
        current = _parse_title(it, current, recipe)
        current = _parse_recipe_by(it, current, recipe)
        current = _parse_serving_size_preparation_time(it, current, recipe)
        current = _parse_categories(it, current, recipe)
        current = _parse_ingredients(it, current, recipe)
        current = _parse_directions(it, current, recipe)
        current = _parse_notes(it, current, recipe)
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


def _is_mxp_header(line):
    """Returns whether a line is a valid MXP header."""
    line = line.strip()
    return (len(line) > 2 and line.startswith('*') and line.endswith('*') and
            line[1:-1].strip().lower().startswith('exported from'))


def _is_mxp_footer(line):
    """Returns whether a line is a valid MXP footer."""
    return line.strip().startswith('- - - - - - - - - - - - - - - - - -')


def _test_metadata(line):
    """Returns a tuple indicating whether a line contains recipe metadata
    as well as the attribute name and value.

    A line is considered to contain recipe metadata if it contains a colon
    and also contains some non-whitespace before the colon. The attribute name
    comes before the colon and the value comes after.
    """
    index = line.find(':')
    if index >= 0:
        attribute = line[:index].strip()
        value = line[index+1:].strip()
        if attribute:
            return True, attribute, value
        else:
            return False, '', ''
    else:
        return False, '', ''


def _parse_mxp_header(it, current, recipe):
    """Parses the MXP header and moves to the next line if found."""
    current = _skip_empty(it, current)
    if _is_mxp_header(current):
        current = next(it)
    return current


def _parse_title(it, current, recipe):
    """Parses the Title line and moves to the next line."""
    current = _skip_empty(it, current)
    recipe.title = current.strip()
    current = next(it)
    return current


def _parse_recipe_by(it, current, recipe):
    """Parses the Recipe By line and moves to the next line if found."""
    current = _skip_empty(it, current)
    is_metadata, attribute, value = _test_metadata(current)
    if is_metadata and attribute.lower() == 'recipe by':
        recipe.recipe_by = value
        current = next(it)
    return current


def _parse_serving_size_preparation_time(it, current, recipe):
    """Parses the Serving Size/Preparation Time line and moves to the next
    line if found."""
    current = _skip_empty(it, current)
    is_match, serving_size, preparation_time = _test_serving_size_preparation_time(current)
    if is_match:
        recipe.serving_size = serving_size
        recipe.preparation_time = preparation_time
        current = next(it)
    return current


# Any number of spaces followed by 'Serving Size'
# Then any number of spaces followed by ':'
# Then any number of spaces followed by an optional number
# Then any number of spaces followed by 'Preparation Time'
# Then any number of spaces followed by ':'
# Then any number of spaces followed by optional text
_sspt_re = re.compile(r'^ *Serving Size *: *(\d*) *Preparation Time *: *(.*)')


def _test_serving_size_preparation_time(line):
    """Returns a tuple indicating whether the line contained serving size
    and preparation time values and the serving size and preparation time."""
    match = _sspt_re.match(line.rstrip())
    if match:
        return True, match.group(1), match.group(2)
    else:
        return False, '', ''


def _parse_categories(it, current, recipe):
    """Parses the categories section and moves to the next line if found."""
    current = _skip_empty(it, current)
    is_categories, category1, category2 = _test_categories(current)
    while is_categories:
        if category1:
            recipe.categories.append(category1)
        if category2:
            recipe.categories.append(category2)
        current = next(it)
        is_categories, category1, category2 = _test_categories(current)
    return current


def _test_categories(line):
    """Returns a tuple indicating whether the line contained categories, the
    value of category 1, and the value of category 2."""
    if line.lower().startswith('categories    : '):
        category1 = line[16:48].strip()
        category2 = line[48:].strip()
        return True, category1, category2
    elif line.startswith('                '):
        category1 = line[16:48].strip()
        category2 = line[48:].strip()
        if category1:
            return True, category1, category2
        else:
            return False, '', ''
    else:
        return False, '', ''


def _parse_ingredients(it, current, recipe):
    """Skips over ingredient heading lines and parses valid ingredient lines and 
    advances to the first line that is not a valid ingredient line.
    """
    ingredients = []
    try:
        current = _skip_empty(it, current)
        if _is_ingredient_heading_1(current):
            current = next(it)
        if _is_ingredient_heading_2(current):
            current = next(it)
        ingredient = _test_ingredient(current)
        while ingredient:
            ingredients.append(ingredient)
            current = next(it)
            ingredient = _test_ingredient(current)
    finally:
        # Add the ingredients even if we reach end of iterable
        # and StopIteration is raised.
        recipe.ingredients = ingredients
    return current


def _is_ingredient_heading_1(line):
    """Returns True for the first heading line of ingredients section."""
    return line.strip().lower() == 'amount  measure       ingredient -- preparation method'


def _is_ingredient_heading_2(line):
    """Returns True for the second heading line of ingredients section."""
    return line.strip() == '--------  ------------  --------------------------------'


# Amount, measure, and ingredient fields separated by 2 spaces
_ingredient_re = re.compile(r'^  ([\d\./ ]{6})  (.{12})  (.*)')


def _test_ingredient(line):
    """Tests whether a line is an ingredient. Returns an Ingredient object or None."""
    match = _ingredient_re.match(line)
    if match:
        amount = match.group(1).strip()
        measure = match.group(2).strip()
        ingredient = match.group(3).strip()
        preparation_method = ''
        index = ingredient.find(' -- ')
        if index >= 0:
            ingredient, preparation_method = ingredient[:index], ingredient[index+4:]
        return Ingredient(amount, measure, ingredient, preparation_method)
    else:
        return None


def _parse_directions(it, current, recipe):
    """Parse directions section by adding lines until we reach the footer."""
    directions = []
    try:
        while not _is_mxp_footer(current):
            if not _is_empty(current):
                directions.append(current.strip())
            current = next(it)
    finally:
        # Add the directions even if we reach end of iterable
        # and StopIteration is raised.
        recipe.directions = directions
    return current


def _parse_notes(it, current, recipe):
    """Parse notes by skipping the footer and adding lines until the end of the recipe."""
    notes = []
    try:
        current = next(it) # skip mxp footer
        while True:
            if not _is_empty(current):
                notes.append(current.strip())
            current = next(it)
    finally:
        # Add the notes when we reach end of iterable
        # and StopIteration is raised.
        recipe.notes = notes
    return current