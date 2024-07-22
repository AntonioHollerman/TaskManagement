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
        self.acc_id = -1
        self.current_frame = SIGN_IN_FRAME

        # Initializing values
        self.active_frame: SubFrame = SignInFrame(self)
        self.active_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.filter = "Default"

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def swap_frames(self, to_frame, **params):
        if to_frame == SIGN_IN_FRAME:
            self.active_frame.destroy()
            self.active_frame = SignInFrame(self)
            self.active_frame.grid(row=0, column=0, sticky=tk.NSEW)
        elif to_frame == NEW_ACCOUNT_FRAME:
            self.active_frame.destroy()
            self.active_frame = NewAccountFrame(self)
            self.active_frame.grid(row=0, column=0, sticky=tk.NSEW)
        elif to_frame == TASKS_FRAME:
            self.active_frame.destroy()
            self.active_frame = TasksFrame(self)
            self.active_frame.grid(row=0, column=0, sticky=tk.NSEW)
        elif to_frame == NEW_TASK_FRAME:
            self.active_frame.destroy()
            self.active_frame = NewTaskFrame(self, group_name=params["group_name"])
            self.active_frame.grid(row=0, column=0, sticky=tk.NSEW)
        elif to_frame == NEW_CHECKLIST_FRAME:
            self.active_frame.destroy()
            self.active_frame = NewCheckListFrame(self)
            self.active_frame.grid(row=0, column=0, sticky=tk.NSEW)
        else:
            raise RuntimeError("Incorrect 'to_frame' param provided")


class SubFrame(ttk.Frame):
    def __init__(self, master: MasterWindow):
        super().__init__(master)
        self.master: MasterWindow = master


class SignInFrame(SubFrame):
    def __init__(self, master):
        super().__init__(master)

        # Frame title
        self.logger = tk.StringVar()
        self.logger.set("Sign In")
        ttk.Label(self, textvariable=self.logger).grid(row=0, column=1)
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
        if not self.acc_selected.get() == "":
            self.master.current_acc = self.acc_selected.get()
            self.master.swap_frames(TASKS_FRAME)
        else:
            self.logger.set("Invalid Account Selected")


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

        # Adding weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def back(self):
        self.master.swap_frames(SIGN_IN_FRAME)

    def add_acc(self):
        if self.acc_name.get() not in [acc.name for acc in get_all_accounts()]:
            insert_account(self.acc_name.get())
            self.master.swap_frames(SIGN_IN_FRAME)


