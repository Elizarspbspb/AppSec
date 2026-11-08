from flask import Flask, request, redirect
from common_db import current_user, apply_transfer, render_layout

app = Flask(__name__)
app.secret_key = "dev-secret"

GLOBAL_CSRF_TOKEN = "global-demo-token"

@app.route("/")
def index():
    current_user()
    content = f"""
    <h2>Transfer money</h2>
    <form method="post" action="/transfer">
        <input type="hidden" name="csrf_token" value="{GLOBAL_CSRF_TOKEN}">
        <input name="to" value="wiener">
        <input name="amount" value="50">
        <button>Transfer</button>
    </form>
    """
    return render_layout("CSRF lab 4: global token", content)

@app.route("/transfer", methods=["POST"])
def transfer():
    token = request.form.get("csrf_token", "")
    if token != GLOBAL_CSRF_TOKEN:
        return "Bad CSRF token", 403

    to_username = request.form.get("to", "wiener")
    amount = request.form.get("amount", "10")
    apply_transfer(to_username, amount)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
