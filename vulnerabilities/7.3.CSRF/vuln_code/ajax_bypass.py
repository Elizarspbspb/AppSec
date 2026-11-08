app.secret_key = "dev-secret"

def get_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]

def csrf_check_skipped():
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"

@app.route("/")
def index():
    current_user()
    token = get_token()
    content = f"""
    <h2>Transfer money</h2>
    <form method="post" action="/transfer">
        <input type="hidden" name="csrf_token" value="{token}">
        <input name="to" value="wiener">
        <input name="amount" value="50">
        <button>Transfer</button>
    </form>
    """

    return render_layout("CSRF lab 8: AJAX bypass", content)

@app.route("/transfer", methods=["POST"])
def transfer():
    if not csrf_check_skipped():
        token = request.form.get("csrf_token", "")
        if token != get_token():
            return "Bad CSRF token", 403

    to_username = request.form.get("to", "wiener")
    amount = request.form.get("amount", "10")
    apply_transfer(to_username, amount)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