class TasksFrame(SubFrame):
    def __init__(self, master):
        super().__init__(master)
        filter_modes = ["Default", "Bugged", "Uncompleted", "I Completed"]
        self.current_groups = get_all_group_names()
        assert self.master.filter in filter_modes

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
        self.logger = tk.StringVar()
        self.logger.set("Tasks")
        ttk.Label(self.top_frame, textvariable=self.logger, anchor=tk.CENTER).grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(self.top_frame, text="Filter: ", anchor=tk.E).grid(row=1, column=0, sticky="e")

        self.tk_filter = tk.StringVar()
        self.tk_filter.set(self.master.filter)
        self.tk_filter.trace("w", self.change_filter)

        self.filter_dropdown = ttk.Combobox(self.top_frame,
                                            textvariable=self.tk_filter,
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

        for group_name in self.current_groups:
            self.create_group_frame(self.mid_frame, group_name).pack(fill=tk.BOTH, expand=True)

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
        mode = self.tk_filter.get()

        # Helper functions
        def convert(task: TaskRow, items: List[str] = None) -> FilteredRow:
            return FilteredRow(
                task.id,
                task.name,
                task.group_name,
                task.bugged,
                get_check_list(task.id).items if items is None else items
            )

        # Different modes -> ["Default", "Bugged", "Uncompleted", "I Completed"]
        if mode == "Default":
            filtered_tasks = [convert(task) for task in get_all_tasks_by_group(group_name)]
        elif mode == "Bugged":
            filtered_tasks = [convert(task) for task in get_all_tasks_by_group_and_bugged(group_name)]
        elif mode == "Uncompleted":
            # Dictionary contain a task id to filtered items completed pairs
            task_ids_dict = dict()
            for uncompleted_task in filter_all_not_completed_task_items_by_group(group_name):
                if uncompleted_task.task_id in task_ids_dict.keys():
                    task_ids_dict[uncompleted_task.task_id].append(uncompleted_task.item_name)
                else:
                    task_ids_dict[uncompleted_task.task_id] = [uncompleted_task.item_name]

            # Iterating over dictionary to convert pairs
            filtered_tasks = [convert(get_task(task_id), completed_items) for task_id, completed_items in
                              task_ids_dict.items()]
        elif mode == "I Completed":
            # Dictionary contain a task id to filtered items completed pairs
            task_ids_dict = dict()
            for task_completed in filter_by_acc_group_and_completed(group_name, self.master.acc_id):
                if task_completed.task_id in task_ids_dict.keys():
                    task_ids_dict[task_completed.task_id].append(task_completed.item_name)
                else:
                    task_ids_dict[task_completed.task_id] = [task_completed.item_name]

            # Iterating over dictionary to convert pairs
            filtered_tasks = [convert(get_task(task_id), completed_items) for task_id, completed_items in
                              task_ids_dict.items()]
        else:
            self.master.destroy()
            raise RuntimeError("Invalid mode passed")
        return filtered_tasks

    def create_group_frame(self, parent: ctk.CTkScrollableFrame, group_name: str, empty_group: bool = False) \
            -> ttk.Frame:
        # Filter tasks but setting
        filtered_tasks: List[FilteredRow] = self.filter_tasks(group_name)
        if len(filtered_tasks) == 0 and not empty_group:
            return ttk.Frame(parent)

        # Creating master Frame
        group_frame = ttk.Frame(parent)
        top_frame = ttk.Frame(group_frame)
        mid_frame = ttk.Frame(group_frame)
        bottom_frame = ttk.Frame(group_frame)

        # Packing Frames
        top_frame.pack(fill=tk.X, expand=True)
        ttk.Separator(group_frame).pack(fill=tk.X, expand=True)
        mid_frame.pack(fill=tk.BOTH, expand=True)
        bottom_frame.pack(fill=tk.X, expand=True)

        # Populate Top Frame
        ttk.Label(top_frame, text=group_name, anchor=tk.CENTER).grid(row=0, column=0, sticky=tk.W)
        delete_button = ttk.Button(top_frame, text="DELETE",
                                   command=self.delete_group_frame(group_frame, group_name))
        delete_button.grid(row=0, column=1, sticky=tk.E)

        top_frame.rowconfigure(0, weight=1)
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(0, weight=1)

        # Populate Middle Frame
        for task in filtered_tasks:
            self.create_task_frame(mid_frame, task).pack(fill=tk.BOTH, expand=True)

        # Populate Bottom Frame
        add_task_button = ttk.Button(bottom_frame, text="Add Task", command=self.add_task(group_name))
        add_task_button.grid(row=0, column=0)

        bottom_frame.rowconfigure(0, weight=1)
        bottom_frame.columnconfigure(0, weight=1)
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

        # Creating Weights
        task_frame.rowconfigure(0, weight=1)
        task_frame.rowconfigure(1, weight=1)

        task_frame.columnconfigure(0, weight=1)
        task_frame.columnconfigure(1, weight=1)

        # Looping through items for each task
        for index, item_name in enumerate(get_check_list(task.items_filtered)):
            # Tracks if item is checked or un checked
            var = tk.StringVar()
            var.set("Completed" if task_item_completed(TaskItem(task.id, task.name, task.group_name, item_name))
                    else "Not Completed")
            var.trace("w", self.box_value_changed(var, task.id, item_name))
            self.item_vars.append(var)

            # Displays check box
            check_box = ttk.Checkbutton(task_frame, variable=var, text=item_name, onvalue="Completed",
                                        offvalue="Not Completed")
            check_box.grid(row=2+index, column=1, sticky="nw")
            task_frame.rowconfigure(2+index, weight=1)
            self.check_boxes.append(check_box)

        return task_frame

    def box_value_changed(self, box_status: tk.StringVar, task_id: int, item_name):
        def to_return():
            if box_status.get() == "Completed":
                insert_completed_task(self.master.acc_id, task_id, item_name, datetime.datetime.now())
            else:
                delete_completed_task_item(task_id, item_name)
        return to_return

    def change_filter(self):
        self.master.filter = self.tk_filter.get()
        self.master.swap_frames(TASKS_FRAME)

    def delete_group_frame(self, group_frame: ttk.Frame, group_name):
        def to_return():
            self.current_groups.remove(group_name)
            delete_group(group_name)
            group_frame.destroy()
        return to_return

    @staticmethod
    def delete_task_frame(task_frame: ttk.Frame, task_id):
        def to_return():
            delete_task(task_id)
            task_frame.destroy()
        return to_return

    @staticmethod
    def change_bug_state(task_id: int, bug_state: tk.StringVar):
        def to_return():
            update_bug_state(task_id, bug_state.get())
        return to_return

    def add_task(self, group_name: str):
        def to_return():
            self.master.swap_frames(NEW_TASK_FRAME, group_name=group_name)
        return to_return

    def add_group(self):
        if self.group_name.get() not in self.current_groups:
            (self.create_group_frame(self.mid_frame, self.group_name.get(), True)
             .pack(fill=tk.BOTH, expand=True))
            self.current_groups.append(self.group_name.get())
        else:
            self.logger.set("Group already exist")


class NewTaskFrame(SubFrame):
    def __init__(self, master, group_name: str):
        super().__init__(master)
        self.group_name = group_name

        # Creating labels
        self.logger = tk.StringVar()
        self.logger.set("Add Task")
        title_label = ttk.Label(self, textvariable=self.logger, anchor=tk.CENTER)
        title_label.grid(row=0, column=0, columnspan=3, sticky=tk.EW)

        sub_title = ttk.Label(self, text=f'Adding task to "{group_name}" group', anchor=tk.CENTER)
        sub_title.grid(row=1, column=0, columnspan=3, sticky=tk.EW)

        check_list_label = ttk.Label(self, text="Check List: ", anchor=tk.E)
        check_list_label.grid(row=2, column=1, sticky=tk.E)

        task_name_label = ttk.Label(self, text="Task Name: ", anchor=tk.E)
        task_name_label.grid(row=3, column=1, sticky=tk.E)

        # Create entries
        self.cl_var = tk.StringVar()
        self.cl_dropbox = ttk.Combobox(self,
                                       textvariable=self.cl_var,
                                       state="readonly",
                                       values=[cl.name for cl in get_all_check_lists()])
        self.cl_dropbox.grid(row=2, column=2, sticky=tk.W)

        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self, textvariable=self.name_var)
        self.name_entry.grid(row=3, column=2, sticky=tk.W)

        # Seperator
        ttk.Separator(self).grid(row=4, column=0, columnspan=3)

        # Creating buttons
        self.back_button = ttk.Button(self, text="<- Back", command=self.back)
        self.new_cl_button = ttk.Button(self, text="New Check List", command=self.create_cl)
        self.add_task_button = ttk.Button(self, text="Add Task", command=self.commit_task)

        self.back_button.grid(row=5, column=0, sticky=tk.W)
        self.new_cl_button.grid(row=5, column=1)
        self.add_task_button.grid(row=5, column=2, sticky=tk.E)

        # Adding weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def back(self):
        self.master.swap_frames(TASKS_FRAME)

    def create_cl(self):
        self.master.swap_frames(NEW_CHECKLIST_FRAME)

    def commit_task(self):
        if self.name_var.get() != "":
            insert_task(
                get_cl_id(self.cl_var.get()),
                self.name_var.get(),
                self.group_name,
                False
            )
            self.master.swap_frames(TASKS_FRAME)
        else:
            self.logger.set("Invalid Check List")


