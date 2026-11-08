from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h1>Search</h1>
    <form action="/search">
        <input name="q" placeholder="Search text">
        <button>Search</button>
    </form>
    """

@app.route("/search")
def search():
    # Валидация - проверка типа данных
    # Экранирование - когда есть JS код
    # Санитизация - когда от пользователя нужны html символы
    # Кодирование - изменение представления символов
    q = request.args.get("q", "")
    html_vuln = f"""
    <h1>Search results</h1>
    <p>You searched for: {q}</p>
    <p>No results found.</p>
    <a href="/">Back</a>
    """
    # Экранирование - самый безопасный. Шаблонизатор Jinja
    # HTML-кодирование
    html_vuln = f"""
    <h1>Search results</h1>
    <p>You searched for: {q}</p>
    <p>No results found.</p>
    <a href="/">Back</a>
    """
    return html