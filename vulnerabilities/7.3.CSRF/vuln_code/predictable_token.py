from flask import Flask, request, redirect, session
from common_db import current_user, apply_transfer, render_layout

app = Flask(__name__)
app.secret_key = "dev-secret"

def make_token():
    user_id = session.get("user_id", 1)
    raw = f"csrf:{user_id}:transfer"
    return hashlib.md5(raw.encode()).hexdigest()

@app.route("/")
def index():
    current_user()
    token = make_token()
    content = f"""
    <h2>Transfer money</h2>
    <form method="post" action="/transfer">
        <input type="hidden" name="csrf_token" value="{token}">
        <input name="to" value="wiener">
        <input name="amount" value="50">
        <button>Transfer</button>
    </form>
    """
    return render_layout("CSRF lab 3: predictable token", content)

@app.route("/transfer", methods=["POST"])
def transfer():
    token = request.form.get("csrf_token", "")
    if token != make_token():
        return "Bad CSRF token", 403

    to_username = request.form.get("to", "wiener")
    amount = request.form.get("amount", "10")
    apply_transfer(to_username, amount)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
