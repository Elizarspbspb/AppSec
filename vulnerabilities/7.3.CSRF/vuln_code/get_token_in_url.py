from flask import Flask, request, redirect, session
from common_db import current_user, change_email, render_layout

app = Flask(__name__)
app.secret_key = "dev-secret"

def get_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]

@app.route("/")
def index():
    current_user()
    token = get_token()
    content = f"""
    <h2>Change email</h2>
    <form method="get" action="/change-email">
        <input type="hidden" name="csrf_token" value="{token}">
        <input name="email" value="new@example.com">
        <button>Change email</button>
    </form>
    """
    return render_layout("CSRF lab 6: token in URL", content)

@app.route("/change-email", methods=["GET"])
def change_email_route():
    token = request.args.get("csrf_token", "")
    if token != get_token():
        return "Bad CSRF token", 403

    email = request.args.get("email", "new@example.com")
    change_email(email)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
