import sqlite3 as sql
from table_records import *
from typing import List
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
    conn.commit()


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


def get_all_completed_tasks() -> List[TaskCompletedRow]:
    cur.execute("SELECT * FROM tasks_completed")

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
