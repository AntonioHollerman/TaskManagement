import sqlite3 as sql
from table_records import *
from typing import List, Set
import datetime

# Creates / Connect to database
conn = sql.connect('TasksManager.db')
cur = conn.cursor()


def create_tables():
    """
    Initialize database with empty tables
    :return: None
    """
    cur.execute("""CREATE TABLE IF NOT EXISTS accounts(
    id INTEGER PRIMARY KEY,
    name TEXT
);
CREATE TABLE IF NOT EXISTS check_lists(
    id INTEGER PRIMARY KEY,
    items TEXT
);
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY,
    cl_id INTEGER,
    group_name TEXT,
    bugged TEXT,
    FOREIGN KEY (cl_id) REFERENCES check_lists(id)
);
CREATE TABLE IF NOT EXISTS tasks_completed(
    acc_id INTEGER,
    task_id INTEGER,
    item_name TEXT,
    date_completed TEXT,
    FOREIGN KEY (acc_id) REFERENCES accounts(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);""")


def get_all_accounts() -> List[AccountRow]:
    cur.execute("SELECT * FROM accounts")

    accounts: List[AccountRow] = []
    for acc_id, name in cur.fetchall():
        accounts.append(AccountRow(
            int(acc_id),
            name
        ))
    return accounts


def get_all_check_lists() -> List[CheckListRow]:
    cur.execute("SELECT * FROM check_lists")

    check_lists: List[CheckListRow] = []
    for cl_id, name, items in cur.fetchall():
        check_lists.append(CheckListRow(
            int(cl_id),
            name,
            items.split(", ")
        ))
    return check_lists


# Getting by id
def get_account(acc_id: int) -> AccountRow:
    cur.execute("SELECT * FROM accounts WHERE id = ?", (acc_id,))
    _, name = cur.fetchone()
    return AccountRow(
        acc_id,
        name
    )


def get_check_list(cl_id: int) -> CheckListRow:
    cur.execute(f"SELECT * FROM check_lists WHERE id = {cl_id}")
    _, name, items = cur.fetchone()
    return CheckListRow(
            cl_id,
            name,
            items.split(", ")
        )


def get_task(task_id: int) -> TaskRow:
    cur.execute("SELECT id, cl_id, name, group_name, bugged FROM tasks WHERE id = ?", (task_id,))
    _, cl_id, name, group_name, bugged = cur.fetchone()
    return TaskRow(
            task_id,
            int(cl_id),
            name,
            group_name,
            "true" == bugged.lower()
        )


def get_all_tasks() -> List[TaskRow]:
    cur.execute("SELECT * FROM tasks")

    tasks: List[TaskRow] = []
    for task_id, cl_id, name, group_name, bugged in cur.fetchall():
        tasks.append(TaskRow(
            int(task_id),
            int(cl_id),
            name,
            group_name,
            "true" == bugged.lower()
        ))
    return tasks


def get_all_tasks_by_group(group_name: str) -> List[TaskRow]:
    cur.execute(f"SELECT * FROM tasks WHERE group_name = '{group_name}'")

    tasks: List[TaskRow] = []
    for task_id, cl_id, name, group_name, bugged in cur.fetchall():
        tasks.append(TaskRow(
            int(task_id),
            int(cl_id),
            name,
            group_name,
            "true" == bugged.lower()
        ))
    return tasks


def get_all_tasks_by_group_and_bugged(group_name: str) -> List[TaskRow]:
    cur.execute(f"SELECT * FROM tasks "
                f"WHERE group_name = '?' AND bugged = 'true'", (group_name,))

    tasks: List[TaskRow] = []
    for task_id, cl_id, name, group_name, bugged in cur.fetchall():
        tasks.append(TaskRow(
            int(task_id),
            int(cl_id),
            name,
            group_name,
            "true" == bugged.lower()
        ))
    return tasks


def filter_by_acc_group_and_completed(group_name, acc_id) -> List[TaskCompletedRow]:
    cur.execute(f"""
    SELECT tc.acc_id, tc.task_id, tc.item_name, tc.date_completed FROM tasks_completed AS tc
    INNER JOIN tasks AS t
        on t.id = tc.task_id
    INNER JOIN accounts AS a 
        on tc.acc_id = a.id
    WHERE t.group_name = ? AND a.id = ?""", (group_name, acc_id))

    completed: List[TaskCompletedRow] = []
    for acc_id, task_id, item_name, date_completed in cur.fetchall():
        month, day, year = date_completed.split("/")
        completed.append(TaskCompletedRow(
            int(acc_id),
            int(task_id),
            item_name,
            datetime.date(
                int(year),
                int(month),
                int(day)
            )
        ))
    return completed


def get_all_completed_task_items() -> List[TaskItem]:
    cur.execute("SELECT t.id, t.name, t.group_name, tc.item_name FROM tasks_completed AS tc "
                "INNER JOIN tasks AS t ON t.id = tc.task_id")

    completed: List[TaskItem] = []
    for task_id, task_name, group_name, item_name in cur.fetchall():
        completed.append(TaskItem(
            int(task_id),
            task_name,
            group_name,
            item_name
        ))
    return completed


