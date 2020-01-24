try:
    from Tkinter import StringVar, Entry, Frame, Listbox, Scrollbar
    from Tkconstants import *
except ImportError:
    from tkinter import StringVar, Entry, Frame, Listbox, Scrollbar
    from tkinter.constants import *

try:
    import Tkinter as tk
    import ttk
except ModuleNotFoundError:
    import tkinter as tk
    import tkinter.ttk as ttk

from tkinter import *
import json
from PIL import Image, ImageTk


###########################################
filename = 'rs_items.json'
with open(filename) as f:
    alldicts = json.load(f)

names = []
prices = []
for key in alldicts.items():
    names.append(key[1]['name'])
print(names)
for price in alldicts.items():
    prices.append(price[1]['sell_average'])

print(prices)
list_of_items = names



###########################################

def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


class Combobox_Autocomplete(Entry, object):

    def __init__(self, master, list_of_items=None, autocomplete_function=None, listbox_width=None, listbox_height=7,
                 ignorecase_match=False, startswith_match=True, vscrollbar=True, hscrollbar=True, **kwargs):
        super().__init__(master)
        self.master = master
        if hasattr(self, "autocomplete_function"):
            if autocomplete_function is not None:
                raise ValueError("Combobox_Autocomplete subclass has 'autocomplete_function' implemented")
        else:
            if autocomplete_function is not None:
                self.autocomplete_function = autocomplete_function
            else:
                if list_of_items is None:
                    raise ValueError("If not guiven complete function, list_of_items can't be 'None'")

                if ignorecase_match:
                    if startswith_match:
                        def matches_function(entry_data, item):
                            return item.startswith(entry_data)
                    else:
                        def matches_function(entry_data, item):
                            return item in entry_data

                    self.autocomplete_function = lambda entry_data: [item for item in self.list_of_items if
                                                                     matches_function(entry_data, item)]
                else:
                    if startswith_match:
                        def matches_function(escaped_entry_data, item):
                            if re.match(escaped_entry_data, item, re.IGNORECASE):
                                return True
                            else:
                                return False
                    else:
                        def matches_function(escaped_entry_data, item):
                            if re.search(escaped_entry_data, item, re.IGNORECASE):
                                return True
                            else:
                                return False

                    def autocomplete_function(entry_data):
                        escaped_entry_data = re.escape(entry_data)
                        return [item for item in self.list_of_items if matches_function(escaped_entry_data, item)]

                    self.autocomplete_function = autocomplete_function

        self._listbox_height = int(listbox_height)
        self._listbox_width = listbox_width

        self.list_of_items = list_of_items

        self._use_vscrollbar = vscrollbar
        self._use_hscrollbar = hscrollbar

        kwargs.setdefault("background", "white")

        if "textvariable" in kwargs:
            self._entry_var = kwargs["textvariable"]
        else:
            self._entry_var = kwargs["textvariable"] = StringVar()

        Entry.__init__(self, master, **kwargs)

        self._trace_id = self._entry_var.trace('w', self._on_change_entry_var)

        self._listbox = None

        self.bind("<Tab>", self._on_tab)
        self.bind("<Up>", self._previous)
        self.bind("<Down>", self._next)
        self.bind('<Control-n>', self._next)
        self.bind('<Control-p>', self._previous)

        self.bind("<Return>", self._update_entry_from_listbox)
        self.bind("<Escape>", lambda event: self.unpost_listbox())

    def _on_tab(self, event):
        self.post_listbox()
        return "break"

    def _on_change_entry_var(self, name, index, mode):

        entry_data = self._entry_var.get()

        if entry_data == '':
            self.unpost_listbox()
            self.focus()
        else:
            values = self.autocomplete_function(entry_data)
            if values:
                if self._listbox is None:
                    self._build_listbox(values)
                else:
                    self._listbox.delete(0, END)

                    height = min(self._listbox_height, len(values))
                    self._listbox.configure(height=height)

                    for item in values:
                        self._listbox.insert(END, item)

            else:
                self.unpost_listbox()
                self.focus()

    def _build_listbox(self, values):
        listbox_frame = Frame()

        self._listbox = Listbox(listbox_frame, background="white", selectmode=SINGLE, activestyle="none",
                                exportselection=False)
        self._listbox.grid(row=0, column=0, sticky=N + E + W + S)

        self._listbox.bind("<ButtonRelease-1>", self._update_entry_from_listbox)
        self._listbox.bind("<Return>", self._update_entry_from_listbox)
        self._listbox.bind("<Escape>", lambda event: self.unpost_listbox())

        self._listbox.bind('<Control-n>', self._next)
        self._listbox.bind('<Control-p>', self._previous)

        if self._use_vscrollbar:
            vbar = Scrollbar(listbox_frame, orient=VERTICAL, command=self._listbox.yview)
            vbar.grid(row=0, column=1, sticky=N + S)

            self._listbox.configure(yscrollcommand=lambda f, l: autoscroll(vbar, f, l))

        if self._use_hscrollbar:
            hbar = Scrollbar(listbox_frame, orient=HORIZONTAL, command=self._listbox.xview)
            hbar.grid(row=1, column=0, sticky=E + W)

            self._listbox.configure(xscrollcommand=lambda f, l: autoscroll(hbar, f, l))

        listbox_frame.grid_columnconfigure(0, weight=1)
        listbox_frame.grid_rowconfigure(0, weight=1)

        x = -self.cget("borderwidth") - self.cget("highlightthickness")
        y = self.winfo_height() - self.cget("borderwidth") - self.cget("highlightthickness")

        if self._listbox_width:
            width = self._listbox_width
        else:
            width = self.winfo_width()

        listbox_frame.place(in_=self, x=x, y=y, width=width)

        height = min(self._listbox_height, len(values))
        self._listbox.configure(height=height)

        for item in values:
            self._listbox.insert(END, item)

    def post_listbox(self):
        if self._listbox is not None: return

        entry_data = self._entry_var.get()
        if entry_data == '': return

        values = self.autocomplete_function(entry_data)
        if values:
            self._build_listbox(values)

    def unpost_listbox(self):
        if self._listbox is not None:
            self._listbox.master.destroy()
            self._listbox = None

    def get_value(self):
        return self._entry_var.get()

    def set_value(self, text, close_dialog=False):
        self._set_var(text)

        if close_dialog:
            self.unpost_listbox()

        self.icursor(END)
        self.xview_moveto(1.0)

    def _set_var(self, text):
        self._entry_var.trace_vdelete("w", self._trace_id)
        self._entry_var.set(text)
        self._trace_id = self._entry_var.trace('w', self._on_change_entry_var)

    def _update_entry_from_listbox(self, event):
        if self._listbox is not None:
            current_selection = self._listbox.curselection()

            if current_selection:
                text = self._listbox.get(current_selection)
                self._set_var(text)

            self._listbox.master.destroy()
            self._listbox = None

            self.focus()
            self.icursor(END)
            self.xview_moveto(1.0)

        return "break"

    def _previous(self, event):
        if self._listbox is not None:
            current_selection = self._listbox.curselection()

            if len(current_selection) == 0:
                self._listbox.selection_set(0)
                self._listbox.activate(0)
            else:
                index = int(current_selection[0])
                self._listbox.selection_clear(index)

                if index == 0:
                    index = END
                else:
                    index -= 1

                self._listbox.see(index)
                self._listbox.selection_set(first=index)
                self._listbox.activate(index)

        return "break"

    def _next(self, event):
        if self._listbox is not None:

            current_selection = self._listbox.curselection()
            if len(current_selection) == 0:
                self._listbox.selection_set(0)
                self._listbox.activate(0)
            else:
                index = int(current_selection[0])
                self._listbox.selection_clear(index)

                if index == self._listbox.size() - 1:
                    index = 0
                else:
                    index += 1

                self._listbox.see(index)
                self._listbox.selection_set(index)
                self._listbox.activate(index)
        return "break"

    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk
        import tkinter as tk


