from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    nickname = request.args.get("nickname", "guest")
    banner = request.args.get("banner", "Welcome to the lab")

    template = """
    <h1>User dashboard</h1>
    <p>Hello, {{ nickname|safe }}</p>
    <div class="banner">{{ banner|safe }}</div>
    """

    return render_template_string(template, nickname=nickname, banner=banner)

