import tkinter as tk
import json
import re

try:
    from Tkinter import StringVar, Entry, Frame, Listbox, Scrollbar
    from Tkconstants import *

except ImportError:
    from tkinter import StringVar, Entry, Frame, Listbox, Scrollbar
    from tkinter.constants import *
    import json


class App(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.master = master
        master.title('Rebuild List')
        # Width, Height of application
        master.geometry("750x400")
        # Creates Widgets and Grids
        self.create_widgets()
        self.alldicts = {}
        self.create_widgets1()


########################################################################################################################
    def create_widgets(self):
        # Calculate button
        self.calculate = tk.Label(self.master, text='Rebuild Check List', width=30, font=('Arial', 10, 'bold'))
        self.calculate.grid(row=0, column=3, padx=20, pady=20, ipady=10)
    # Heading Labels
        # Consumable Label
        self.consume_label = tk.Label(self.master, text='Consumables', font=('Arial', 12, 'bold'))
        self.consume_label.grid(row=1, column=0, columnspan=3, padx=50)
        # Rebuild List Center Text
        self.consume_label = tk.Label(self.master, text='Rebuild List', font=('Arial', 12, 'bold'))
        self.consume_label.grid(row=1, column=3, padx=50)
        # Armour Text
        self.consume_label = tk.Label(self.master, text='Armours', font=('Arial', 12, 'bold'))
        self.consume_label.grid(row=1, column=5, columnspan=3, padx=50)
########################################################################################################################
        # Consumbles lists on the left I think!?!                                                               111111
        # Check Button Number One
        self.boolean_var = tk.BooleanVar()
        self.option_yes = tk.Radiobutton(self.master, text="", variable=self.boolean_var, value=True,
                                         command=self.callback)
        self.option_yes.grid(row=2, column=0)
        # Entry Label To the right of the checkbox
        self.a = tk.StringVar()
        self.consume_entry = tk.Entry(self.master, textvariable=self.a, justify='left')
        self.consume_entry.grid(row=2, column=1)
        # Insert button
        self.insert_butt = tk.Button(self.master, text='Insert', command= lambda : self.commando())
        self.insert_butt.grid(row=2, column=2,padx=10)
########################################################################################################################
        # Check Button Number Two                                                                                22222
        self.boolean_var1 = tk.BooleanVar()
        self.option_yes1 = tk.Radiobutton(self.master, text="", variable=self.boolean_var1, value=True,
                                         command=self.callback1)
        self.option_yes1.grid(row=3, column=0)
        # Entry Label To the right of the checkbox
        self.b = tk.StringVar()
        self.consume_entry1 = tk.Entry(self.master,textvariable=self.b, justify='left')
        self.consume_entry1.grid(row=3, column=1)
        # Insert button
        self.insert_butt1 = tk.Button(self.master, text='Insert', command=lambda: self.commando1())
        self.insert_butt1.grid(row=3, column=2,padx=10)
########################################################################################################################
        # Check Button Number Three                                                                             3333333
        self.boolean_var2 = tk.BooleanVar()
        self.option_yes2 = tk.Radiobutton(self.master, text="", variable=self.boolean_var2, value=True,
                                         command=self.callback2)
        self.option_yes2.grid(row=4, column=0)
        # Entry Label To the right of the checkbox
        self.c = tk.StringVar()
        self.consume_entry2 = tk.Entry(self.master,textvariable=self.c, justify='left')
        self.consume_entry2.grid(row=4, column=1)
        # Insert button
        self.insert_butt2 = tk.Button(self.master, text='Insert', command=lambda: self.commando2())
        self.insert_butt2.grid(row=4, column=2,padx=10)
########################################################################################################################
        # Check Button Number Four                                                                              4444444
        self.boolean_var3 = tk.BooleanVar()
        self.option_yes3 = tk.Radiobutton(self.master, text="", variable=self.boolean_var3, value=True,
                                         command=self.callback3)
        self.option_yes3.grid(row=5, column=0)
        # Entry Label To the right of the checkbox
        self.d = tk.StringVar()
        self.consume_entry3 = tk.Entry(self.master,textvariable=self.d, justify='left')
        self.consume_entry3.grid(row=5, column=1)
        # Insert button
        self.insert_butt3 = tk.Button(self.master, text='Insert', command=lambda: self.commando3())
        self.insert_butt3.grid(row=5, column=2,padx=10)
########################################################################################################################
        # Parts list (listbox)                                                                                 LISTBOX:
        self.list_box = tk.Listbox(self.master, border=0, width=40, justify='center')
        self.list_box.grid(row=2, rowspan=5, column=3)
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=4)
        # Set scrollbar to parts
        self.list_box.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.list_box.yview)
########################################################################################################################
    # Insert Button On the left right
    def commando(self):
        x = 'Consumables'
        self.alldicts.update({x:(self.a.get())})
        self.list_box.insert("end", self.a.get())
        self.insert_butt.config(state="disabled")
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return()
    # Insert Button On the left right
    def commando1(self):
        x = 'Consumables1'
        self.alldicts.update({x:(self.b.get())})
        self.list_box.insert("end", self.b.get())
        self.insert_butt1.config(state="disabled")
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return()
    # Insert Button On the left right
    def commando2(self):
        x = 'Consumables1'
        self.alldicts.update({x: (self.c.get())})
        self.list_box.insert("end", self.c.get())
        self.insert_butt2.config(state="disabled")
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()
    # Insert Button On the left right
    def commando3(self):
        x = 'Consumables1'
        self.alldicts.update({x: (self.d.get())})
        self.list_box.insert("end", self.d.get())
        self.insert_butt3.config(state="disabled")
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()
########################################################################################################################
    # Call back function to color the text
    def callback(self):
        self.list_box.itemconfig(0, {'bg': 'green'})
    # Call back function to color the text
    def callback1(self):
        self.list_box.itemconfig(1, {'bg': 'green'})
    # Call back function to color the text
    def callback2(self):
        self.list_box.itemconfig(2, {'bg': 'green'})
    # Call back function to color the text
    def callback3(self):
        self.list_box.itemconfig(3, {'bg': 'green'})
