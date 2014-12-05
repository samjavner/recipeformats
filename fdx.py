import xml.etree.ElementTree as ET


class Recipe:

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
        self.recipe_image = ''
        self.source_image = ''
        self.ingredients = []
        self.procedures = []
        self.author_notes = []
        self.tips = []
        self.reviews = []
        self.measures = []
        self.images = []
        self.user_data = [''] * 15
        self.nutrition = {}


class Ingredient:

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
        self.measure_quantity = ''
        self.measure_gram_weight = ''
        self.recipe_id = ''
        self.recipe_name = ''


class Procedure:

    def __init__(self):
        self.procedure_text = ''
        self.heading = ''
        self.procedure_image = ''


class Tip:

    def __init__(self):
        self.text = ''
        self.heading = ''


class Tip:

    def __init__(self):
        self.text = ''
        self.heading = ''


class Review:

    def __init__(self):
        self.review_date = ''
        self.rating = ''
        self.reviewer = ''


class Measure:

    def __init__(self):
        self.measure_id = ''
        self.description = ''
        self.gram_weight = ''
        self.measure_type = ''


class Image:

    def __init(self):
        self.value = ''
        self.file_type = ''
        self.description = ''

    def __repr__(self):
        return "{%s} {%s} {%s}" % (self.file_type, self.description, self.value[:50] + '...')


def parse_file(filename):
    fdx = ET.parse(filename).getroot()
    return parse_recipes(fdx)


def parse_recipes(fdx):
    recipes = []
    for r in _find(fdx, 'Recipes').findall('Recipe'):
        recipes.append(parse_recipe(r))
    return recipes


def parse_recipe(r):
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
    recipe.recipe_image = _parse_image(_find(r, 'RecipeImage'))
    recipe.source_image = _parse_image(_find(r, 'SourceImage'))
    recipe.ingredients = _parse_ingredients(r)
    recipe.procedures = _parse_procedures(r)
    recipe.author_notes = _parse_author_notes(r)
    recipe.tips = _parse_tips(r)
    recipe.reviews = _parse_reviews(r)
    recipe.measures = _parse_measures(r)
    recipe.images = _parse_images(r)
    recipe.nutrition = _parse_nutrition(r)
    for i in range(15):
        recipe.user_data[i] = r.get('UserData' + str(i + 1), '')
    return recipe


def _parse_ingredients(r):
    ingredients = []
    for recipe_ingredients in r.findall('RecipeIngredients'):
        for recipe_ingredient in recipe_ingredients.findall('RecipeIngredient'):
            ingredient = _parse_ingredient(recipe_ingredient)
            ingredients.append(ingredient)
    return ingredients


def _parse_ingredient(i):
    ingredient = Ingredient()
    ingredient.quantity = i.get('Quantity', '')
    ingredient.unit = i.get('Unit', '')
    ingredient.ingredient = i.get('Ingredient', '')
    ingredient.heading = i.get('Heading', '')
    ingredient.link_type = i.get('LinkType', '')
    ingredient.ingredient_id = i.get('IngredientID', '')
    ingredient.ingredient_name = i.get('IngredientName', '')
    ingredient.measure_id = i.get('MeasureID', '')
    ingredient.measure = i.get('Measure', '')
    ingredient.measure_quantity = i.get('MeasureQuantity', '')
    ingredient.measure_gram_weight = i.get('MeasureGramWeight', '')
    ingredient.recipe_id = i.get('RecipeID', '')
    ingredient.recipe_name = i.get('RecipeName', '')
    return ingredient


def _parse_procedures(r):
    procedures = []
    for recipe_procedures in r.findall('RecipeProcedures'):
        for recipe_procedure in recipe_procedures.findall('RecipeProcedure'):
            procedure = _parse_procedure(recipe_procedure)
            procedures.append(procedure)
    return procedures


def _parse_procedure(p):
    procedure = Procedure()
    procedure.procedure_text = p.findtext('ProcedureText', '').strip()
    procedure.heading = p.get('Heading', '')
    procedure.procedure_image = _parse_image(_find(p, 'ProcedureImage'))
    return procedure


def _parse_author_notes(r):
    author_notes = []
    for recipe_author_notes in r.findall('RecipeTips'):
        for recipe_author_note in recipe_author_notes.findall('RecipeTip'):
            author_note = _parse_author_note(recipe_author_note)
            author_notes.append(author_note)
    return author_notes


def _parse_author_note(n):
    author_note = Tip()
    author_note.text = n.text.strip()
    author_note.heading = n.get('Heading', '')
    return author_note


def _parse_tips(r):
    tips = []
    for recipe_tips in r.findall('RecipeTips'):
        for recipe_tip in recipe_tips.findall('RecipeTip'):
            tip = _parse_tip(recipe_tip)
            tips.append(tip)
    return tips


def _parse_tip(n):
    tip = Tip()
    tip.text = n.text.strip()
    tip.heading = n.get('Heading', '')
    return tip


def _parse_reviews(r):
    reviews = []
    for recipe_reviews in r.findall('RecipeReviews'):
        for recipe_review in recipe_reviews.findall('RecipeReview'):
            review = _parse_review(recipe_review)
            reviews.append(review)
    return reviews


def _parse_review(r):
    review = Review()
    review.review_date = r.get('ReviewDate', '')
    review.rating = r.get('Rating', '')
    review.reviewer = r.get('Reviewer', '')
    return review


def _parse_measures(r):
    measures = []
    for recipe_measures in r.findall('RecipeMeasures'):
        for recipe_measure in recipe_measures.findall('RecipeMeasure'):
            measure = _parse_measure(recipe_measure)
            measures.append(measure)
    return measures


def _parse_measure(m):
    measure = Measure()
    measure.measure_id = m.get('MeasureID', '')
    measure.description = m.get('Description', '')
    measure.gram_weight = m.get('GramWeight', '')
    measure.measure_type = m.get('MeasureType', '')
    return measure


def _parse_images(r):
    images = []
    for recipe_images in r.findall('RecipeImages'):
        for recipe_image in recipe_images.findall('RecipeImage'):
            image = _parse_image(recipe_image)
            images.append(image)
    return images


def _parse_image(i):
    image = Image()
    if not i.text:
        return None
    image.value = i.text.strip()
    image.file_type = i.get('FileType', '')
    image.description = i.get('Description', '')
    return image


def _parse_nutrition(r):
    return {name: value for name, value in _find(r, 'RecipeNutrition').items()}


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