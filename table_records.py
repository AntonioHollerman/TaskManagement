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

TaskCompletedRow = namedtuple("TaskCompletedRow", [
    "acc_id",
    "task_id",
    "item_name",
    "date_completed"
])
