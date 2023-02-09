import logging
import sqlite3
import pytest
from tkinter import *

try:
    import recipe
except ModuleNotFoundError as e:
    logging.error("Module not found %s", e)


@pytest.fixture
def entry():
    class Entry:
        def __init__(self, name, ingredients, description, category, time):
            self.entry_name = name
            self.entry_ingredients = ingredients
            self.entry_description = description
            self.entry_category = category
            self.entry_time = time
    return Entry('Name', 'Ingredient', 'Description', 'Test Category', 'Test Time')

@pytest.fixture
def setup_database(entry):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    name = entry.entry_name
    ingredients = entry.entry_ingredients
    description = entry.entry_description
    categories = entry.entry_category
    time = entry.entry_time
    
    table_create_times = '''CREATE TABLE Time
            (ID INTEGER, Name TEXT, PRIMARY KEY("ID"))'''
    table_create_categorie = '''CREATE TABLE Categorie 
        (ID INTEGER, Name TEXT, PRIMARY KEY("ID"))'''
    table_create_ingredients = '''CREATE TABLE Ingredients 
        (ID INTEGER, Name TEXT, PRIMARY KEY("ID"))'''
    table_create_table = '''CREATE TABLE RecipeIngredients 
        (ID INTEGER, Recipe_ID INTEGER, Ingredients_ID INTEGER, PRIMARY KEY("ID"),
        CONSTRAINT "FK_Recipe" FOREIGN KEY("Recipe_ID") REFERENCES "Recipe"("ID"),
        CONSTRAINT "FK_Ingredients" FOREIGN KEY("Ingredients_ID") REFERENCES "Ingredients"("ID"))'''

    table_create_query = '''CREATE TABLE Recipe 
                (ID INTEGER, Name TEXT NOT NULL, Description TEXT NOT NULL, Categorie_ID INTEGER, Time_ID INTEGER,
                PRIMARY KEY("ID"),
                CONSTRAINT "FK_Categorie" FOREIGN KEY("Categorie_ID") REFERENCES "Categorie"("ID")
                CONSTRAINT "FK_Time" FOREIGN KEY("Time_ID") REFERENCES "Time"("ID"))'''

    conn.execute(table_create_times)
    conn.execute(table_create_categorie)
    conn.execute(table_create_ingredients)
    conn.execute(table_create_table)
    conn.execute(table_create_query)

    cursor.execute('''INSERT INTO Time (Name) VALUES (?)''', (time,))
    time_id = cursor.execute('''SELECT ID FROM Time WHERE Name LIKE 'Test Time' ''').fetchall()[0][0]
    cursor.execute('''INSERT INTO Categorie (Name) VALUES (?)''', (categories,))
    categorie_id = cursor.execute('''SELECT ID FROM Categorie WHERE Name LIKE 'Test Category' ''').fetchall()[0][0]
    cursor.execute('''INSERT INTO Recipe (Name, Description, Categorie_ID, Time_ID) VALUES (?, ?, ?, ?)''',
                    (name, description, str(categorie_id), str(time_id)))
    recipe_id = cursor.execute('''SELECT ID FROM Recipe WHERE Name LIKE ?''', (name,)).fetchall()[0][0]
    lines = ingredients.splitlines()

    for line in lines:
        values = cursor.execute('''SELECT Name FROM Ingredients WHERE Name LIKE ?''', (line,)).fetchall()
        if len(values) == 0:
            cursor.execute("INSERT INTO Ingredients (Name) VALUES (?)", (line,))
        ingredients_id = cursor.execute('''SELECT ID FROM Ingredients WHERE Name LIKE ?''', (line,)).fetchall()[0][0]
        cursor.execute('''INSERT INTO RecipeIngredients (Recipe_ID, Ingredients_ID) VALUES (?, ?)''',
                        (str(recipe_id), str(ingredients_id)))
    conn.commit()
    yield conn

