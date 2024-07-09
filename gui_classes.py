import tkinter as tk
from tkinter import ttk
from db_funcs import *
import customtkinter as ctk

# Frame constant values
SIGN_IN_FRAME = "sign in frame"
NEW_ACCOUNT_FRAME = "new account frame"
TASKS_FRAME = "tasks frame"
NEW_TASK_FRAME = "new task frame"
NEW_CHECKLIST_FRAME = "new checklist frame"


class MasterWindow(ctk.CTk):
    def __init__(self, **kwargs):
        # Applying default parameters
        super().__init__(**kwargs)
        ctk.set_appearance_mode("light")
        self.current_acc = None
        self.current_frame = SIGN_IN_FRAME

        # Initializing frame
        self.current_frame: SubFrame = SignInFrame(self)

    def swap_frames(self, to_frame, **params):
        if to_frame == SIGN_IN_FRAME:
            self.current_frame.destroy()
            self.current_frame = SignInFrame(self)
            self.current_frame.grid(row=0, column=0, sticky=tk.NSEW)
        elif to_frame == NEW_ACCOUNT_FRAME:
            self.current_frame.destroy()
            self.current_frame = NewAccountFrame(self)
            self.current_frame.grid(row=0, column=0, sticky=tk.NSEW)
        elif to_frame == TASKS_FRAME:
            self.current_frame.destroy()
            self.current_frame = TasksFrame(self)
            self.current_frame.grid(row=0, column=0, sticky=tk.NSEW)
        elif to_frame == NEW_TASK_FRAME:
            self.current_frame.destroy()
            self.current_frame = NewTaskFrame(self)
            self.current_frame.grid(row=0, column=0, sticky=tk.NSEW)
        elif to_frame == NEW_CHECKLIST_FRAME:
            self.current_frame.destroy()
            self.current_frame = NewCheckListFrame(self)
            self.current_frame.grid(row=0, column=0, sticky=tk.NSEW)
        else:
            raise RuntimeError("Incorrect 'to_frame' param provided")


class SubFrame(ttk.Frame):
    def __init__(self, master: MasterWindow):
        super().__init__(master)
        self.master: MasterWindow = master

    def refresh(self, master: MasterWindow, **params):
        current_sub_class = type(self)
        self.destroy()
        return current_sub_class(master, params)


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
        self.master.swap_frames(NEW_ACCOUNT_FRAME)

    def select_acc(self):
        self.master.current_acc = self.acc_selected.get()
        self.master.swap_frames(TASKS_FRAME)


class NewAccountFrame(SubFrame):
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
        self.master.swap_frames(SIGN_IN_FRAME)

    def add_acc(self):
        if self.acc_name.get() not in [acc.name for acc in get_all_accounts()]:
            insert_account(self.acc_name.get())


