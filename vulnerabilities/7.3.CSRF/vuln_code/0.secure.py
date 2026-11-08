import hmac
from flask import Flask, request, redirect, session
from common_db import current_user, apply_transfer, change_email, render_layout

app = Flask(__name__)
app.secret_key = "replace-with-real-random-secret"

def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]

def validate_csrf():
    expected = session.get("csrf_token", "")
    submitted = request.form.get("csrf_token", "")
    return bool(expected) and hmac.compare_digest(expected, submitted)

@app.route("/")
def index():
    current_user()
    token = csrf_token()
    content = f"""
    <h2>Transfer money</h2>
    <form method="post" action="/transfer">
        <input type="hidden" name="csrf_token" value="{token}">
        <input name="to" value="wiener">
        <input name="amount" value="50">
        <button>Transfer</button>
    </form>

    <h2>Change email</h2>
    <form method="post" action="/change-email">
        <input type="hidden" name="csrf_token" value="{token}">
        <input name="email" value="new@example.com">
        <button>Change email</button>
    </form>

    <p>Secure baseline: random session-bound token, POST for state changes, constant-time comparison.</p>
    """
    return render_layout("Secure CSRF version", content)

@app.route("/transfer", methods=["POST"])
def transfer():
    if not validate_csrf():
        return "Bad CSRF token", 403

    to_username = request.form.get("to", "wiener")
    amount = request.form.get("amount", "10")
    apply_transfer(to_username, amount)
    return redirect("/")

@app.route("/change-email", methods=["POST"])
def change_email_route():
    if not validate_csrf():
        return "Bad CSRF token", 403

    email = request.form.get("email", "new@example.com")
    change_email(email)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

