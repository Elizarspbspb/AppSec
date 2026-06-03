import sqlite3


def search_user_by_name(name):
    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    query = "SELECT id, username FROM users WHERE username = '" + name + "'"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows
