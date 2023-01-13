from tkinter import *

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.entry_button = Button(self.master, text = 'Recipe Entry', width = 25, command = self.new_entry_window)
        self.search_button = Button(self.master, text = 'Recipe Search', width = 25, command = self.new_search_window)
        self.entry_button.pack()
        self.search_button.pack()

    def new_entry_window(self):
        self.master.withdraw()
        self.new_window = Toplevel()
        self.new_window.geometry('700x350')
        EntryWindow(self.new_window, self.master)
    
    def new_search_window(self):
        self.master.withdraw()
        self.new_window = Toplevel()
        self.new_window.geometry('700x350')
        SearchWindow(self.new_window, self.master)
        
class EntryWindow:
    def __init__(self, master, oldmaster):
        self.master = master
        self.headline = Label(self.master, text = 'Enter your Recipe here')
        self.quit_button = Button(self.master, text = 'Quit', width = 25, command = lambda:self.close_windows(oldmaster))
        headline_ingredients = Label(self.master, text="Enter your Ingredients")
        headline_name = Label(self.master, text="Enter your Recipes name")
        self.submit_button = Button(self.master, text='Submit', command=lambda:self.get_input())
        self.entry_name = Entry(self.master)
        self.entry_ingredients = Entry(self.master)
        
        self.headline.pack()
        headline_name.pack()
        self.entry_name.pack(pady=10)
        headline_ingredients.pack()
        self.entry_ingredients.pack(pady=10)
        self.submit_button.pack()
        self.quit_button.pack()

    def close_windows(self, oldmaster):
        oldmaster.deiconify()
        self.master.destroy()
    
    def get_input(self):
        name = self.entry_name.get()
        entry = self.entry_ingredients.get()
        print(f"{name}\n{entry}")

class SearchWindow:
    def __init__(self, master, oldmaster):
        self.master = master
        self.headline = Label(self.master, text = 'Search for your Recipe here')
        self.quit_button = Button(self.master, text = 'Quit', width = 25, command = lambda:self.close_windows(oldmaster))
        self.submit_button = Button(self.master, text='Submit', command=lambda:self.get_input())
        self.text = Text(self.master, width=80, height=15)
        
        self.headline.pack()
        self.submit_button.pack()
        self.text.pack()
        self.quit_button.pack()

    def close_windows(self, oldmaster):
        oldmaster.deiconify()
        self.master.destroy()
    
    def get_input(self):
        input = self.entry_ingredients.get()
        print(input)
        
def main(): 
    root = Tk()
    root.geometry('700x350')
    MainWindow(root)
    root.mainloop()

main()