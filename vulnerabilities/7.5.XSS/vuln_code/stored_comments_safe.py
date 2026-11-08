from flask import Flask, request, redirect, Markup, render_template # Добавили Markup
from common_db import get_db

import html
import bleach # для санитизации в Python

app = Flask(__name__)

@app.route("/")
def index():
    conn = get_db()
    comments = conn.execute("SELECT author, body FROM comments ORDER BY id DESC").fetchall()
    conn.close()

    items = ""
    for comment in comments:
        # 1. HTML-кодирование author
        safe_author = html.escape(comment['author'])
        # Можно доверить шаблонизатору Jinja
        
        # 2. Санитизация для тела комментария 
        # Разрешаем только безопасные теги для изменения шрифта
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'span']
        safe_body = bleach.clean(comment['body'], tags=allowed_tags, strip=True)
        
        # • Если данные — простой текст (никнейм, город, имя): bleach не нужен. 
        # Выводим в Jinja БЕЗ | safe [1.3].
        # • Если данные — HTML-текст (комментарий с форматированием): 
        # Обязательно очищаем через bleach на бэкенде, а в Jinja выводим строго С фильтром | safe [1.3].

        items += f"""
        <div class="comment">
            <strong>{safe_author}</strong>
            <div>{safe_body}</div>
        </div>
        """
        
    # Строка items уже содержит безопасный HTML. Если защищаем сами вручную без шаблонизатора
    safe_items = Markup(items) 

    # если сами защитили, но плохой паттерн
    return f"""
    <h1>Article</h1>
    <p>This is a training article about web security.</p>

    <h2>Comments</h2>
    {safe_items}
    <h2>Add comment</h2>
    <form method="post" action="/comment">
        <input name="author" placeholder="Name">
        <textarea name="body" placeholder="Comment"></textarea>
        <button>Send</button>
    </form>
    """

# Или с шаблонизатором Jinja
@app.route("/")
def index():
    conn = get_db()
    comments = conn.execute("SELECT author, body FROM comments ORDER BY id DESC").fetchall()
    conn.close()
    sanitized_comments = []
    allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'span']
    for comment in comments:
        sanitized_comments.append({
            'author': comment['author'], # Оставляем как есть
            'body': bleach.clean(comment['body'], tags=allowed_tags, strip=True) # Очищаем
        })
    # Отправляем чистые данные в шаблон
    return render_template("index.html", comments=sanitized_comments)

# index.html для Jinja
'''
{% for comment in comments %}
<div class="comment">
    <!-- Jinja автоматически КОДИРУЕТ автора -->
    <strong>{{ comment.author }}</strong> 
    
    <!-- Для тела мы разрешаем HTML, так как уже очистили его бличем -->
    <div>{{ comment.body | safe }}</div> 
</div>
{% endfor %}
'''

@app.route("/comment", methods=["POST"])
def comment():
    author = request.form.get("author", "anonymous")
    # 3. Валидация на длину имени или спец символы
    body = request.form.get("body", "")
    conn = get_db()
    conn.execute("INSERT INTO comments (author, body) VALUES (?, ?)", (author, body))
    conn.commit()
    conn.close()
    return redirect("/")