import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from LibraryDbSQlite import LibraryDbSQlite

class LibraryGui(customtkinter.CTk):

    def __init__(self, dataBase=LibraryDbSQlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        # 'App Main' ---------------------------------------------------------------------------------------------------------
        self.title('Library Record Management System')
        self.geometry('1000x800')
        self.config(bg='#2F5061')
        self.resizable(False, False)

        self.font1 = ('Arial', 20, 'bold')
        self.font2 = ('Arial', 12, 'bold')

        # Data Entry Form ---------------------------------------------------------------------------------------------------------
        # 'Book ID' Label and Entry Widgets ---------------------------------------------------------------------------------------------------------
        self.id_label = self.newCtkLabel('Book ID')
        self.id_label.place(x=20, y=450)
        self.id_entry = self.newCtkEntry()
        self.id_entry.place(x=120, y=450)

        # 'Title' Label and Entry Widgets ---------------------------------------------------------------------------------------------------------
        self.name_label = self.newCtkLabel('Title')
        self.name_label.place(x=20, y=500)
        self.name_entry = self.newCtkEntry()
        self.name_entry.place(x=120, y=500)

        # 'Author' Label and Entry Widgets ---------------------------------------------------------------------------------------------------------
        self.author_label = self.newCtkLabel('Author')
        self.author_label.place(x=20, y=550)
        self.author_entry = self.newCtkEntry()
        self.author_entry.place(x=120, y=550)

        # 'Publisher' Label and Entry Widgets ---------------------------------------------------------------------------------------------------------
        self.publisher_label = self.newCtkLabel('Publisher')
        self.publisher_label.place(x=20, y=600)
        self.publisher_entry = self.newCtkEntry()
        self.publisher_entry.place(x=120, y=600)

        # 'Year' Label and Entry Widgets ---------------------------------------------------------------------------------------------------------
        self.year_label = self.newCtkLabel('Year')
        self.year_label.place(x=20, y=650)
        self.year_entry = self.newCtkEntry()
        self.year_entry.place(x=120, y=650)

        # 'Genre' Label and Entry Widgets ---------------------------------------------------------------------------------------------------------
        self.Genre_label = self.newCtkLabel('Genre')
        self.Genre_label.place(x=20, y=700)
        self.Genre_entry = self.newCtkEntry()
        self.Genre_entry.place(x=120, y=700)


        # 'Status' Label and Combo Box Widgets ---------------------------------------------------------------------------------------------------------
        self.status_label = self.newCtkLabel('Status')
        self.status_label.place(x=20, y=750)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['In Library', 'Borrowed', 'To be replaced']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=120, y=750)


        # 'Add Button' ---------------------------------------------------------------------------------------------------------
        self.add_button = self.newCtkButton(text='Add Record',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=400,y=450)

        # 'New button' ---------------------------------------------------------------------------------------------------------
        self.new_button = self.newCtkButton(text='New Record',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=115, y=400)

        # 'Update Button' ---------------------------------------------------------------------------------------------------------
        self.update_button = self.newCtkButton(text='Update Record',
                                    onClickHandler=self.update_entry,
                                    fgColor='#FFC300',
                                    hoverColor='#d1a104',
                                    borderColor='#FFC300')
        self.update_button.place(x=550,y=500)

        # 'Delete Button' ---------------------------------------------------------------------------------------------------------
        self.delete_button = self.newCtkButton(text='Delete Record',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=700,y=450)

        # 'Export Button' ---------------------------------------------------------------------------------------------------------
        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv,
                                    fgColor='#9B0000',
                                    hoverColor='#6e0101',
                                    borderColor='#9B0000')
        self.export_button.place(x=700,y=550)

         # 'Import Button' ---------------------------------------------------------------------------------------------------------
        self.import_button = self.newCtkButton(text='Import from CSV',
                                    onClickHandler=self.import_from_csv,
                                    fgColor='#1A7A00',
                                    hoverColor='#125700',
                                    borderColor='#1A7A00')
        self.import_button.place(x=400,y=550)

         # 'Export JSON Button' ---------------------------------------------------------------------------------------------------------
        self.export_json_button = self.newCtkButton(text='Export to JSON',
                                    onClickHandler=self.export_to_json,
                                    fgColor='#FFC300',
                                    hoverColor='#d1a104',
                                    borderColor='#FFC300')
        self.export_json_button.place(x=550,y=600)

        # Tree View for Database Entries ---------------------------------------------------------------------------------------------------------
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#8b8c8c',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('ID', 'Title', 'Author', 'Publisher', 'Year', 'Genre', 'Status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=30)
        self.tree.column('Title', anchor=tk.CENTER, width=150)
        self.tree.column('Author', anchor=tk.CENTER, width=150)
        self.tree.column('Publisher', anchor=tk.CENTER, width=150)
        self.tree.column('Year', anchor=tk.CENTER, width=150)
        self.tree.column('Genre', anchor=tk.CENTER, width=150)
        self.tree.column('Status', anchor=tk.CENTER, width=100)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Author', text='Author')
        self.tree.heading('Publisher', text='Publisher')
        self.tree.heading('Year', text='Year')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Status', text='Status')

        self.tree.place(x=20, y=20, width=960, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget ---------------------------------------------------------------------------------------------------------
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFFFFF'
        widget_BgColor='#2F5061'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget ---------------------------------------------------------------------------------------------------------
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#2F5061'
        widget_FgColor='#FFF'
        widget_BorderColor='#2F5061'
        widget_BorderWidth=1
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget ---------------------------------------------------------------------------------------------------------
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#0A0E0D'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget ---------------------------------------------------------------------------------------------------------
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#2F5061', hoverColor='#FF5002', bgColor='#2F5061', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=260
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget
    

    # Handles
    # 'Add to tree view' ---------------------------------------------------------------------------------------------------------
    def add_to_treeview(self):
        records = self.db.fetch_record()
        self.tree.delete(*self.tree.get_children())
        for record in records:
            print(record)
            self.tree.insert('', END, values=record)

    # 'Clear Form' ---------------------------------------------------------------------------------------------------------
    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.publisher_entry.delete(0, END)
        self.year_entry.delete(0, END)
        self.Genre_entry.delete(0, END)
        self.status_cboxVar.set('In Library')

    # 'Read Display' ---------------------------------------------------------------------------------------------------------
    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.id_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.author_entry.insert(0, row[2])
            self.publisher_entry.insert(0, row[3])
            self.year_entry.insert(0, row[4])
            self.Genre_entry.insert(0, row[5])
            self.status_cboxVar.set(row[6])
        else:
            pass
    
    # 'Add Entry' ---------------------------------------------------------------------------------------------------------
    def add_entry(self):
        id=self.id_entry.get()
        title=self.name_entry.get()
        author=self.author_entry.get()
        publisher=self.publisher_entry.get()
        year=self.year_entry.get()
        genre=self.Genre_entry.get()
        status=self.status_cboxVar.get()

        if not (id and title and author and publisher and year and genre and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(id):
            messagebox.showerror('Error', 'ID already exists')
        else:
            
            self.db.insert_record(id, title, author, publisher, year, genre, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')
    
    # 'Update Entry' ---------------------------------------------------------------------------------------------------------
    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a record to delete')
        else:
            id = self.id_entry.get()
            self.db.delete_record(id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')
    # 'Update Entry' ---------------------------------------------------------------------------------------------------------
    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a record to update')
        else:
            id=self.id_entry.get()
            title=self.name_entry.get()
            author=self.author_entry.get()
            publisher=self.publisher_entry.get()
            year=self.year_entry.get()
            genre=self.Genre_entry.get()
            status=self.status_cboxVar.get()
            
            self.db.update_record(title, author, publisher, year, genre, status, id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    # 'Export Entry' ---------------------------------------------------------------------------------------------------------
    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    from tkinter import filedialog
    # 'Import Entry' ---------------------------------------------------------------------------------------------------------
    from tkinter import filedialog
    def import_from_csv(self):
        file_path = self.filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.db.import_csv(file_path)
            self.add_to_treeview()
            messagebox.showinfo('Success', f'Data imported from {file_path}')

    # 'Export JSON' ---------------------------------------------------------------------------------------------------------
    def export_to_json(self):
        file_path = self.filedialog.asksaveasfilename(title="Save JSON file", defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if file_path:
            self.db.export_json(file_path)
            messagebox.showinfo('Success', f'Data exported to {file_path}')

