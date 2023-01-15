from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import sqlite3

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.entry_button = Button(self.master, text = 'Recipe Entry', font = ('Arial', 15), width = 50, height = 2, command = self.new_entry_window)
        self.search_button = Button(self.master, text = 'Recipe Search', font = ('Arial', 15), width = 50, height = 2, command = self.new_search_window)
        self.search_button.place(x = 270, y = 450)
        self.entry_button.place(x = 270, y = 360)
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
        self.new_window.geometry('1080x750')
        SearchWindow(self.new_window, self.master)
       
class EntryWindow:
    def __init__(self, master, oldmaster):
        self.master = master
        headline = Label(self.master, text = 'Enter your recipe here', font = ('Arial', 20, 'underline'), bg = '#E0DFD5')
        self.quit_button = Button(self.master, text = 'Quit', width = 25, font = ('Arial', 15), command = lambda:self.close_windows(oldmaster))
        headline_ingredients = Label(self.master, text = "Enter your ingredients", font = ('Arial', 15), bg = '#E0DFD5')
        headline_name = Label(self.master, text = "Enter your recipes name", font = ('Arial', 15), bg = '#E0DFD5')
        headline_description = Label(self.master, text = "Enter the description", font = ('Arial', 15), bg = '#E0DFD5')
        self.submit_button = Button(self.master, text = 'Submit', width = 25, font = ('Arial', 15), command=lambda:RecipeDatabase.store_data(self))
        self.entry_name = Entry(self.master, width = 43, font = ('Arial', 12))
        self.entry_ingredients = scrolledtext.ScrolledText(self.master, width = 43, height = 3, font = ('Arial', 12))
        self.entry_description = scrolledtext.ScrolledText(self.master, width = 43, height = 3, font = ('Arial', 12))
        
        headline.pack(pady=20)
        headline_name.pack()
        self.entry_name.pack(pady=10)
        headline_ingredients.pack()
        self.entry_ingredients.pack(pady=10)
        headline_description.pack()
        self.entry_description.pack(pady=10)
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
        self.headline = Label(self.master, text = 'Search for your recipe here')
        self.quit_button = Button(self.master, text = 'Quit', width = 25, command = lambda:self.close_windows(oldmaster))
        self.search_button = Button(self.master, text='Submit', command=lambda:RecipeDatabase.search_data(self))
        self.entry_name = Entry(self.master)
        
        self.headline.pack()
        self.entry_name.pack()
        self.search_button.pack()
        self.quit_button.pack()

    def close_windows(self, oldmaster):
        oldmaster.deiconify()
        self.master.destroy()

class RecipeDatabase(EntryWindow):
    
    def __init__(self, master, oldmaster):
        super().__init__(master, oldmaster)
        
    def store_data(self):
        name = self.entry_name.get()
        ingredients = self.entry_ingredients.get("1.0", END)
        description = self.entry_description.get("1.0", END)
        
        if len(name) == 0:
            messagebox.showinfo('Error', 'Fill in the name space')
        elif len(ingredients) == 0:
            messagebox.showinfo('Error', 'Fill in the ingredients space')
        elif len(description) == 0:
            messagebox.showinfo('Error', 'Fill in the description space')
        
        conn = sqlite3.connect('recipe.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Recipe_Data 
                    (Name TEXT NOT NULL, Ingredients TEXT NOT NULL, Description TEXT NOT NULL)'''
        conn.execute(table_create_query)
        
        data_insert_query = '''INSERT INTO Recipe_Data (Name, Ingredients, Description) VALUES
        (?, ?, ?)'''
        data_insert_tuple = (name, ingredients, description)
        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()
    
    def search_data(self):
        conn = sqlite3.connect('recipe.db')
        conn_ = conn.cursor()
        conn_.execute('SELECT * FROM Recipe_Data WHERE Name LIKE ?', ('%' + str(self.entry_name.get()),))
        
        i = 0
        for recipe in conn_:
            if recipe == None:
                pass
            for j in range(len(recipe)):
                e = Label(self.master, width = 10, text = recipe[j])
                e.pack(pady = i, padx = j)
            i = i + 1

def main(): 
    root = Tk(className="Cookbook")
    root.configure(bg = '#C6AD94')
    root.geometry('1080x750')
    MainWindow(root)
    root.mainloop()

main()