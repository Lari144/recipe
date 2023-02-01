from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import nametofont
import sqlite3

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.entry_button = Button(self.master, text = 'Recipe Entry', font = ('Arial', 15), width = 50, height = 2, command = self.new_entry_window)
        self.search_button = Button(self.master, text = 'Recipe Search', font = ('Arial', 15), width = 50, height = 2, command = self.new_search_window)
        self.recipes_button = Button(self.master, text = 'All Recipes', font = ('Arial', 15), width = 50, height = 2, command = self.new_recipes_window)
        
        self.search_button.place(x = 270, y = 450)
        self.entry_button.place(x = 270, y = 360)
        self.recipes_button.place(x = 270, y = 540)
        headline = Label(self.master, text = 'COOKBOOK', font = ('Arial', 40), bg = '#C6AD94', fg = 'white')
        headline.pack(pady=150)
        
    def new_entry_window(self):
        self.master.withdraw()
        self.new_window = Toplevel()
        self.new_window.config(bg = '#E0DFD5')
        self.new_window.geometry('1080x750')
        EntryWindow(self.new_window, self.master)
    
    def new_search_window(self):
        self.master.withdraw()
        self.new_window = Toplevel()
        self.new_window.config(bg = '#E0DFD5')
        self.new_window.geometry('1080x750')
        SearchWindow(self.new_window, self.master)
    
    def new_recipes_window(self):
        self.master.withdraw()
        self.new_window = Toplevel()
        self.new_window.config(bg = '#E0DFD5')
        self.new_window.geometry('1080x750')
        RecipesWindow(self.new_window, self.master)
     
class EntryWindow:
    def __init__(self, master, oldmaster):
        self.master = master
        self.entry_name = Entry(self.master, width = 43, font = ('Arial', 12))
        
        headline = Label(self.master, text = 'Enter your recipe here', font = ('Arial', 20, 'underline'), bg = '#E0DFD5')
        self.quit_button = Button(self.master, text = 'Quit', width = 25, font = ('Arial', 15), command = lambda:self.close_windows(oldmaster))
        headline_ingredients = Label(self.master, text = "Enter your ingredients", font = ('Arial', 15), bg = '#E0DFD5')
        headline_name = Label(self.master, text = "Enter your recipes name", font = ('Arial', 15), bg = '#E0DFD5')
        headline_description = Label(self.master, text = "Enter the description", font = ('Arial', 15), bg = '#E0DFD5')
        self.submit_button = Button(self.master, text = 'Submit', width = 25, font = ('Arial', 15), command=lambda:[RecipeDatabase.store_data(self.entry_name.get(), self.entry_ingredients.get("1.0", 'end-1c'), self.entry_description.get("1.0", 'end-1c'), self.categories.get()), self.refresh()])
        self.entry_ingredients = scrolledtext.ScrolledText(self.master, width = 43, height = 3, font = ('Arial', 12))
        self.entry_description = scrolledtext.ScrolledText(self.master, width = 43, height = 3, font = ('Arial', 12))     
        headline_categories = Label(self.master, text = "Choose the categorie", font = ('Arial', 15), bg = '#E0DFD5')
        list_categories = ['cake', 'bread', 'soup']
        self.categories = ttk.Combobox(self.master, values=list_categories, font = ('Arial', 15), width = 43)
        RecipeDatabase.create_categories(list_categories)

        headline.pack(pady=20)
        headline_name.pack()
        self.entry_name.pack(pady=10)
        headline_ingredients.pack()
        self.entry_ingredients.pack(pady=10)
        headline_description.pack()
        self.entry_description.pack(pady=10)
        headline_categories.pack()
        self.categories.pack(pady=10)
        self.submit_button.pack(pady=20)
        self.quit_button.place(x = 395, y = 650)
    
    def refresh(self):
        self.entry_name.delete(0, 'end')
        self.entry_ingredients.delete('1.0', 'end')
        self.entry_description.delete('1.0', 'end')
        self.categories.delete(0, 'end')

    def close_windows(self, oldmaster):
        oldmaster.deiconify()
        self.master.destroy()
    
    def get_input(self):
        self.entry_name.get()
        self.entry_ingredients.get()
        self.entry_description.get()
        
