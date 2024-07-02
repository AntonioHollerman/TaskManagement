from collections import namedtuple

# Named tuples that represent rows for each table
AccountRow = namedtuple("AccountRow", [
    "id",
    "name"
])

CheckListRow = namedtuple("CheckListRow", [
    "id",
    "name",
    "items"
])

TaskRow = namedtuple("TaskRow", [
    "id",
    "cl_id",
    "name",
    "group_name",
    "bugged"
])

FilteredRow = namedtuple("FilteredRow", [
    "id",
    "name",
    "group_name",
    "bugged",
    "items_filtered"
])

TaskCompletedRow = namedtuple("TaskCompletedRow", [
    "acc_id",
    "task_id",
    "item_name",
    "date_completed"
])

TaskItem = namedtuple("TaskItem", [
    "task_name",
    "group_name",
    "item_name"
])
