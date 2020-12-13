import sqlite3
import numpy as np


def execute_query(query):
    """
    Returns all courses that match the identifier entered in the query
    """
    #Fetching professor from course acc to query - checks for substring
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    if (query[0:6].lower() == "select"):
        return cursor.fetchall()
    else:
        return False