class SearchWindow:
    def __init__(self, master, oldmaster):
        self.master = master
        self.headline = Label(self.master, text = 'Search for your recipe here', font = ('Arial', 20, 'underline'), bg = '#E0DFD5')
        self.quit_button = Button(self.master, text = 'Quit', width = 25, font = ('Arial', 15), command = lambda:self.close_windows(oldmaster))
        self.search_button = Button(self.master, text='Search', width = 25, font = ('Arial', 15), command=lambda: [RecipeDatabase.name_output(self), RecipeDatabase.ingredients_output(self), RecipeDatabase.search_data(self)])
        self.entry_name = Entry(self.master, width = 43, font = ('Arial', 12))
        
        self.headline.pack(pady = 20)
        self.entry_name.pack()
        self.search_button.pack(pady = 20)
        self.quit_button.place(x = 395, y = 650)

    def close_windows(self, oldmaster):
        oldmaster.deiconify()
        self.master.destroy()

class RecipesWindow():
    def __init__(self, master, oldmaster):
        self.master = master
        self.selected_items = []
        
        list_categories = ['cake', 'bread', 'soup']
        self.filter_option = ttk.Combobox(self.master, values=list_categories, font = ('Arial', 15), width = 10)
        search_button = Button(self.master, text='Search', command=lambda:RecipeDatabase.filter_data(self), width=10, font = ('Arial', 15))
        search_button.place(x = 670, y = 37)
        reset_button = Button(self.master, text='Show all', command=lambda:RecipeDatabase.reset_search(self), width=10, font = ('Arial', 15))
        reset_button.place(x = 130, y = 37)
        self.filter_option.place(x = 805, y = 44)
        edit_button = Button(self.master, text='Edit Recipe', command=lambda:self.edit_item())
        edit_button.place(x = 620,y = 600)
        select_button = Button(self.master, text='Show Recipe', command=lambda:self.select_item())
        select_button.place(x = 310, y = 600)
        delete_button = Button(self.master, text='Delete Recipe', command=lambda:self.delete_item())
        delete_button.place(x = 460, y = 600)
        self.quit_button = Button(self.master, text = 'Quit', width = 25, font = ('Arial', 15), command = lambda:self.close_windows(oldmaster))   
        self.quit_button.place(x = 395, y = 670)
        self.tree = ttk.Treeview(self.master, column=("c1"), show='tree', selectmode="browse")
        RecipeDatabase.recipe_output(self)

    def close_windows(self, oldmaster):
        oldmaster.deiconify()
        self.master.destroy()
        
    def edit_item(self):
        for selected_item in self.tree.selection():
            top = Toplevel(self.master)
            top.geometry('750x500')
            item = self.tree.item(selected_item)

            e0 = Entry(top, width = 30, text = item['values'][0], font = ('Arial', 15))
            e0.insert(0, item['values'][0])
            e1 = scrolledtext.ScrolledText(top, width = 28, height=5, font = ('Arial', 15))
            e1.insert('insert', item['values'][1])
            e2 = scrolledtext.ScrolledText(top, width = 28, height=5, font = ('Arial', 15))
            for item in item['values'][3:]:
                e2.insert('insert', item + '\n')
            commit_button = Button(top, text='Commit Changes', command=lambda: [RecipeDatabase.add(e0.get(), e1.get("1.0",'end-1c')), RecipeDatabase.update_ingredients(e0.get(), e2.get("1.0",'end-1c'))])
            e0.pack()
            e1.pack()
            e2.pack()
            commit_button.pack(pady=10)
    
    def select_item(self):
        for selected_item in self.tree.selection():
            top = Toplevel(self.master)
            top.geometry('750x250')
            item = self.tree.item(selected_item)
            record = item['values']
            for j in range(len(record)):
                e = Label(top, width = 30, text = record[j], font = ('Arial', 15))
                e.pack()

    def delete_item(self):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            RecipeDatabase.delete_item(item['values'][0])
            self.tree.delete(selected_item)

