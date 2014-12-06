"""Recipe parsing for Food Data Exchange (Living Cookbook) format (.fdx) files.

Use parse_file to parse a file.
"""

import xml.etree.ElementTree as ET

__all__ = ['parse_file', 'Recipe', 'RecipeIngredient', 'RecipeProcedure',
           'RecipeAuthorNote', 'RecipeTip', 'RecipeReview', 'RecipeMeasure',
           'RecipeImage']


def parse_file(filename):
    """Parses a .fdx file.

    Args:
        filename: File name of the .fdx file to parse.

    Returns: 
        A list of Recipe objects.
    """
    fdx = ET.parse(filename).getroot()
    return [Recipe.parse(e) for e in fdx.findall('./Recipes/Recipe')]


class Recipe:
    """Represents a recipe in a Food Data Exchange .fdx file.

    Attributes:
        name: Name string.
        id: Id string - can be reference from ingredients of another recipe.
        cookbook_id: Id string of cookbook.
        cookbook_chapter_id: Id string of cookbook chapter.
        servings: Number of servings string (perhaps empty).
        yield_: Yield string (e.g. 24 cupcakes) (perhaps empty).
        oven_temperature_f: Oven temperature in degrees F (perhaps empty).
        oven_temperature_c: Oven temperature in degrees C (perhaps empty).
        preparation_time: Preparation time in minutes as a string (perhaps empty).
        cooking_time: Cooking time in minutes as a string (perhaps empty).
        inactive_time: Inactive time in minutes as a string (perhaps empty).
        ready_in_time: Ready in time in minutes as a string (perhaps empty).
        degree_of_difficulty: Difficulty (1-5) as a string (perhaps empty).
        recipe_types: Recipe types as a comma separated string (perhaps empty).
        author: Author string (perhaps empty).
        source: Source string (perhaps empty).
        source_page_number: Source page number string (perhaps empty).
        web_page: Web page string (perhaps empty).
        copyright: Copyright string (perhaps empty).
        comments: Comments string (perhaps empty).
        color_flag: Color flag string (one of '<None>', 'Red', 'Blue',
            'Yellow', 'Green', 'Orange', or 'Purple').
        create_date: Creation date string ('YYYY-MM-DD' format).
        recipe_image: RecipeImage object for main recipe image or None.
        source_image: RecipeImage object for recipe source or None.
        ingredients: List of RecipeIngredient objects.
        procedures: List of RecipeProcedure objects.
        author_notes: List of RecipeAuthorNote objects.
        tips: List of RecipeTip objects.
        reviews: List of RecipeReview objects.
        measures: List of RecipeMeasure objects.
        images: List of RecipeImage objects.
        user_data: List of custom user data with length 15 (items may be empty).
        nutrition: Dictionary of nutrition values.
            Keys are nutrient strings (e.g. 'VitaminA').
            Values are decimal string in the nutrient's standard units (e.g. '1.25')
    """

    def __init__(self):
        self.name = ''
        self.id = ''
        self.cookbook_id = ''
        self.cookbook_chapter_id = ''
        self.servings = ''
        self.yield_ = ''
        self.oven_temperature_f = ''
        self.oven_temperature_c = ''
        self.preparation_time = ''
        self.cooking_time = ''
        self.inactive_time = ''
        self.ready_in_time = ''
        self.degree_of_difficulty = ''
        self.recipe_types = ''
        self.author = ''
        self.source = ''
        self.source_page_number = ''
        self.web_page = ''
        self.copyright = ''
        self.comments = ''
        self.color_flag = ''
        self.create_date = ''
        self.recipe_image = None
        self.source_image = None
        self.ingredients = []
        self.procedures = []
        self.author_notes = []
        self.tips = []
        self.reviews = []
        self.measures = []
        self.images = []
        self.user_data = [''] * 15
        self.nutrition = {}

    @staticmethod
    def parse(r):
        recipe = Recipe()
        recipe.name = r.get('Name', '')
        recipe.id = r.get('ID', '')
        recipe.cookbook_id = r.get('CookbookID', '')
        recipe.cookbook_chapter_id = r.get('CookbookChapterID', '')
        recipe.servings = r.get('Servings', '')
        recipe.yield_ = r.get('Yield', '')
        recipe.oven_temperature_f = r.get('OvenTemperatureF', '')
        recipe.oven_temperature_c = r.get('OvenTemperatureC', '')
        recipe.preparation_time = r.get('PreparationTime', '')
        recipe.cooking_time = r.get('CookingTime', '')
        recipe.inactive_time = r.get('InactiveTime', '')
        recipe.ready_in_time = r.get('ReadyInTime', '')
        recipe.degree_of_difficulty = r.get('DegreeOfDifficulty', '')
        recipe.recipe_types = r.get('RecipeTypes', '')
        recipe.author = r.get('Author', '')
        recipe.source = r.get('Source', '')
        recipe.source_page_number = r.get('SourcePageNumber', '')
        recipe.web_page = r.get('WebPage', '')
        recipe.copyright = r.get('Copyright', '')
        recipe.comments = r.get('Comments', '')
        recipe.color_flag = r.get('ColorFlag', '')
        recipe.create_date = r.get('CreateDate', '')
        recipe.recipe_image = RecipeImage.find_and_parse(r, 'RecipeImage')
        recipe.source_image = RecipeImage.find_and_parse(r, 'SourceImage')
        recipe.ingredients = [RecipeIngredient.parse(e) for e in r.findall('./RecipeIngredients/RecipeIngredient')]
        recipe.procedure = [RecipeProcedure.parse(e) for e in r.findall('./RecipeProcedures/RecipeProcedure')]
        recipe.author_notes = [RecipeAuthorNote.parse(e) for e in r.findall('./RecipeAuthorNotes/RecipeAuthorNote')]
        recipe.tips = [RecipeTip.parse(e) for e in r.findall('./RecipeTips/RecipeTip')]
        recipe.reviews = [RecipeReview.parse(e) for e in r.findall('./RecipeReviews/RecipeReview')]
        recipe.measures = [RecipeMeasure.parse(e) for e in r.findall('./RecipeMeasures/RecipeMeasure')]
        recipe.images = [RecipeImage.parse(e) for e in r.findall('./RecipeImages/RecipeImages')]
        recipe.nutrition = {name: value for name, value in _find(r, 'RecipeNutrition').items()}
        recipe.user_data = [r.get('UserData' + str(i + 1), '') for i in range(15)]
        return recipe


