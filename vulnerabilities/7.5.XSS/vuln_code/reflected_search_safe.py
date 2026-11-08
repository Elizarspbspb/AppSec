from flask import Flask, request
from flask import render_template,render_template_string   # Jinja экранирует символы

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
    
    # Далее 2 варианта
    # 1 - html шаблон в коде программы
    html = f"""
    <h1>Search results</h1>
    <p>You searched for: {{q}}</p>
    <p>No results found.</p>
    <a href="/">Back</a>
    """
    return render_template_string(html, query=q)
    
    # 2 - html шаблон в отдельном файле search.html
    return render_template("search.html", query=q)
    
# search.html
'''
<h1>Search results</h1>
<!-- Jinja сама сделает кодирование для {{ query }} -->
<p>You searched for: {{ query }}</p>
<p>No results found.</p>
<a href="/">Back</a>
'''