class RecipeDatabase():
    
    def create_categories(categories):
        conn = sqlite3.connect('recipe.db')
        cursor = conn.cursor()
        values = cursor.execute('''SELECT Name FROM Categorie''').fetchall()
        
        if len(values) == 0:
            for c in categories:
                cursor.execute('''INSERT INTO Categorie (Name) VALUES
                (?)''', ([c]))

        conn.commit()
        conn.close()

    def store_data(name, ingredients, description, categories):
        
        if len(name) == 0:
            messagebox.showinfo('Error', 'Fill in the name space')
        elif len(ingredients) == 0:
            messagebox.showinfo('Error', 'Fill in the ingredients space')
        elif len(description) == 0:
            messagebox.showinfo('Error', 'Fill in the description space')
        conn = sqlite3.connect('recipe.db')
        
        table_create_categorie = '''CREATE TABLE IF NOT EXISTS Categorie 
            (ID INTEGER, Name TEXT, PRIMARY KEY("ID"))'''
        table_create_ingredients = '''CREATE TABLE IF NOT EXISTS Ingredients 
            (ID INTEGER, Name TEXT, PRIMARY KEY("ID"))'''
        table_create_table = '''CREATE TABLE IF NOT EXISTS RecipeIngredients 
            (ID INTEGER, Recipe_ID INTEGER, Ingredients_ID INTEGER, PRIMARY KEY("ID"),
            CONSTRAINT "FK_Recipe" FOREIGN KEY("Recipe_ID") REFERENCES "Recipe"("ID"),
            CONSTRAINT "FK_Ingredients" FOREIGN KEY("Ingredients_ID") REFERENCES "Ingredients"("ID"))'''

        table_create_query = '''CREATE TABLE IF NOT EXISTS Recipe 
                    (ID INTEGER, Name TEXT NOT NULL, Description TEXT NOT NULL, Categorie_ID INTEGER,
                    PRIMARY KEY("ID"),
	                CONSTRAINT "FK_Categorie" FOREIGN KEY("Categorie_ID") REFERENCES "Categorie"("ID"))'''
        
        conn.execute(table_create_categorie)
        conn.execute(table_create_ingredients)
        conn.execute(table_create_query)
        conn.execute(table_create_table)
        
        cursor = conn.cursor()
        categorie_id = cursor.execute('''SELECT ID FROM Categorie WHERE Name LIKE ?''', ([categories])).fetchall()[0][0]
        cursor.execute('''INSERT INTO Recipe (Name, Description, Categorie_ID) VALUES (?, ?, ?)''',
                        (name, description, str(categorie_id)))
        
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
        conn.close()
    
    def filter_data(self):
        categories = self.filter_option.get()
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect('recipe.db')
        conn_ = conn.cursor()
        
        id = conn_.execute('''SELECT ID FROM Categorie WHERE Name LIKE ?''', ([categories])).fetchall()[0][0]
        search = conn_.execute('''SELECT r.Name, i.Name as Ingredients_name, r.Description, c.Name as Categorie_name
                            FROM Recipe r 
                            JOIN Categorie c ON r.ID = c.ID 
                            JOIN Ingredients i ON r.ID = i.ID
                            WHERE Categorie_ID LIKE ? LIMIT 2''', (str(id)))

        for recipe in search:
            self.tree.insert('', 'end', values=recipe)

        conn.commit()
        conn.close()
    
    def reset_search(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect('recipe.db')
        conn_ = conn.cursor()
        
        conn_.execute('''SELECT r.Name, i.Name as Ingredients_name, r.Description, c.Name as Categorie_name
                        FROM Recipe r 
                        JOIN Categorie c ON r.ID = c.ID 
                        JOIN Ingredients i ON r.ID = i.ID''')

        for recipe in conn_:
            self.tree.insert('', 'end', values=recipe)

        conn.commit()
        conn.close()
    
    def search_data(self):
        conn = sqlite3.connect('recipe.db')
        conn_ = conn.cursor()
        conn_.execute('''SELECT r.Description, c.Name as Categorie_name
                        FROM Recipe r 
                        JOIN Categorie c ON r.ID = c.ID 
                        JOIN Ingredients i ON r.ID = i.ID
                        WHERE r.Name LIKE ?''', ('%' + str(self.entry_name.get()),))
        i = 0
        for recipe in conn_:
            for j in range(len(recipe)):
                e = Label(self.master, width = 30, text = recipe[j], font = ('Arial', 15))
                e.pack(pady = i + 5, padx = j)
            i = i + 1
            
    def ingredients_output(self):
        conn = sqlite3.connect('recipe.db')
        conn_ = conn.cursor()
        conn_.execute('''SELECT i.Name
                        FROM RecipeIngredients x
                        JOIN Recipe r ON x.Recipe_ID = r.ID
                        JOIN Ingredients i ON x.Ingredients_ID = i.ID
                        WHERE r.Name LIKE ?''', ('%' + str(self.entry_name.get()),))
        i = 0
        for recipe in conn_:
            for j in range(len(recipe)):
                e = Label(self.master, width = 30, text = recipe[j], font = ('Arial', 15))
                e.pack(pady = i + 5, padx = j)
            i = i + 1
    
    def name_output(self):
        conn = sqlite3.connect('recipe.db')
        conn_ = conn.cursor()
        conn_.execute('SELECT Name FROM Recipe WHERE Name LIKE ?', ('%' + str(self.entry_name.get()),))
        i = 0
        for recipe in conn_:
            for j in range(len(recipe)):
                e = Label(self.master, width = 30, text = recipe[j], font = ('Arial', 20, 'underline'), bg = '#E0DFD5')
                e.pack(pady = 20)
            i = i + 1

    def recipe_output(self):
        conn = sqlite3.connect('recipe.db')
        conn_ = conn.cursor()
        
        recipe_ = conn_.execute('''SELECT r.ID, r.Name, r.Description, c.Name as Categorie_name
                        FROM Recipe r 
                        JOIN Categorie c ON r.ID = c.ID 
                        JOIN Ingredients i ON r.ID = i.ID''').fetchall()

        style= ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', rowheight = 40)
        
        self.tree = ttk.Treeview(self.master, column=("c1"), show='headings', selectmode="browse")
        self.tree.column("#1", anchor=CENTER, width=800)
        self.tree.heading("#1", text="Recipes")
        nametofont('TkHeadingFont').configure(size=20)
        nametofont('TkDefaultFont').configure(size=16)
        treeScroll = ttk.Scrollbar(self.master)
        treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeScroll.set)
        treeScroll.pack(side= RIGHT, fill = BOTH)
        self.tree.pack(pady=100)

        for recipe in recipe_:
            ingredients_ = conn_.execute('''SELECT i.Name
                            FROM Ingredients i
                            JOIN RecipeIngredients x ON i.ID = x.ID
                            JOIN Recipe r ON x.Recipe_ID = r.ID
                            WHERE r.ID = ?''', (str(recipe[0]),)).fetchall()

            recipe_ingredients = ()
            for ingredient in ingredients_:
                recipe_ingredients += ingredient

            display_recipe = recipe[1:] + recipe_ingredients
            self.tree.insert('', 'end', values=display_recipe)

    def delete_item(name):
        conn = sqlite3.connect("recipe.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Recipe WHERE Name LIKE ?", ('%' + name,))
        conn.commit()
        conn.close()
    
    def add(name, description):
        conn = sqlite3.connect("recipe.db")
        cursor = conn.cursor()
        cursor.execute('''UPDATE Recipe SET Name=?, Description=? WHERE Name LIKE ?''', (name, description, name))
        conn.commit()
        conn.close()
    
    def update_ingredients(name, ingredients):
        conn = sqlite3.connect("recipe.db")
        cursor = conn.cursor()
        recipe_id = cursor.execute('''SELECT ID FROM Recipe WHERE Name LIKE ?''', (name,)).fetchall()[0][0]
        lines = ingredients.splitlines()
        
        for line in lines:
            cursor.execute("INSERT INTO Ingredients (Name) VALUES (?)", (line,))
            ingredients_id = cursor.execute('''SELECT ID FROM Ingredients WHERE Name LIKE ?''', (line,)).fetchall()[0][0]
            cursor.execute('''INSERT INTO RecipeIngredients (Recipe_ID, Ingredients_ID) VALUES (?, ?)''',
                            (str(recipe_id), str(ingredients_id)))
        conn.commit()
        conn.close()
        
def main(): 
    root = Tk(className="Cookbook")
    root.configure(bg = '#C6AD94')
    root.geometry('1080x750')
    MainWindow(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()