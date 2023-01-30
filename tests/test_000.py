import logging
import sqlite3
import pytest
from tkinter import *

try:
    import recipe
except ModuleNotFoundError as e:
    logging.error("Module not found %s", e)


def test_000_insert():
    from recipe import EntryWindow
    x = EntryWindow(master=None, oldmaster=None)
    name = x.entry_name
    ingredients = x.entry_ingredients
    description = x.entry_description
    
    conn = sqlite3.connect('recipe.db')
    sql_insert = ('''INSERT INTO Recipe (Name, Ingredients, Description, Categorie_ID) VALUES (?, ?, ?, ?)''')
    conn_ = conn.cursor()
    
    try:
        affected_count = conn_.execute(sql_insert, (name, ingredients, description ))
        conn.commit()
        logging.warn("%d", affected_count)
        logging.info("inserted values %s, %s, %s", name, ingredients, description)
    except:
        logging.warn("failed to insert values %s, %s, %s", name, ingredients, description)
    finally:
        conn_.close()

def test_001_select():
    conn = sqlite3.connect('recipe.db')
    conn_ = conn.cursor()    
    result = conn_.execute('''SELECT Name, Ingredients, Description FROM Recipe''')
    
    assert len(result.fetchall()) > 0
