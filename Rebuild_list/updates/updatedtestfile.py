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

for key in alldicts.items():
    names.append(key[1]['name'])

for name in names:
    print(name)
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
#######################################################################################################################
#######################################################################################################################
class App(tk.Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)
        self.root = master
        self.master.title('Rebuild List')
        # Width, Height of application
        self.master.geometry("775x700")
        self.store = Combobox_Autocomplete
        self.alldicts = {}
        self.create_widgets()
        self.create_widgets1()
        self.refresh_button()

    def create_widgets(self, *args):
        # Calculate button
        self.imgtitle = ImageTk.PhotoImage(Image.open('C:\\Users\\Chris\\PycharmProjects\\untitled\\snapsrebuild.png'))
        self.lab = tk.Label(image=self.imgtitle)
        self.lab.grid(row=0, column=3, padx=20, pady=20)
        # Heading Labels
        # Consumable Label
        self.consume_label = tk.Label(self.root, text='Items:', font=('Arial', 12, 'bold'))
        self.consume_label.grid(row=1, column=0, columnspan=3, padx=50)
        # Rebuild List Center Text
        self.consume_label = tk.Label(self.root, text='Rebuild List', font=('Arial', 12, 'bold'))
        self.consume_label.grid(row=1, column=3, padx=50)
        # Armour Text
        self.consume_label = tk.Label(self.root, text='items:', font=('Arial', 12, 'bold'))
        self.consume_label.grid(row=1, column=5, columnspan=3, padx=50)
        #######################################################################################################################
        #                                               Left Side buttons and input
        #######################################################################################################################
        # 111111
        # Check Button Number One
        self.is_checked = IntVar()
        self.option_yes = tk.Checkbutton(self.root, text="", onvalue=1, offvalue=0, variable=self.is_checked,
                                         command=self.callback)
        self.option_yes.grid(row=2, column=0, padx=15)
        # Entry Label To the right of the checkbox
        self.entry_0 = tk.StringVar()
        self.combobox_autocomplete = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_0,
                                                           highlightthickness=1)
        self.combobox_autocomplete.grid(row=2, column=1)
        # Insert button
        self.insert_butt = tk.Button(self.root, text='Insert', command=lambda: self.commando())
        self.insert_butt.grid(row=2, column=2, padx=10)
        ########################################################################################################################
        # Check Button Number Two                                                                                22222
        self.is_checked1 = IntVar()
        self.option_yes1 = tk.Checkbutton(self.root, text="", onvalue=1, offvalue=0, variable=self.is_checked1,
                                          command=self.callback1)
        self.option_yes1.grid(row=3, column=0, padx=15)
        # Entry Label To the right of the checkbox
        self.entry_1 = tk.StringVar()
        self.combobox_autocomplete1 = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_1,
                                                            highlightthickness=1)
        self.combobox_autocomplete1.grid(row=3, column=1)
        # Insert button
        self.insert_butt1 = tk.Button(self.root, text='Insert', command=lambda: self.commando1())
        self.insert_butt1.grid(row=3, column=2, padx=10)
        ########################################################################################################################
        # Check Button Number Three                                                                             3333333
        self.is_checked2 = IntVar()
        self.option_yes2 = tk.Checkbutton(self.root, text="", onvalue=1, offvalue=0, variable=self.is_checked2,
                                          command=self.callback2)
        self.option_yes2.grid(row=4, column=0, padx=15)
        # Entry Label To the right of the checkbox
        self.entry_2 = tk.StringVar()
        self.combobox_autocomplete2 = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_2,
                                                            highlightthickness=1)
        self.combobox_autocomplete2.grid(row=4, column=1)
        # Insert button
        self.insert_butt2 = tk.Button(self.root, text='Insert', command=lambda: self.commando2())
        self.insert_butt2.grid(row=4, column=2, padx=10)
        ########################################################################################################################
        # Check Button Number Four                                                                              4444444
        self.is_checked3 = IntVar()
        self.option_yes3 = tk.Checkbutton(self.root, text="", onvalue=1, offvalue=0, variable=self.is_checked3,
                                          command=self.callback3)
        self.option_yes3.grid(row=5, column=0, padx=15)
        # Entry Label To the right of the checkbox
        self.entry_3 = tk.StringVar()
        self.combobox_autocomplete3 = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_3,
                                                            highlightthickness=1)
        self.combobox_autocomplete3.grid(row=5, column=1)
        # Insert button
        self.insert_butt3 = tk.Button(self.root, text='Insert', command=lambda: self.commando3())
        self.insert_butt3.grid(row=5, column=2, padx=10)
        ########################################################################################################################
        # Parts list (listbox)                                                                                 LISTBOX:
        self.list_box = Listbox(self.root, border=0, width=40, height=20, justify='center')
        self.list_box.grid(row=2, rowspan=5, column=3, pady=5)
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.grid(row=3, column=4)
        # Set scrollbar to parts
        self.list_box.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.list_box.yview)

    ########################################################################################################################
    # LEFT SIDE FUNCTIONS
    ########################################################################################################################
    # Insert Button On the left right
    def commando(self):
        x = 'Consumables'
        self.alldicts.update({x: (self.entry_0.get())})
        self.list_box.delete(0)
        self.list_box.insert(0, self.entry_0.get())
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()

    def commando1(self):
        x = 'Consumables1'
        self.alldicts.update({x: (self.entry_1.get())})
        self.list_box.delete(1)
        self.list_box.insert(1, self.entry_1.get())
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()
        # Insert Button On the left right

    def commando2(self):
        x = 'Consumables2'
        self.alldicts.update({x: (self.entry_2.get())})
        self.list_box.delete(2)
        self.list_box.insert(2, self.entry_2.get())
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()
        # Insert Button On the left right

    def commando3(self):
        x = 'Consumables3'
        self.alldicts.update({x: (self.entry_3.get())})
        self.list_box.delete(3)
        self.list_box.insert(3, self.entry_3.get())
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()

    #######################################################################################################################
    def callback(self):
        if self.is_checked.get():
            self.list_box.itemconfig(0, {'bg': 'green'})
        else:
            self.list_box.itemconfig(0, {'bg': '#ffffff'})

    def callback1(self):
        if self.is_checked1.get():
            self.list_box.itemconfig(1, {'bg': 'green'})
        else:
            self.list_box.itemconfig(1, {'bg': '#ffffff'})

    def callback2(self):
        if self.is_checked2.get():
            self.list_box.itemconfig(2, {'bg': 'green'})
        else:
            self.list_box.itemconfig(2, {'bg': '#ffffff'})

    def callback3(self):
        if self.is_checked3.get():
            self.list_box.itemconfig(3, {'bg': 'green'})
        else:
            self.list_box.itemconfig(3, {'bg': '#ffffff'})

    ########################################################################################################################
    # RIGHT SIDE BUTTONS AND LABELS
    ########################################################################################################################
    # 5555555
    def create_widgets1(self, *args):
        # Check Button Number One
        self.is_checked4 = IntVar()
        self.option_yes4 = tk.Checkbutton(self.root, text="", onvalue=1, offvalue=0, variable=self.is_checked4,
                                          command=self.callback4)
        self.option_yes4.grid(row=2, column=7, padx=15)
        # Entry Label To the right of the checkbox
        self.entry_4 = tk.StringVar()
        self.combobox_autocomplete4 = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_4,
                                                            highlightthickness=1)
        self.combobox_autocomplete4.grid(row=2, column=6)
        # Insert button
        self.insert_butt4 = tk.Button(self.root, text='Insert', command=lambda: self.commando4())
        self.insert_butt4.grid(row=2, column=5, padx=10)
        ########################################################################################################################
        # Check Button Number Two                                                                               666666
        self.is_checked5 = IntVar()
        self.option_yes5 = tk.Checkbutton(self.root, text="", onvalue=1, offvalue=0, variable=self.is_checked5,
                                          command=self.callback5)
        self.option_yes5.grid(row=3, column=7, padx=15)
        # Entry Label To the right of the checkbox
        self.entry_5 = tk.StringVar()
        self.combobox_autocomplete5 = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_5,
                                                            highlightthickness=1)
        self.combobox_autocomplete5.grid(row=3, column=6)
        # Insert button
        self.insert_butt5 = tk.Button(self.root, text='Insert', command=lambda: self.commando5())
        self.insert_butt5.grid(row=3, column=5, padx=10)
        ########################################################################################################################
        # Check Button Number Three                                                                             777777
        self.is_checked6 = IntVar()
        self.option_yes6 = tk.Checkbutton(self.root, text="", onvalue=1, offvalue=0, variable=self.is_checked6,
                                          command=self.callback6)

        self.option_yes6.grid(row=4, column=7, padx=15)
        # Entry Label To the right of the checkbox
        self.entry_6 = tk.StringVar()
        self.combobox_autocomplete6 = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_6,
                                                            highlightthickness=1)
        self.combobox_autocomplete6.grid(row=4, column=6)
        # Insert button
        self.insert_butt6 = tk.Button(self.root, text='Insert', command=lambda: self.commando6())
        self.insert_butt6.grid(row=4, column=5, padx=10)
        ########################################################################################################################
        # Check Button Number Four                                                                             888888
        self.is_checked7 = IntVar()
        self.option_yes7 = tk.Checkbutton(self.root, text="", onvalue=1, offvalue=0, variable=self.is_checked7,
                                          command=self.callback7)

        self.option_yes7.grid(row=5, column=7, padx=15)
        # Entry Label To the right of the checkbox
        self.entry_7 = tk.StringVar()
        self.combobox_autocomplete7 = Combobox_Autocomplete(self.root, list_of_items, textvariable=self.entry_7,
                                                            highlightthickness=1)
        self.combobox_autocomplete7.grid(row=5, column=6)
        # Insert button
        self.insert_butt7 = tk.Button(self.root, text='Insert', command=lambda: self.commando7())
        self.insert_butt7.grid(row=5, column=5, padx=10)

    ########################################################################################################################
    #        FUNCTIONS FOR THE RIGHT SIDE
    ########################################################################################################################
    # Insert Buttons on the right side
    def commando4(self):
        x = 'Consumables'
        self.alldicts.update({x: (self.entry_4.get())})
        self.list_box.delete(4)
        self.list_box.insert(4, self.entry_4.get())
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()

    def commando5(self):
        x = 'Consumables1'
        self.alldicts.update({x: (self.entry_5.get())})
        self.list_box.delete(5)
        self.list_box.insert(5, self.entry_5.get())
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()

    def commando6(self):
        x = 'Consumables1'
        self.alldicts.update({x: (self.entry_6.get())})
        self.list_box.delete(6)
        self.list_box.insert(6, self.entry_6.get())
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()

    def commando7(self):
        x = 'Consumables1'
        self.alldicts.update({x: (self.entry_7.get())})
        self.list_box.delete(7)
        self.list_box.insert(7, self.entry_7.get())
        for (key, value) in self.alldicts.items():
            print(key, "::", value)
        return ()

    ########################################################################################################################
    def callback4(self):
        if self.is_checked4.get():
            self.list_box.itemconfig(4, {'bg': 'green'})
        else:
            self.list_box.itemconfig(4, {'bg': '#ffffff'})

    def callback5(self):
        if self.is_checked5.get():
            self.list_box.itemconfig(5, {'bg': 'green'})
        else:
            self.list_box.itemconfig(5, {'bg': '#ffffff'})

    def callback6(self):
        if self.is_checked6.get():
            self.list_box.itemconfig(6, {'bg': 'green'})
        else:
            self.list_box.itemconfig(6, {'bg': '#ffffff'})

    def callback7(self):
        if self.is_checked7.get():
            self.list_box.itemconfig(7, {'bg': 'green'})
        else:
            self.list_box.itemconfig(7, {'bg': '#ffffff'})

    #########################################################################################################################
    # Refresh button
    def refresh_button(self, *args):
        self.refresher = tk.Button(self.root, text='Refresh', command=lambda: self.refresh())
        self.refresher.grid(row=7, column=3, pady=10)

    # Need to refresh the colours that have been checked already, must clear the list box.
    def refresh(self, *args):
        self.list_box.delete(0, END)
        self.combobox_autocomplete.delete(0, "end")
        self.combobox_autocomplete1.delete(0, "end")
        self.combobox_autocomplete2.delete(0, "end")
        self.combobox_autocomplete3.delete(0, "end")
        self.combobox_autocomplete4.delete(0, "end")
        self.combobox_autocomplete5.delete(0, "end")
        self.combobox_autocomplete6.delete(0, "end")
        self.combobox_autocomplete7.delete(0, "end")


def main():
    root = tk.Tk()
    app = App(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()
