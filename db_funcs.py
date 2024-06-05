import sqlite3 as sql
from collections import namedtuple

# Creates / Connect to database
conn = sql.connect('TasksManager.db')
cur = conn.cursor()

# Named tuples that represent rows for each table
AccountRow = namedtuple("AccountRow", [])


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
