import sqlite3
import os

def get_db_connection():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(project_dir, ".."))
    db_path = os.path.join(project_dir, "cooking.sqlite")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn