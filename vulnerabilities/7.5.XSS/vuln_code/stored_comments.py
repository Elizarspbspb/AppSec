from flask import Flask, request, redirect
from common_db import get_db

app = Flask(__name__)

@app.route("/")
def index():
    conn = get_db()
    comments = conn.execute("SELECT author, body FROM comments ORDER BY id DESC").fetchall()
    conn.close()

    items = ""
    for comment in comments:
        items += f"""
        <div class="comment">
            <strong>{comment['author']}</strong>
            <div>{comment['body']}</div>
        </div>
        """

    return f"""
    <h1>Article</h1>
    <p>This is a training article about web security.</p>

    <h2>Comments</h2>
    {items}
    <h2>Add comment</h2>
    <form method="post" action="/comment">
        <input name="author" placeholder="Name">
        <textarea name="body" placeholder="Comment"></textarea>
        <button>Send</button>
    </form>
    """

@app.route("/comment", methods=["POST"])
def comment():
    author = request.form.get("author", "anonymous")
    body = request.form.get("body", "")
    conn = get_db()
    conn.execute("INSERT INTO comments (author, body) VALUES (?, ?)", (author, body))
    conn.commit()
    conn.close()
    return redirect("/")