class RecipeIngredient:
    """Represents an ingredient in a Food Data Exchange .fdx file.

    Attributes:
        quantity: Amount string (perhaps empty) (e.g. '2').
        unit: Unit of measure string (perhaps empty) (e.g. 'cups').
        ingredient: Ingredient part string (e.g. 'milk').
        heading: Heading string ('Y' or 'N').
        link_type: Link type string:
            '', 'Recipe', 'NoLink', 'Ingredient', 'Unlinked', others?
        ingredient_id: ID string of linked ingredient when link_type == 'Ingredient'.
        ingredient_name: Name string of linked ingredient when link_type == 'Ingredient'.
        measure_id: ID string of measure when link_type == 'Ingredient'.
        measure: Quantity string of measure when link_type == 'Ingredient'.
        measure_gram_weight: Equivalent number of grams as a string when link_type == 'Ingredient'.
            Equivalent to the measure given in measure.
        measure_quantity: Number (as a string) to multiply by measure or
            measure_gram_weight to get the total quantity when link_type == 'Ingredient'.
            Number (as a string) of recipe servings when link_type == 'Recipe'.
        recipe_id: ID string of linekd recipe when link_type == 'Recipe'.
        recipe_name: Name string of linked recipe when link_type == 'Recipe'.
    """

    def __init__(self):
        self.quantity = ''
        self.unit = ''
        self.ingredient = ''
        self.heading = ''
        self.link_type = ''
        self.ingredient_id = ''
        self.ingredient_name = ''
        self.measure_id = ''
        self.measure = ''
        self.measure_gram_weight = ''
        self.measure_quantity = ''
        self.recipe_id = ''
        self.recipe_name = ''

    @staticmethod
    def parse(e):
        ingredient = RecipeIngredient()
        ingredient.quantity = e.get('Quantity', '')
        ingredient.unit = e.get('Unit', '')
        ingredient.ingredient = e.get('Ingredient', '')
        ingredient.heading = e.get('Heading', '')
        ingredient.link_type = e.get('LinkType', '')
        ingredient.ingredient_id = e.get('IngredientID', '')
        ingredient.ingredient_name = e.get('IngredientName', '')
        ingredient.measure_id = e.get('MeasureID', '')
        ingredient.measure = e.get('Measure', '')
        ingredient.measure_quantity = e.get('MeasureQuantity', '')
        ingredient.measure_gram_weight = e.get('MeasureGramWeight', '')
        ingredient.recipe_id = e.get('RecipeID', '')
        ingredient.recipe_name = e.get('RecipeName', '')
        return ingredient