class NewCheckListFrame(SubFrame):
    def __init__(self, master):
        super().__init__(master)

        self.top_frame = ttk.Frame(self)
        self.items_frame = ctk.CTkScrollableFrame(self)
        self.bottom_from = ttk.Frame(self)

        # Populate top frame
        self.logger = tk.StringVar()
        self.logger.set("Add Check List")
        title_label = ttk.Label(self.top_frame, textvariable=self.logger, anchor=tk.CENTER)
        title_label.grid(row=0, column=0, columnspan=3, sticky=tk.EW)

        name_label = ttk.Label(self.top_frame, text="Set Name: ", anchor=tk.E)
        name_label.grid(row=1, column=0, columnspan=2, sticky=tk.E)

        list_label = ttk.Label(self.top_frame, text="List Items", anchor=tk.CENTER)
        list_label.grid(row=2, column=0, columnspan=2, sticky=tk.EW)

        self.name_var = tk.StringVar()
        self.name_var.set("Check List Name")
        self.name_entry = ttk.Entry(self.top_frame, textvariable=self.name_var)
        self.name_entry.grid(row=1, column=2, sticky=tk.EW)

        # Populate Items Frame
        self.item_name_vars: List[tk.StringVar | None] = []
        self.item_frames: List[ttk.Frame] = []
        self.next_index = 0

        # Populate Bottom Frame
        self.back_button = ttk.Button(self.bottom_from, text="<- Back", command=self.back)
        self.add_item_button = ttk.Button(self.bottom_from, text="Add Item", command=self.create_item_frame)
        self.create_cl_button = ttk.Button(self.bottom_from, text="Create Check List", command=self.creat_cl)

        self.back_button.grid(row=0, column=0, sticky=tk.E)
        self.add_item_button.grid(row=0, column=1)
        self.create_cl_button.grid(row=0, column=2, sticky=tk.W)

        # Packing Frames
        self.top_frame.pack(fill=tk.X, expand=True)
        self.items_frame.pack(fill=tk.BOTH, expand=True)
        self.bottom_from.pack(fill=tk.X, expand=True)

        # Adding weights
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)

    def back(self):
        self.master.swap_frames(NEW_TASK_FRAME)

    def create_item_frame(self):
        item_frame = ttk.Frame(self.items_frame)

        # Create delete button
        delete_button = ttk.Button(item_frame, text="X", command=self.delete_item_frame(self.next_index))
        self.next_index += 1
        delete_button.grid(row=0, column=0, sticky=tk.E)

        # Label
        ttk.Label(item_frame, text="Item Name: ", anchor=tk.E).grid(row=0, column=1, sticky=tk.E)

        # Name Entry
        name_var = tk.StringVar()
        name_entry = ttk.Entry(item_frame, textvariable=name_var)
        name_entry.grid(row=0, column=2, sticky=tk.W)

        # Separator
        ttk.Separator(item_frame).grid(row=0, column=0, columnspan=3, sticky=tk.EW)

        # Add frame
        item_frame.pack(fill=tk.X, expand=True)
        self.item_name_vars.append(name_var)
        self.item_frames.append(item_frame)

    def creat_cl(self):
        cl_items: Set[str] = {item.get() for item in [var for var in self.item_name_vars if var is not None] if "," not in item.get()}
        if "" in cl_items:
            self.logger.set("No empty tasks")
        elif self.name_var.get() == "" or self.name_var.get() in [cl.name for cl in get_all_check_lists()]:
            self.logger.set("Invalid Check List name")
        elif len(cl_items) == 0:
            self.logger.set("No valid tasks spotted")
        else:
            insert_cl(self.name_var.get(), cl_items)
            self.master.swap_frames(NEW_TASK_FRAME)

    def delete_item_frame(self, index: int):
        def to_return():
            self.item_frames[index].destroy()
            self.item_name_vars[index] = None
        return to_return
