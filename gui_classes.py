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
        self.acc_selected.set(accounts[0].name if len(accounts) != 0 else "")

        self.acc_dropdown = ttk.Combobox(self,
                                         textvariable=self.acc_selected,
                                         state="readonly",
                                         values=[acc.name for acc in accounts])
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
        self.name_entry.grid(row=1, column=1, sticky=tk.EW)

        # Create Buttons
        self.back_button = ttk.Button(self, text="<-", command=self.back)
        self.back_button.grid(row=2, column=0, sticky=tk.W)

        self.add_button = ttk.Button(self, text="Add", command=self.add_acc)
        self.add_button.grid(row=2, column=1, sticky=tk.E)

    def back(self):
        pass

    def add_acc(self):
        pass


class TasksFrame(SubFrame):
    def __init__(self, master):
        super().__init__(master)

        # Creating sub frames
        self.top_frame = ttk.Frame(self)

        self.mid_frame = ttk.Frame(self)
        self.content_frame = ttk.Frame(self.mid_frame)
        self.scroll_frame = ttk.Frame(self.mid_frame)

        self.bottom_frame = ttk.Frame(self)

        # Packing the sub frames
        self.top_frame.pack(fill=tk.X, expand=True)
        ttk.Separator(self).pack(fill=tk.X, expand=False)

        self.mid_frame.pack(fill=tk.BOTH, expand=True)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        ttk.Separator(self).pack(fill=tk.X, expand=False)

        self.bottom_frame.pack(fill=tk.X, expand=True)

        # Populate Top Frame
        ttk.Label(self.top_frame, text="Tasks", anchor=tk.CENTER).grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(self.top_frame, text="Filter: ", anchor=tk.E).grid(row=1, column=0, sticky="e")

        self.filter = tk.StringVar()
        self.filter.set("Default")
        self.filter.trace("w", self.change_filter)

        self.filter_dropdown = ttk.Combobox(self.top_frame,
                                            textvariable=self.filter,
                                            state="readonly",
                                            values=["Default", "Bugged", "Uncompleted", "I Completed"])
        self.filter_dropdown.grid(row=1, column=1, sticky="w")

        # Populate Mid Frame

        # Populate Bottom Frame
        self.add_group_button = ttk.Button(self.bottom_frame, text="New Group", command=self.add_group)
        self.add_group_button.grid(row=0, column=0, sticky=tk.W)

        self.group_name = tk.StringVar()
        self.group_name.set("Group Name")

        self.group_entry = ttk.Entry(self.bottom_frame, textvariable=self.group_name)
        self.group_entry.grid(row=0, column=1, sticky=tk.E)

    @staticmethod
    def create_group_frame():
        pass

    @staticmethod
    def create_task_frame():
        pass

    def change_filter(self):
        pass

    def delete_group(self):
        pass

    def delete_task(self):
        pass

    def add_task(self):
        pass

    def add_group(self):
        pass


class NewTaskFrame(SubFrame):
    def __init__(self, master):
        super().__init__(master)


class NewCheckListFrame(SubFrame):
    def __init__(self, master):
        super().__init__(master)
