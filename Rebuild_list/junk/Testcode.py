import tkinter as tk

class App(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        master.title('Rebuild List')
        # Width, Height of application
        master.geometry("750x400")
        # Creates Widgets and Grid
        self.create_widgets()
        self.dicts = {}

    def create_widgets(self):
        # self.chkValue = tk.StringVar()
        # self.check4 = tk.Checkbutton(self.master, text="check me", variable=self.chkValue, onvalue="on", offvalue="off")
        # self.check4.grid(row=5, column=0, ipady=10)
        # self.check4.deselect()
        # Entry Label To the right of the checkbox
        self.y = tk.StringVar()
        self.consume_entry3 = tk.Entry(self.master,textvariable=self.y, justify='left')
        self.consume_entry3.grid(row=5, column=1)
        # Insert button
        self.insert_butt3 = tk.Button(self.master, text='Insert', state='active', command= lambda : self.commando())
        self.insert_butt3.grid(row=5, column=2,padx=10)
        self.insert_butt4 = tk.Button(self.master, text='Insert', command=lambda: self.test())
        self.insert_butt4.grid(row=6, column=2, padx=10)

        # Consumbles lists on the left I think!?!
        # Check Button Number One
        # self.var1 = tk.StringVar()
        # self.check1 = tk.Checkbutton(self.master, variable=self.var1, onvalue="on", offvalue="off")
        # self.check1.grid(row=2, column=0, ipady=10, padx=10)
        # self.check1.deselect()
        # Entry Label To the right of the checkbox
        self.a = tk.StringVar()
        self.consume_entry = tk.Entry(self.master, textvariable=self.a, justify='left')
        self.consume_entry.grid(row=2, column=1)
        # Insert button
        self.insert_butt = tk.Button(self.master, text='Insert', command=lambda: self.commando1())
        self.insert_butt.grid(row=2, column=2, padx=10)
        ########################################################################################################################
        # Parts list (listbox)
        self.list_box = tk.Listbox(self.master, border=0)
        self.list_box.grid(row=2, rowspan=5, column=3)

        self.boolean_var = tk.BooleanVar()
        self.option_yes = tk.Radiobutton(self.master, text="Yes", variable=self.boolean_var, value=True, command=self.callback)
        self.option_no = tk.Radiobutton(self.master, text="No", variable=self.boolean_var, value=False, command=self.callback)
        self.option_yes.grid(row=2, column=0)
        self.option_no.grid(row=1, column=1)

    def callback(self):
        self.list_box.itemconfig(0, {'bg': 'red'})







    # def test2(self):
    #     if self.chkValue == True:
    #         print("Oh. I'm clicked")
    #     else:
    #         pass





if __name__ == '__main__':
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()


