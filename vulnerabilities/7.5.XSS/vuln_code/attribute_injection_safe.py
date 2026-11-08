import os
from flask import Flask, request, render_template_string, abort
from urllib.parse import urlparse

app = Flask(__name__)

# Белый список разрешенных путей для перенаправления
ALLOWED_ROUTES = ['/profile']
def is_safe_url(url):
    """Проверяет, что URL безопасен: относительный путь ИЛИ строго из белого списка"""
    if not url:
        return False
    # Парсим URL, чтобы проверить схему
    parsed_url = urlparse(url)
    # Если это абсолютный URL (http://example.com), блокируем
    if parsed_url.netloc or parsed_url.scheme:
        return False
    # Проверяем, входит ли путь в наш белый список
    return parsed_url.path in ALLOWED_ROUTES
    
@app.route("/")
def index():
    next_url = request.args.get("next", "/profile")
    label = request.args.get("label", "Continue")
    
    # Валидация - если URL не в белом списке, принудительно сбрасываем на дефолт
    if not is_safe_url(next_url):
        next_url = "/profile"

    profile_template = """
    <h1>Redirect page</h1>
    <p>Click the link to continue.</p>
    <a class="button" href="{{ url }}">{{ lab }}</a>
    """
    
    # Передаем переменные в контекст Jinja
    return render_template_string(profile_template, url=next_url, lab=label)

@app.route("/profile")
def profile():
    avatar = request.args.get("avatar", "https://example.com/avatar.png")
    
    # Валидация
    parsed_ava = urlparse(avatar)
    # Проверяем, что расширение заканчивается на .png
    is_png = parsed_ava.path.lower().endswith('.png')
    
    # Проверяем, что протокол только http или https (блокируем javascript:)
    # Если это относительный путь (без протокола), тоже разрешаем
    is_safe_protocol = parsed_ava.scheme in ['http', 'https', '']

    if not (is_png and is_safe_protocol):
        # Если аватар не прошел проверку, ставим дефолтный безопасный
        avatar = "https://example.com/avatar.png"

    # Шаблон БЕЗ f-строк
    ava_template = """
    <h1>Profile</h1>
    <img src="{{ ava_url }}" alt="User avatar" width="120">
    <p>Demo profile page</p>
    """
    
    return render_template_string(ava_template, ava_url=avatar)