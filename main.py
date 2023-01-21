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
        self.submit_button = Button(self.master, text = 'Submit', width = 25, font = ('Arial', 15), command=lambda:RecipeDatabase.store_data(self))
        self.entry_ingredients = scrolledtext.ScrolledText(self.master, width = 43, height = 3, font = ('Arial', 12))
        self.entry_description = scrolledtext.ScrolledText(self.master, width = 43, height = 3, font = ('Arial', 12))     
        headline_categories = Label(self.master, text = "Choose the categorie", font = ('Arial', 15), bg = '#E0DFD5')
        self.categories = ttk.Combobox(self.master, values=['','cake', 'bread', 'soup'], font = ('Arial', 15), width = 43)        
        
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
        self.search_button = Button(self.master, text='Search', width = 25, font = ('Arial', 15), command=lambda: [RecipeDatabase.name_output(self), RecipeDatabase.search_data(self)])
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
        select_button = Button(self.master, text='Show Recipe', command=lambda:self.select_item())
        select_button.place(x = 395, y = 600)
        delete_button = Button(self.master, text='Delete Recipe', command=lambda:self.delete_item())
        delete_button.place(x = 534, y = 600)
        self.quit_button = Button(self.master, text = 'Quit', width = 25, font = ('Arial', 15), command = lambda:self.close_windows(oldmaster))   
        self.quit_button.place(x = 395, y = 670)
        self.tree = ttk.Treeview(self.master, column=("c1"), show='tree', selectmode="browse")

        RecipeDatabase.recipe_output(self)

    def close_windows(self, oldmaster):
        oldmaster.deiconify()
        self.master.destroy()
    
    def edit_item(self):
        selected_item = self.tree.focus()
        self.tree.item(selected_item)
    
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
            print(item)
            RecipeDatabase.delete_item(item['values'][0])
            self.tree.delete(selected_item)
            return

class RecipeDatabase():
        
    def store_data(self):
        name = self.entry_name.get()
        ingredients = self.entry_ingredients.get("1.0", END)
        description = self.entry_description.get("1.0", END)
        categories = self.categories.get()

        if len(name) == 0:
            messagebox.showinfo('Error', 'Fill in the name space')
        elif len(ingredients) == 0:
            messagebox.showinfo('Error', 'Fill in the ingredients space')
        elif len(description) == 0:
            messagebox.showinfo('Error', 'Fill in the description space')
        
        conn = sqlite3.connect('recipe.db')
        
        table_create_categorie = '''CREATE TABLE IF NOT EXISTS Categorie 
            (ID INTEGER, Name TEXT, PRIMARY KEY("ID"))'''

        table_create_query = '''CREATE TABLE IF NOT EXISTS Recipe 
                    (ID INTEGER, Name TEXT NOT NULL, Ingredients TEXT NOT NULL, Description TEXT NOT NULL, Categorie_ID INTEGER,
                    PRIMARY KEY("ID"),
	                CONSTRAINT "FK_Categorie" FOREIGN KEY("Categorie_ID") REFERENCES "Categorie"("ID"))'''
        
        conn.execute(table_create_categorie)
        conn.execute(table_create_query)
        
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO Categorie (Name) VALUES
        (?)''', [categories])
        categorie_id = cursor.lastrowid
        
        
        cursor.execute('''INSERT INTO Recipe (Name, Ingredients, Description, Categorie_ID) VALUES (?, ?, ?, ?)''',
                       (name, ingredients, description, categorie_id))
        
        conn.commit()
        conn.close()
    
    def search_data(self):
        conn = sqlite3.connect('recipe.db')
        conn_ = conn.cursor()
        conn_.execute('SELECT Ingredients, Description FROM Recipe WHERE Name LIKE ?', ('%' + str(self.entry_name.get()),))
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
        conn_.execute('SELECT Name, Ingredients, Description FROM Recipe')
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

        for recipe in conn_:
            self.tree.insert('', 'end', values=recipe)

    def delete_item(name):
        conn = sqlite3.connect("recipe.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Recipe WHERE Name LIKE ?", ('%' + name,))
        conn.commit()
        conn.close()

def main(): 
    root = Tk(className="Cookbook")
    root.configure(bg = '#C6AD94')
    root.geometry('1080x750')
    MainWindow(root)
    root.mainloop()

main()