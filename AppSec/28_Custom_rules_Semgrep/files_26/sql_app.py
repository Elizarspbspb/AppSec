import sqlite3
from typing import List, Tuple, Optional


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect("app.db")
    return conn


def unsafe_get_user_by_id(user_id: str) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT id, username, email FROM users WHERE id = " + user_id
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    return row


def unsafe_search_users(term: str) -> List[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT id, username, email FROM users WHERE username LIKE '%" + term + "%'"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


def unsafe_login(username: str, password: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    query = (
        "SELECT id FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "'"
    )
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    return row is not None


def unsafe_get_orders_for_user(user_id: str) -> List[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    query = f"SELECT id, total FROM orders WHERE user_id = {user_id}"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


def safe_get_user_by_id(user_id: int) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT id, username, email FROM users WHERE id = ?"
    cur.execute(query, (user_id,))
    row = cur.fetchone()
    conn.close()
    return row


def safe_search_users(term: str) -> List[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT id, username, email FROM users WHERE username LIKE ?"
    pattern = "%" + term + "%"
    cur.execute(query, (pattern,))
    rows = cur.fetchall()
    conn.close()
    return rows


def safe_login(username: str, password: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT id FROM users WHERE username = ? AND password = ?"
    cur.execute(query, (username, password))
    row = cur.fetchone()
    conn.close()
    return row is not None


def get_user_statistics(limit: str) -> List[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    query = (
        "SELECT username, COUNT(orders.id) "
        "FROM users LEFT JOIN orders ON users.id = orders.user_id "
        "GROUP BY users.id "
        "ORDER BY COUNT(orders.id) DESC "
        "LIMIT " + limit
    )
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


def safe_get_user_statistics(limit: int) -> List[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    query = (
        "SELECT username, COUNT(orders.id) "
        "FROM users LEFT JOIN orders ON users.id = orders.user_id "
        "GROUP BY users.id "
        "ORDER BY COUNT(orders.id) DESC "
        "LIMIT ?"
    )
    cur.execute(query, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