class RecipeProcedure:
    """Represents a procedure in a Food Data Exchange .fdx file.

    Attributes:
        procedure_text: Text string.
        heading: Heading string ('Y' or 'N').
        image: Image object or None.
    """

    def __init__(self):
        self.procedure_text = ''
        self.heading = ''
        self.procedure_image = None

    @staticmethod
    def parse(e):
        procedure = RecipeProcedure()
        procedure.procedure_text = e.findtext('ProcedureText', '').strip()
        procedure.heading = e.get('Heading', '')
        procedure.procedure_image = RecipeImage.find_and_parse(e, 'ProcedureImage')
        return procedure


class RecipeAuthorNote:
    """Represents an author note in a Food Data Exchange .fdx file.

    Attributes:
        text: Text string.
        heading: Heading string ('True' or '')
    """

    def __init__(self):
        self.text = ''
        self.heading = ''

    @staticmethod
    def parse(e):
        author_note = RecipeAuthorNote()
        author_note.text = e.text.strip()
        author_note.heading = e.get('Heading', '')
        return author_note


class RecipeTip:
    """Represents a tip in a Food Data Exchange .fdx file.

    Attributes:
        text: Text string.
        heading: Heading string ('True' or '')
    """

    def __init__(self):
        self.text = ''
        self.heading = ''

    @staticmethod
    def parse(e):
        tip = RecipeTip()
        tip.text = e.text.strip()
        tip.heading = e.get('Heading', '')
        return tip


class RecipeReview:
    """Represents a review in a Food Data Exchange .fdx file.

    Attributes:
        review_date: Date string ('YYYY-MM-DD' format).
        rating: Rating (0-5) as a string.
        reviewer: Name of reviewer string.
    """

    def __init__(self):
        self.review_date = ''
        self.rating = ''
        self.reviewer = ''

    @staticmethod
    def parse(e):
        review = RecipeReview()
        review.review_date = e.get('ReviewDate', '')
        review.rating = e.get('Rating', '')
        review.reviewer = e.get('Reviewer', '')
        return review


class RecipeMeasure:
    """Represents a recipe measurement in a Food Data Exchange .fdx file.

    Attributes:
        measure_id: ID string.
        description: Description string (e.g. '1 cup').
        gram_weight: Gram weight string (e.g. '300').
        measure_type: Measure type string:
            'Volume', 'Mass', 'Weight (Mass)', 'Unit', others?
    """

    def __init__(self):
        self.measure_id = ''
        self.description = ''
        self.gram_weight = ''
        self.measure_type = ''

    @staticmethod
    def parse(e):
        measure = RecipeMeasure()
        measure.measure_id = e.get('MeasureID', '')
        measure.description = e.get('Description', '')
        measure.gram_weight = e.get('GramWeight', '')
        measure.measure_type = e.get('MeasureType', '')
        return measure


class RecipeImage:
    """Represents an image in a Food Data Exchange .fdx file.

    Attributes:
        value: Bytes of image file encoded as a base 64 string.
        file_type: Extension of image file name (e.g. 'JPG', 'GIF').
        description: Description string for image.
            (only used for Recipe.images; not recipe_image, source_image, or procedure_image)
    """

    def __init(self):
        self.value = ''
        self.file_type = ''
        self.description = ''

    def __repr__(self):
        return "{%s} {%s} {%s}" % (self.file_type, self.description, self.value[:50] + '...')

    @staticmethod
    def find_and_parse(element, tag):
        image = element.find(tag)
        if image is None:
            return None
        else:
            return RecipeImage.parse(image)

    @staticmethod
    def parse(e):
        image = RecipeImage()
        image.value = e.text.strip()
        image.file_type = e.get('FileType', '')
        image.description = e.get('Description', '')
        return image


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