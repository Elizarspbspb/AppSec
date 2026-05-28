import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "labdb")
DB_USER = os.getenv("DB_USER", "labuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "labpass")

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def ensure_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        )
        """
    )
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM notes")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute(
            "INSERT INTO notes (title, body) VALUES (%s, %s)",
            ("Привет из БД", "Это первая запись в таблице notes."),
        )
        conn.commit()
    cur.close()
    conn.close()


@app.route("/", methods=["GET"])
def index():
    error = None
    notes = []
    try:
        ensure_db()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, body FROM notes ORDER BY id ASC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        notes = rows
    except Exception as e:
        error = str(e)
    return render_template("index.html", notes=notes, error=error)


@app.route("/add", methods=["POST"])
def add_note():
    title = request.form.get("title") or "Без названия"
    body = request.form.get("body") or ""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notes (title, body) VALUES (%s, %s)",
        (title, body),
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