########################################################################################################################
########################################################################################################################
    def create_widgets1(self):
        # Consumbles lists on the left I think!?!                                                               111111
        # Check Button Number One
        self.boolean_varR = tk.BooleanVar()
        self.option_yesR = tk.Radiobutton(self.master, text="", variable=self.boolean_varR, value=True,
                                         command=self.callbackk)
        self.option_yesR.grid(row=2, column=8)
        # Entry Label To the right of the checkbox
        self.aR = tk.StringVar()
        self.consume_entryR = tk.Entry(self.master, textvariable=self.aR, justify='left')
        self.consume_entryR.grid(row=2, column=7)

        # Insert button
        self.insert_buttR = tk.Button(self.master, text='Insert', command= lambda : self.commandoo())
        self.insert_buttR.grid(row=2, column=6,padx=10)
########################################################################################################################
        # Check Button Number Two                                                                                22222
        self.boolean_var1R = tk.BooleanVar()
        self.option_yes1R = tk.Radiobutton(self.master, text="", variable=self.boolean_var1R, value=True,
                                         command=self.callback11)
        self.option_yes1R.grid(row=3, column=8)
        # Entry Label To the right of the checkbox
        self.bR = tk.StringVar()
        self.consume_entry1R = tk.Entry(self.master,textvariable=self.bR, justify='left')
        self.consume_entry1R.grid(row=3, column=7)
        # Insert button
        self.insert_butt1R = tk.Button(self.master, text='Insert', command=lambda: self.commando11())
        self.insert_butt1R.grid(row=3, column=6,padx=10)
########################################################################################################################
        # Check Button Number Three                                                                             3333333
        self.boolean_var2R = tk.BooleanVar()
        self.option_yes2R = tk.Radiobutton(self.master, text="", variable=self.boolean_var2R, value=True,
                                         command=self.callback22)
        self.option_yes2R.grid(row=4, column=8)
        # Entry Label To the right of the checkbox
        self.cR = tk.StringVar()
        self.consume_entry2R = tk.Entry(self.master,textvariable=self.cR, justify='left')
        self.consume_entry2R.grid(row=4, column=7)
        # Insert button
        self.insert_butt2R = tk.Button(self.master, text='Insert', command=lambda: self.commando22())
        self.insert_butt2R.grid(row=4, column=6,padx=10)
########################################################################################################################
        # Check Button Number Four                                                                              4444444
        self.boolean_var3R = tk.BooleanVar()
        self.option_yes3R = tk.Radiobutton(self.master, text="", variable=self.boolean_var3R, value=True,
                                         command=self.callback33)
        self.option_yes3R.grid(row=5, column=8)
        # Entry Label To the right of the checkbox
        self.dR = tk.StringVar()
        self.consume_entry3R = tk.Entry(self.master,textvariable=self.dR, justify='left')
        self.consume_entry3R.grid(row=5, column=7)
        # Insert button
        self.insert_butt3R = tk.Button(self.master, text='Insert', command=lambda: self.commando33())
        self.insert_butt3R.grid(row=5, column=6,padx=10)
########################################################################################################################
    # Insert Button On the right
    def commandoo(self):
        x = 'Consumables'
        self.alldicts.update({x:(self.a.get())})
        self.list_box.insert("end", self.a.get())
        self.insert_buttR.config(state="disabled")
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return()
    # Insert Button On the left right
    def commando11(self):
        x = 'Consumables1'
        self.alldicts.update({x:(self.b.get())})
        self.list_box.insert("end", self.b.get())
        self.insert_butt1R.config(state="disabled")
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return()
    # Insert Button On the left right
    def commando22(self):
        x = 'Consumables1'
        self.alldicts.update({x: (self.c.get())})
        self.list_box.insert("end", self.c.get())
        self.insert_butt2R.config(state="disabled")
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()
    # Insert Button On the left right
    def commando33(self):
        x = 'Consumables1'
        self.alldicts.update({x: (self.d.get())})
        self.list_box.insert("end", self.d.get())
        self.insert_butt3R.config(state="disabled")
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()
########################################################################################################################
    # Call back function to color the text
    def callbackk(self):
        self.list_box.itemconfig(4, {'bg': 'green'})
    # Call back function to color the text
    def callback11(self):
        self.list_box.itemconfig(5, {'bg': 'green'})
    # Call back function to color the text
    def callback22(self):
        self.list_box.itemconfig(6, {'bg': 'green'})
    # Call back function to color the text
    def callback33(self):
        self.list_box.itemconfig(7, {'bg': 'green'})
########################################################################################################################


root = tk.Tk()
app = App(master=root)
app.mainloop()





##### try and get the list box to corospond with their names and their positions.

###### Potentially add in the prices to buy a full rebuild

###### Add in Staking sessions how much youu are up or down per sesh at the casino and log it

###### Refactor all the code to put into different folders etc.

#### Potential make a bot to rebuy these items

### Clear button / Refresh button



