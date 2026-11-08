from flask import Flask, request, redirect
from common_db import current_user, apply_transfer, render_layout

app = Flask(__name__)
app.secret_key = "dev-secret"

@app.route("/")
def index():
    current_user()
    content = """
    <h2>Transfer money</h2>
    <form method="post" action="/transfer">
        <input name="to" value="wiener">
        <input name="amount" value="50">
        <button>Transfer</button>
    </form>
    """
    return render_layout("CSRF lab 1: no token", content)

@app.route("/transfer", methods=["POST"])
def transfer():
    to_username = request.form.get("to", "wiener")
    amount = request.form.get("amount", "10")
    apply_transfer(to_username, amount)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

