import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle

import json
import sqlite3
import urllib.request as request
from tkinter import *
from tkinter import messagebox

import requests
from PIL import Image, ImageTk
from autocompletebox import Combobox_Autocomplete
from dbase import Database
from save import Savebase

#######################################################################################################################
sdb = Savebase('saved.db')
db = Database('store.db')

with request.urlopen('https://rsbuddy.com/exchange/summary.json') as response:
    if response.getcode() == 200:
        source = response.read()
        data = json.loads(source)
        with open('rs_items.json', 'w')as f:
            json.dump(data, f, indent=4, sort_keys=True)
    else:
        print('Error')

filename = 'rs_items.json'
with open(filename) as f:
    alldicts = json.load(f)

names = []
prices = []
ids = []
for key in alldicts.items():
    names.append(key[1]['name'])

for id in alldicts.items():
    ids.append(id[0])

for price in alldicts.items():
    prices.append(price[1]['sell_average'])

list_of_items = names

# Adds the K M B T P - To the end of an INTEGER for the total amount
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

class App(tk.Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)
        self.root = master
        # self.root.config(bg="#")
        self.master.title('Rebuild List')
        # self.root.attributes('-alpha', 0.3)
        # Width, Height of application
        self.master.geometry("535x700")
        # Setting theme
        self.style = ThemedStyle(self.root)
        # self.style.set_theme("scidgrey")
        self.style.set_theme("scidblue")
        self.store = Combobox_Autocomplete
        self.alldicts = {}
        self.create_widgets()
        self.my_values_cal()
        self.populate_list()



    def create_widgets(self, *args):
        # menubar = Menu(self.master)
        # self.master.config(menu=menubar)
        # fileMenu = Menu(menubar)
        # fileMenu.add_command(label="Exit", command=self.save_sets())
        # menubar.add_cascade(label="File", menu=fileMenu)
        # menubar.config(background="blue")

        # Image
        self.imgtitle = ImageTk.PhotoImage(Image.open('C:\\Users\\Chris\\PycharmProjects\\Runescape_RebuildList_V2\\snapsrebuild.png'))
        self.lab = tk.Label(image=self.imgtitle)
        self.lab.grid(row=0, column=0, columnspan=6, padx=20, pady=20)
        self.infernalCape = ImageTk.PhotoImage(Image.open('C:\\Users\\Chris\\PycharmProjects\\Runescape_RebuildList_V2\\infernal.gif'))
        self.cape = tk.Label(image=self.infernalCape)
        self.cape.place(x=345,y=0)
        self.dclaws = ImageTk.PhotoImage(Image.open('C:\\Users\\Chris\\PycharmProjects\\Runescape_RebuildList_V2\\dclaws.png'))
        self.claws = tk.Label(image=self.dclaws)
        self.claws.place(x=20,y=20)
        self.tbow = ImageTk.PhotoImage(Image.open('C:\\Users\\Chris\\PycharmProjects\\Runescape_RebuildList_V2\\tbow.png'))
        self.bow = tk.Label(image=self.tbow)
        self.bow.place(x=110,y=50)
        # Supplies Label
        self.consume_label = tk.Label(self.root, text='Supplies:', font=('Arial', 12, 'bold'))
        self.consume_label.place(x=18,y=110)
        # AutoCompleteBox
        self.entry_0 = tk.StringVar()
        self.combobox_autocomplete = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_0,
                                                           width=32, highlightthickness=1)
        self.combobox_autocomplete.grid(row=2, column=0, columnspan=5, sticky="W", padx=20, pady=10, ipady=3)
        # Quantity Box
        self.quantity = tk.StringVar()
        self.combobox_autocomplete1 = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.quantity,
                                                           width=5, highlightthickness=1, justify='center')
        self.combobox_autocomplete1.place(x=227,y=136)
        # Tree View
        self.tree = ttk.Treeview(self.root, height=20, columns=('id', 'items total', 'quantity'))
        self.tree.heading('#0', text='LIST OF ITEMS', anchor=tk.CENTER)
        self.tree.heading('#1', text='#', anchor=tk.CENTER)
        self.tree.heading('#2', text='PRICE', anchor=tk.CENTER)
        self.tree.heading('#3', text='TOTAL', anchor=tk.CENTER)
        self.tree.column('#0', stretch=tk.YES, minwidth=50, width=200, anchor='center')
        self.tree.column('#1', stretch=tk.YES, minwidth=50, width=50, anchor='center')
        self.tree.column('#2', stretch=tk.YES, minwidth=50, width=120, anchor='center')
        self.tree.column('#3', stretch=tk.YES, minwidth=50, width=120, anchor='center')
        self.tree.grid(row=3, column=0, padx=20)
        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        ysb.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscroll=ysb.set)
        self.tree.bind('<ButtonRelease-1>', self.select_item)
        # Insert Button
        self.insert_butt = ttk.Button(self.root, text='Insert', width=5, command=lambda : self.commando1())
        self.insert_butt.place(x=275, y=133)
        # Total Labels down the bottom
        self.lab = tk.Label(self.root, text='0', font=('courier',15,'bold'))
        self.lab.place(x=420,y=607)
        self.lab1 = tk.Label(self.root, text='TOTAL', font=('courier',15,'bold'))
        self.lab1.place(x=350, y=607)
        self.gambling = tk.Label(self.root, text='Just Say Neigh To Gambling', font=('courier',15,'bold'))
        self.gambling.place(x=20, y=650)
        # Delete Button
        self.del_button1 = ttk.Button(self.root, text='Delete', command=lambda : self.delbutton1())
        self.del_button1.place(x=469, y=133)
        self.filemenu = Menu(self.root, tearoff=0)
        self.filemenu.add_command(label="Open", command='hello')
        self.filemenu.add_command(label="Save", command='hello')
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command='root.quit')

        # Save Current Set
        self.save_butt = ttk.Button(self.root, text='Save', command=lambda: self.save_sets())
        self.save_butt.place(x=175, y=607)

        # Update SAVED Sets Button
        self.save_butt = ttk.Button(self.root, text='Load', width=7, command=lambda: self.load_test())
        self.save_butt.place(x=210, y=607)

        # Delete Sets Button
        self.save_butt = ttk.Button(self.root, text='Delete', width=7, command=lambda: self.yeet())
        self.save_butt.place(x=263, y=607)

        # Saved Sets Entry Box
        self.save_entry = tk.StringVar()
        self.saved_sets = ttk.Combobox(self.root, width=20, text="Fuckwit", textvariable=self.save_entry, values='Fuckwit')
        self.saved_sets.place(x=20,y=610)

    def yeet(self):
        self.load_test()
        self.my_values()
    def load_test(self):
        self.read_saved = self.save_entry.get()
        self.test = sdb.read_from_db(self.read_saved)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for a in self.test:
            self.tree.insert('', 0, text=a[1], values=(a[2], a[3], a[4]))

    # Populating the tree view with item and quantity taken from the entry boxes
    def populate_list(self):
        for row in db.fetch():
            self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3]))

    def my_values(self):
        try:
            self.read = self.save_entry.get()
            self.summing = sdb.read_total_db(self.read)
            self.nig = int(self.summing[0][0])
            print(self.nig)
            self.nigTotal = self.nig
            if self.nigTotal <= 0:
                for i in self.tree.get_children():
                    self.populate_list()
            else:
                self.lab.config(text=human_format(self.nigTotal))
        except TypeError:
            self.lab.config(text=0)
            print('Fuckwit')

    def save_sets(self):
        self.save_item_name = []
        self.save_item_quantity = []
        self.save_item_price = []
        self.save_item_total = []
        self.save_item_summing = []
        for rows in db.fetch():
            self.save_item_name.append(rows[0])
            self.save_item_quantity.append(rows[1])
            self.save_item_price.append(rows[2])
            self.save_item_total.append(rows[3])
            self.save_item_summing.append(rows[4])
        for self.b in self.save_item_quantity:
            pass
        for self.c in self.save_item_price:
            pass
        for self.d in self.save_item_total:
            pass
        for self.e in self.save_item_summing:
            pass
        for self.a in self.save_item_name:
            sdb.insert(self.save_entry.get(), self.a,  self.b, self.c, self.d, self.e)

    def select_item(self, event):
        '''Select an item, adds the item back to the AutoComboBox and added the quanity for updating price'''
        try:
            self.selectItem = self.tree.focus()
            self.my_list = []
            tree = self.tree.item(self.selectItem)
            for k, v in tree.items():
                self.my_list.append(v)

            self.combobox_autocomplete.delete(0, END)
            self.combobox_autocomplete.insert(END, self.my_list[0])
            self.combobox_autocomplete1.delete(0, END)
            self.combobox_autocomplete1.insert(END, self.my_list[2][0])
        except IndexError:
            print('Waiting for information FatHead')

    def clear_text(self):
        self.combobox_autocomplete.delete(0, tk.END)
        self.combobox_autocomplete1.delete(0, tk.END)

    def commando1(self):
        x = 'Gear'
        # Insert to the database
        self.alldicts.update({x: (self.entry_0.get())})
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        try:
            for item in names:
                if item in self.entry_0.get():
                    indexNumber = names.index(self.entry_0.get())
                    self.outputPrice = prices[indexNumber]
                    self.int_price = int(self.outputPrice)
                    self.int_quantity = int(self.quantity.get())
                    self.totalPrice = self.int_price * self.int_quantity
                    self.jsonPrice = f"{self.outputPrice:,d}"
                    self.humanFormat = f"{human_format(self.totalPrice)}"
                    self.totalPrice = int(self.totalPrice)
                    db.insert(self.entry_0.get(), self.quantity.get(), self.jsonPrice, self.humanFormat, self.totalPrice)
                    self.tree.insert('', 'end', text=self.entry_0.get(), values=(self.quantity.get(), self.jsonPrice, self.humanFormat))
                    self.my_values_cal()
        except ValueError:
                    self.messagebox = messagebox.showinfo('Error', 'Please enter a number')

    def delbutton1(self):
        self.conn = sqlite3.connect('store.db')
        self.cur = self.conn.cursor()
        for self.selected_item in self.tree.selection():
            self.cur.execute("DELETE FROM list WHERE price=?", (self.tree.set(self.selected_item, '#2'),))
            self.conn.commit()
            # self.tree.delete(self.selected_item)
            self.my_values_cal()
        self.conn.close()
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.populate_list()



    def my_values_cal(self):
        try:
            self.sum = db.read_from_db()
            self.int1 = int(self.sum[0][0])
            self.sumTotal = self.int1
            if self.sumTotal < 5:
                for i in self.tree.get_children():
                    self.populate_list()
                    # print(i)
            else:
                self.lab.config(text=human_format(self.int1))
                # print(self.int1)
        except TypeError:
            self.lab.config(text=0)
            print('First time loading Database.')


def main():
    root = tk.Tk()
    app = App(master=root)
    root.mainloop()

if __name__ == '__main__':
    main()