class TasksFrame(SubFrame):
    def __init__(self, master, filter_="Default"):
        filter_modes = ["Default", "Bugged", "Uncompleted", "I Completed"]
        assert filter_ in filter_modes
        super().__init__(master)

        # Creating sub frames
        self.top_frame = ttk.Frame(self)
        self.mid_frame = ctk.CTkScrollableFrame(self)
        self.bottom_frame = ttk.Frame(self)

        # Packing the sub frames
        self.top_frame.pack(fill=tk.X, expand=True)
        ttk.Separator(self).pack(fill=tk.X, expand=False)

        self.mid_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Separator(self).pack(fill=tk.X, expand=False)

        self.bottom_frame.pack(fill=tk.X, expand=True)

        # Populate Top Frame
        ttk.Label(self.top_frame, text="Tasks", anchor=tk.CENTER).grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(self.top_frame, text="Filter: ", anchor=tk.E).grid(row=1, column=0, sticky="e")

        self.filter = tk.StringVar()
        self.filter.set(filter_)
        self.filter.trace("w", self.change_filter)

        self.filter_dropdown = ttk.Combobox(self.top_frame,
                                            textvariable=self.filter,
                                            state="readonly",
                                            values=filter_modes)
        self.filter_dropdown.grid(row=1, column=1, sticky="w")

        # Populate Mid Frame
        self.item_vars: List[tk.StringVar] = []
        self.bugged_vars: List[tk.StringVar] = []
        self.check_boxes: List[ttk.Checkbutton] = []
        self.bugged_check_boxes: List[ttk.Checkbutton] = []
        self.delete_buttons: List[ttk.Button] = []
        self.group_delete_buttons: List[ttk.Button] = []

        for group_name in get_all_group_names():
            self.create_group_frame(self.mid_frame, group_name).pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Populate Bottom Frame
        self.add_group_button = ttk.Button(self.bottom_frame, text="New Group", command=self.add_group)
        self.add_group_button.grid(row=0, column=0, sticky=tk.W)

        self.group_name = tk.StringVar()
        self.group_name.set("Group Name")

        self.group_entry = ttk.Entry(self.bottom_frame, textvariable=self.group_name)
        self.group_entry.grid(row=0, column=1, sticky=tk.E)

    def filter_tasks(self, group_name: str) -> List[FilteredRow]:
        # Initialize values
        filtered_tasks: List[FilteredRow] = []
        mode = self.filter.get()

        # Helper functions
        def convert(task: TaskRow) -> FilteredRow:
            return FilteredRow(
                task.id,
                task.name,
                task.group_name,
                task.bugged,
                get_check_list(task.id).items
            )

        # Different modes -> ["Default", "Bugged", "Uncompleted", "I Completed"]
        if mode == "Default":
            filtered_tasks = [convert(task) for task in get_all_tasks_by_group(group_name)]
        elif mode == "Bugged":
            filtered_tasks = [convert(task) for task in get_all_tasks_by_group_and_bugged(group_name)]
        elif mode == "Uncompleted":
            for task in get_all_tasks_by_group(group_name):
                task_converted = convert(task)

        elif mode == "I Completed":
            pass
        else:
            self.master.destroy()
            raise RuntimeError("Invalid mode passed")
        return filtered_tasks

    def create_group_frame(self, parent: ctk.CTkScrollableFrame, group_name: str) -> ttk.Frame:
        # Filter tasks but setting
        filtered_tasks: List[FilteredRow] = self.filter_tasks(group_name)
        if len(filtered_tasks) == 0:
            return ttk.Frame(parent)

        # Creating master Frame
        group_frame = ttk.Frame(parent)
        top_frame = ttk.Frame(group_frame)
        bottom_frame = ttk.Frame(group_frame)

        # Packing Frames
        top_frame.pack(fill=tk.X, expand=True)
        bottom_frame.pack(fill=tk.BOTH, expand=True)

        # Populate Top Frame
        ttk.Label(top_frame, text=group_name, anchor=tk.CENTER).grid(row=0, column=0, sticky=tk.EW)
        delete_button = ttk.Button(top_frame, text="DELETE",
                                   command=TasksFrame.delete_group_frame(group_frame, group_name))
        delete_button.grid(row=0, column=1, sticky=tk.W)

        # Populate Bottom Frame
        for task in filtered_tasks:
            self.create_task_frame(bottom_frame, task).pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        return group_frame

    def create_task_frame(self, parent: ttk.Frame, task: FilteredRow) -> ttk.Frame:
        # Frame to be returned
        task_frame = ttk.Frame(parent)

        # Creating task delete button
        delete_button = ttk.Button(task_frame, text="X", command=TasksFrame.delete_task_frame(task_frame, task.id))
        delete_button.grid(row=0, column=0, sticky="ne")
        self.delete_buttons.append(delete_button)

        # Creating Label for task
        task_label = ttk.Label(task_frame, text=task.name, anchor=tk.CENTER)
        task_label.grid(row=0, column=1, sticky="ew")

        # Creating bugged tab
        bugged_var = tk.StringVar()
        bugged_var.set("Bugged" if task.bugged else "Not Bugged")
        bugged_var.trace("w", TasksFrame.change_bug_state(task.id, bugged_var))
        self.bugged_vars.append(bugged_var)

        bugged_box = ttk.Checkbutton(task_frame, variable=bugged_var, text="Bugged", onvalue="Bugged",
                                     offvalue="Not Bugged")
        bugged_box.grid(row=1, column=1, sticky="nw")
        self.bugged_check_boxes.append(bugged_box)

        # Looping through items for each task
        for index, item_name in enumerate(get_check_list(task.items_filtered)):
            # Tracks if item is checked or un checked
            var = tk.StringVar()
            var.set("Completed" if task_item_completed(TaskItem(task.name, task.group_name, item_name))
                    else "Not Completed")
            var.trace("w", TasksFrame.box_value_changed(var, task.id, item_name))
            self.item_vars.append(var)

            # Displays check box
            check_box = ttk.Checkbutton(task_frame, variable=var, text=item_name, onvalue="Completed",
                                        offvalue="Not Completed")
            check_box.grid(row=2+index, column=1, sticky="nw")
            self.check_boxes.append(check_box)

        return task_frame

    @staticmethod
    def box_value_changed(box_status: tk.StringVar, task_id: int, item_name):
        def to_return():
            pass
        return to_return

    def change_filter(self):
        pass

    @staticmethod
    def delete_group_frame(group_frame: ttk.Frame, group_name):
        def to_return():
            pass
        return to_return

    @staticmethod
    def delete_task_frame(task_frame: ttk.Frame, task_id):
        def to_return():
            pass
        return to_return

    @staticmethod
    def change_bug_state(task_id: int, bug_state: tk.StringVar):
        def to_return():
            pass
        return to_return

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
