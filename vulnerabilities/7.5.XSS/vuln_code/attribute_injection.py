from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    next_url = request.args.get("next", "/profile")
    label = request.args.get("label", "Continue")

    return f"""
    <h1>Redirect page</h1>
    <p>Click the link to continue.</p>
    <a class="button" href="{next_url}">{label}</a>
    """

@app.route("/profile")
def profile():
    avatar = request.args.get("avatar", "https://example.com/avatar.png")

    return f"""
    <h1>Profile</h1>
    <img src="{avatar}" alt="User avatar" width="120">
    <p>Demo profile page</p>
    """