def test_create_categories(setup_database):
    '''Method for testing if category was inserted correctly'''
    
    categories = [('Test Category')]
    
    conn = setup_database
    cursor = conn.cursor()
    result = cursor.execute('''SELECT Name FROM Categorie''').fetchall()
    
    result = [r[0] for r in result]

    assert result == categories

def test_create_time(setup_database):
    '''Method for testing if time was inserted correctly'''
    
    categories = [('Test Time')]
    
    conn = setup_database
    cursor = conn.cursor()
    result = cursor.execute('''SELECT Name FROM Time''').fetchall()
    
    result = [r[0] for r in result]

    assert result == categories
    
def test_create_recipe(setup_database):
    '''Method for testing if recipe was inserted correctly'''
    
    recipe = [('Name', 'Description')]
    
    conn = setup_database
    cursor = conn.cursor()
    result = cursor.execute('''SELECT Name, Description FROM Recipe''').fetchall()
    
    result = [r for r in result]

    assert result == recipe

def test_create_ingredients(setup_database):
    '''Method for testing if ingredient was inserted correctly'''
    
    ingredients = [('Ingredient')]
    
    conn = setup_database
    cursor = conn.cursor()
    result = cursor.execute('''SELECT Name FROM Ingredients''').fetchall()
    
    result = [r[0] for r in result]

    assert result == ingredients

def test_create_recipe_ingredients(setup_database):
    '''Method for testing if ingredient was inserted correctly'''
    
    ingredients = [(1, 1,)]
    
    conn = setup_database
    cursor = conn.cursor()
    result = cursor.execute('''SELECT Recipe_ID, Ingredients_ID FROM RecipeIngredients''').fetchall()
    
    result = [r for r in result]

    assert result == ingredients

def test_search_name(entry, setup_database):
    '''Method for testing if name_output is searching correctly'''
    
    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    name = 'Name'
    entry_name = entry.entry_name
    
    name_ = x.name_output(entry_name).fetchall()[0][0]

    assert str(name_) == name

def test_ingredients_search(entry, setup_database):
    '''Method for testing if ingredient_output is searching correctly'''
    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    result = 'Ingredient'
    entry_name = entry.entry_name
    
    name_ = x.ingredients_output(entry_name).fetchall()[0][0]

    assert str(name_) == result

def test_delete_item(entry, setup_database):
    '''Method for testing if deleting is done correctly'''

    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    entry_name = entry.entry_name
    
    name_ = x.delete_item(entry_name)

    assert str(name_) == str([])

def test_update(entry, setup_database):
    '''Method for testing if update is done correctly'''

    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    name = entry.entry_name
    desc = 'new description'
    ing = 'new ingredient'
    
    before = (entry.entry_description, entry.entry_ingredients)
    result = x.update_item(name, ing, desc)
    assert not (before == result)

def test_recipe_output(entry, setup_database):
    '''Method for testing if recipe_output is searching correctly'''

    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    name = entry.entry_name
    desc = entry.entry_description
    ing = entry.entry_ingredients
    
    result_expect = [(name, desc, ing)]
    result = x.recipe_output()
    assert result_expect == result

def test_filter_data(entry, setup_database):
    '''Method for testing if filter_data is done correctly'''

    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    
    name = entry.entry_name
    desc = entry.entry_description
    cat = entry.entry_category
    ing = entry.entry_ingredients
    
    result_expect = [(name, desc, cat, ing)]
    result = x.filter_data(cat)
    assert result_expect == result

def test_filter_time(entry, setup_database):
    '''Method for testing if filter_time is done correctly'''

    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    
    name = entry.entry_name
    desc = entry.entry_description
    cat = entry.entry_category
    ing = entry.entry_ingredients
    time = entry.entry_time
    
    result_expect = [(name, desc, cat, ing)]
    result = x.filter_time(time)
    assert result_expect == result
    
def test_connection(setup_database):
    '''Method for testing if connection to database is working'''

    conn = setup_database
    if conn:
        conn.cursor()
    else:
        raise Exception("Failed to connect to the database")