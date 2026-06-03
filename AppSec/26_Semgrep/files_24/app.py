from flask import Flask, request
import sqlite3
import subprocess
import requests
import pickle

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("example.db")
    return conn


@app.route("/user")
def user():
    user_id = request.args.get("id", "")
    conn = get_db()
    cur = conn.cursor()
    query = f"SELECT id, username, email FROM users WHERE id = {user_id}"
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    if not row:
        return "User not found"
    return f"User: {row[1]} ({row[2]})"


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    cmd = f"ping -c 1 {host}"
    subprocess.run(cmd, shell=True)
    return "OK"


@app.route("/load")
def load():
    data = request.args.get("data", "")
    try:
        obj = pickle.loads(bytes.fromhex(data))
    except Exception:
        return "Error"
    return str(obj)


@app.route("/check")
def check():
    url = request.args.get("url", "https://example.com")
    r = requests.get(url, verify=False)
    return f"Status: {r.status_code}"


if __name__ == "__main__":
    app.run(debug=True)