def filter_all_completed_task_items_by_group(group_name: str) -> List[TaskItem]:
    cur.execute("SELECT t.id, t.name, t.group_name, tc.item_name FROM tasks_completed AS tc "
                "INNER JOIN tasks AS t ON t.id = tc.task_id"
                "WHERE t.group_name = ?", (group_name,))

    completed: List[TaskItem] = []
    for task_id, task_name, group_name, item_name in cur.fetchall():
        completed.append(TaskItem(
            int(task_id),
            task_name,
            group_name,
            item_name
        ))
    return completed


def get_all_task_items() -> List[TaskItem]:
    cur.execute("""
SELECT t.id, t.name, t.group_name, items FROM tasks AS t 
INNER JOIN check_lists cl
    on cl.id = t.cl_id;""")
    task_items: List[TaskItem] = []

    for task_id, name, group_name, items in cur.fetchall():
        for item in items.split(", "):
            task_items.append(TaskItem(
                int(task_id),
                name,
                group_name,
                item
            ))

    return task_items


def filter_all_task_items_by_group(group_name: str) -> List[TaskItem]:
    cur.execute("""
SELECT t.id, t.name, t.group_name, items FROM tasks AS t 
INNER JOIN check_lists cl
    on cl.id = t.cl_id
WHERE t.group_name = ?;""", (group_name,))
    task_items: List[TaskItem] = []

    for task_id, name, group_name, items in cur.fetchall():
        for item in items.split(", "):
            task_items.append(TaskItem(
                int(task_id),
                name,
                group_name,
                item
            ))

    return task_items


def get_all_not_completed_task_items() -> List[TaskItem]:
    all_tasks = set(get_all_task_items())
    completed_tasks = set(get_all_completed_task_items())
    return list(all_tasks.difference(completed_tasks))


def get_cl_id(cl_name):
    cur.execute("SELECT id FROM check_lists WHERE name = ?", (cl_name,))
    return cur.fetchone()[0]


def filter_all_not_completed_task_items_by_group(group_name: str) -> List[TaskItem]:
    all_group_tasks = set(filter_all_task_items_by_group(group_name))
    all_completed_group_tasks = set(filter_all_completed_task_items_by_group(group_name))
    return list(all_group_tasks.difference(all_completed_group_tasks))


def get_all_completed_tasks_by_name(name: str) -> List[TaskItem]:
    cur.execute(f"""
SELECT t.id, t.name, t.group_name, tc.item_name FROM tasks_completed as tc
INNER JOIN tasks t
    on t.id = tc.task_id
INNER JOIN accounts a 
    on tc.acc_id = a.id
WHERE a.name = '{name}'""")
    tasks_completed: List[TaskItem] = []

    for task_id, task_name, group_name, item in cur.fetchall():
        tasks_completed.append(TaskItem(
            int(task_id),
            task_name,
            group_name,
            item
        ))

    return tasks_completed


def get_all_group_names() -> List[str]:
    cur.execute("SELECT DISTINCT group_name FROM tasks")
    return [row[0] for row in cur.fetchall()]


def task_item_completed(task_item: TaskItem) -> bool:
    return task_item in get_all_completed_task_items()


def insert_account(name: str):
    cur.execute(
        "INSERT INTO accounts (name) "
        f"VALUES ('{name}')"
    )


def insert_cl(name: str, items: Set[str]):
    cur.execute(
        "INSERT INTO check_lists (name, items) "
        f"VALUES (?, ?)",
        (name, ", ".join(items))
    )
    

def insert_task(cl_id: int, name: str, group_name: str, bugged: bool):
    cur.execute(
        "INSERT INTO tasks (cl_id, name, group_name, bugged) "
        f"VALUES ({cl_id}, '{name}', '{group_name}', '{bugged}')"
    )
    

def update_bug_state(task_id: int, state: str):
    assert state == "Bugged" or state == "Not Bugged"
    cur.execute("UPDATE tasks SET bugged = ? WHERE id = ?", (state, task_id))


def insert_completed_task(acc_id: int, task_id: int, item_name: str, date_completed: datetime.date):
    date_formatted = f"{date_completed.month:02d}/{date_completed.day:02d}/{date_completed.year}"
    cur.execute(
        "INSERT INTO tasks_completed (acc_id, task_id, item_name, date_completed) "
        f"VALUES (?, ?, ?, ?)",
        (acc_id, task_id, item_name, date_formatted)
    )


def delete_acc(acc_id: int):
    cur.execute(f"""
DELETE FROM accounts
WHERE id = ?""",
                (acc_id,))


def delete_task(task_id: int):
    cur.execute(f"""
DELETE FROM tasks
WHERE id = ?""",
                (task_id,))


def delete_group(group_name: str):
    cur.execute(f"""
DELETE FROM tasks
WHERE group_name = ? """,
                (group_name,))


def delete_completed_task_item(task_id: int, item_name: str):
    cur.execute(f"""
DELETE FROM tasks_completed
WHERE task_id = ? AND item_name = ?""",
                (task_id, item_name))