#######################################################################################################################

class App(tk.Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)
        self.root = master
        self.master.title('Rebuild List')
        # Width, Height of application
        self.master.geometry("575x600")
        self.store = Combobox_Autocomplete
        self.alldicts = {}
        self.create_widgets()
        self.create_widgets1()

    def create_widgets(self, *args):
        # Image
        self.imgtitle = ImageTk.PhotoImage(Image.open('snapsrebuild.png'))
        self.lab = tk.Label(image=self.imgtitle)
        self.lab.grid(row=0, column=0, columnspan=6, padx=20, pady=20)
        # Supplies Label
        self.consume_label = tk.Label(self.root, text='Supplies:', font=('Arial', 12, 'bold'))
        self.consume_label.grid(row=1, column=0, columnspan=2, padx=50)
        # AutoCompleteBox
        self.entry_0 = tk.StringVar()
        self.combobox_autocomplete = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_0,
                                                           width=32, highlightthickness=1)
        self.combobox_autocomplete.grid(row=2, column=0, sticky="W", padx=20, pady=10)
        # Insert Button
        self.insert_butt = tk.Button(self.root, text='Insert', command=lambda: self.commando())
        self.insert_butt.place(x=220, y=155)
        # List Box
        self.list_box = Listbox(self.root, border=1, width=40, height=20, justify='center')
        self.list_box.grid(row=3, rowspan=5, column=0, padx=20)
        # Delete Button
        self.del_button = tk.Button(self.root, text='Delete', command=lambda: self.delbutton())
        self.del_button.place(x=175, y=520)
        # Check Button
        self.check_button = tk.Button(self.root, text='Check', command=lambda: self.checkbutton())
        self.check_button.place(x=50, y=520)
        # Uncheck Button
        self.uncheck_button = tk.Button(self.root, text='Uncheck', command=lambda: self.uncheckbutton())
        self.uncheck_button.place(x=105, y=520)

        self.list_box.insert(END, "Dragon Claws")
        self.list_box.insert(END, "Super Combat Potions")
    def delbutton(self):
        self.list_box.delete(ACTIVE)

    def checkbutton(self):
        self.list_box.itemconfig(ACTIVE, {'bg': 'green'})

    def uncheckbutton(self):
        self.list_box.itemconfig(ACTIVE, {'bg': '#ffffff'})


    # def commando(self):
    #     x = 'Consumables'
    #     self.alldicts.update({x: (self.entry_0.get())})
    #     self.list_box.insert(END, self.entry_0.get())
    #     for (key, value) in self.alldicts.items():
    #         print(key, "::", value)
    #     return ()

    #######################################################################################################################

    def create_widgets1(self):
        # Gear Label
        self.consume_label1 = tk.Label(self.root, text='Gear', font=('Arial', 12, 'bold'))
        self.consume_label1.grid(row=1, column=2, padx=50)
        self.entry_1 = tk.StringVar()
        self.combobox_autocomplete1 = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_1,
                                                            width=32,
                                                            highlightthickness=1)
        self.combobox_autocomplete1.grid(row=2, column=2, padx=20, pady=10, sticky="W")
        # Insert Button
        self.insert_butt1 = tk.Button(self.root, text='Insert', command=lambda: self.commando1())
        self.insert_butt1.place(x=505, y=155)
        # List Box
        self.list_box1 = Listbox(self.root, border=1, width=40, height=20)
        self.list_box1.grid(row=3, rowspan=5, column=2, padx=20)
        # Delete Button
        self.del_button1 = tk.Button(self.root, text='Delete', command=lambda: self.delbutton1())
        self.del_button1.place(x=502, y=520)
        # Check Button
        self.check_button1 = tk.Button(self.root, text='Check', command=lambda: self.checkbutton1())
        self.check_button1.place(x=305, y=520)
        # Uncheck Button
        self.uncheck_button1 = tk.Button(self.root, text='Uncheck', command=lambda: self.uncheckbutton1())
        self.uncheck_button1.place(x=400, y=520)


        self.headers = [" ITEM", "                                            PRICE"]
        self.row_format = "{:<8}  {:>8}"
        self.list_box1.insert(0, self.row_format.format(*self.headers, sp="       " * 6))
        self.list_box1.insert(1, '-----------------------------------------------------------')

    def delbutton1(self):
        self.list_box1.delete(ACTIVE)

    def checkbutton1(self):
        self.list_box1.itemconfig(ACTIVE, {'bg': 'green'})

    def uncheckbutton1(self):
        self.list_box1.itemconfig(ACTIVE, {'bg': '#ffffff'})




    def commando1(self):
        x = 'Gear'
        self.alldicts.update({x: (self.entry_1.get())})
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        for item in names:
            if item in self.entry_1.get():
                indexNumber = names.index(self.entry_1.get())
                print(indexNumber)
                self.priceIndex = prices[indexNumber]
                self.ent = self.entry_1.get()
                self.headers1 = [self.ent,'                            ', f"{self.priceIndex:,d}"]
                self.row_format1 = "{:<8}  {:>8} {:>8}"
                self.list_box1.insert(END, self.row_format1.format(*self.headers1))
        return ()


#######################################################################################################################

def main():
    root = tk.Tk()
    app = App(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()
