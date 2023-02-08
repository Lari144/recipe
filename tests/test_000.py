import logging
import sqlite3
import pytest
from tkinter import *

try:
    import recipe
except ModuleNotFoundError as e:
    logging.error("Module not found %s", e)


@pytest.fixture
def entry_name():
    class Entry:
        def __init__(self, name, ingredients, description, category, time):
            self.entry_name = name
            self.entry_ingredients = ingredients
            self.entry_description = description
            self.entry_category = category
            self.entry_time = time
    return Entry('Name', 'Ingredient', 'Description', 'Test Category', 'Test Time')

@pytest.fixture
def setup_database(entry_name):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    name = entry_name.entry_name
    ingredients = entry_name.entry_ingredients
    description = entry_name.entry_description
    categories = entry_name.entry_category
    time = entry_name.entry_time
    
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

    time_id = cursor.execute('''INSERT INTO Time (Name) VALUES (?)''', (time,))
    categorie_id = cursor.execute('''INSERT INTO Categorie (Name) VALUES (?)''', (categories,))
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
    categories = [('Test Category')]
    
    conn = setup_database
    cursor = conn.cursor()
    result = cursor.execute('''SELECT Name FROM Categorie''').fetchall()
    
    result = [r[0] for r in result]

    assert result == categories

def test_create_time(setup_database):
    categories = [('Test Time')]
    
    conn = setup_database
    cursor = conn.cursor()
    result = cursor.execute('''SELECT Name FROM Time''').fetchall()
    
    result = [r[0] for r in result]

    assert result == categories
    
def test_create_recipe(setup_database):
    recipe = [('Name', 'Description')]
    
    conn = setup_database
    cursor = conn.cursor()
    result = cursor.execute('''SELECT Name, Description FROM Recipe''').fetchall()
    
    result = [r for r in result]

    assert result == recipe

def test_create_ingredients(setup_database):
    ingredients = [('Ingredient')]
    
    conn = setup_database
    cursor = conn.cursor()
    result = cursor.execute('''SELECT Name FROM Ingredients''').fetchall()
    
    result = [r[0] for r in result]

    assert result == ingredients

def test_create_recipe_ingredients(setup_database):
    ingredients = [(1, 1,)]
    
    conn = setup_database
    cursor = conn.cursor()
    result = cursor.execute('''SELECT Recipe_ID, Ingredients_ID FROM RecipeIngredients''').fetchall()
    
    result = [r for r in result]

    assert result == ingredients

def test_search_name(entry_name, setup_database):
    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    name = 'Name'
    entry_name = entry_name.entry_name
    
    name_ = x.name_output(entry_name).fetchall()[0][0]

    assert str(name_) == name

def test_ingredients_search(entry_name, setup_database):
    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    result = 'Ingredient'
    entry_name = entry_name.entry_name
    
    name_ = x.ingredients_output(entry_name).fetchall()[0][0]

    assert str(name_) == result

def test_delete_item(entry_name, setup_database):
    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    entry_name = entry_name.entry_name
    
    name_ = x.delete_item(entry_name)

    assert str(name_) == str([])

def test_update(entry_name, setup_database):
    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    name = entry_name.entry_name
    desc = 'new description'
    ing = 'new ingredient'
    
    before = (entry_name.entry_description, entry_name.entry_ingredients)
    result = x.update_item(name, ing, desc)
    assert not (before == result)

def test_recipe_output(entry_name, setup_database):
    recipe.RecipeDatabase.conn = setup_database
    x = recipe.RecipeDatabase
    name = entry_name.entry_name
    desc = entry_name.entry_description
    ing = entry_name.entry_ingredients
    
    result_expect = [(name, desc, ing)]
    result = x.recipe_output()
    assert result_expect == result
    
def test_connection(setup_database):
    conn = setup_database
    if conn:
        conn.cursor()
    else:
        raise Exception("Failed to connect to the database")