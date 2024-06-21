import tkinter as tk
from tkinter import ttk
from db_funcs import *


class MasterWindow(tk.Tk):
    pass


class SubFrame(ttk.Frame):
    def __init__(self, master: MasterWindow):
        super().__init__(master)
        self.master = master


class SignInFrame(SubFrame):
    def __init__(self, master):
        super().__init__(master)
        # Frame title
        ttk.Label(self, text="Sign In").grid(row=0, column=1)
        # Label for accounts
        ttk.Label(self, text="Accounts: ", anchor=tk.E).grid(row=1, column=0, sticky=tk.E)

        # Making drop down for accounts
        self.acc_selected = tk.StringVar()
        accounts = get_all_accounts()
        self.acc_dropdown = ttk.Combobox(self, textvariable=self.acc_selected, values=[acc.name for acc in accounts])
        self.acc_dropdown.grid(row=1, column=1, sticky=tk.W)

        # Bottom buttons
        ttk.Button(self, text="New Account", command=self.add_acc).grid(row=2, column=0, sticky="w", padx=10)
        ttk.Button(self, text="Select Account", command=self.select_acc).grid(row=2, column=2, sticky="e", padx=10)

        # Adding Weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def add_acc(self):
        pass

    def select_acc(self):
        pass


class NewAccountFrane(SubFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create title
        ttk.Label(self, text="New Account", anchor=tk.CENTER).grid(row=0, column=0, columnspan=2, sticky="ew")

        # Add User
        ttk.Label(self, text="Username: ", anchor=tk.E).grid(row=1, column=0, sticky="e")

        self.acc_name = tk.StringVar()
        self.name_entry = ttk.Entry(self, textvariable=self.acc_name)
        self.name_entry.grid(row=1, column=1, sticky="ew")

        # Create Buttons

    def back(self):
        pass

    def add_acc(self):
        pass


class TasksFrame(SubFrame):
    def __init__(self, master):
        super().__init__(master)


class NewTaskFrame(SubFrame):
    def __init__(self, master):
        super().__init__(master)


class NewCheckListFrame(SubFrame):
    def __init__(self, master):
        super().__init__(master)
