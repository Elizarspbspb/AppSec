# Цель урока: соединить знания по Python и HTML/CSS в простое веб-приложение на Flask, которое станет учебным стендом для последующих лабораторий по уязвимостям. 

Вы создадите маршруты, шаблоны и реализуете простую авторизацию (регистрация/вход/выход).

### На предыдущих уроках вы:
* Настроили Python и VSCode;
* Вспомнили базовые конструкции Python;
* Сделали HTML-страницы: `register.html` и `chat.html`.

### Теперь нужно собрать всё вместе в минимальное веб-приложение (стенд), чтобы:
* понимать, как данные от клиента доходят до сервера;
* иметь контролируемую «мишень» для безопасных лабораторий (XSS, SQLi, CSRF и т.д.);
* уметь повторно разворачивать и тестировать исправления.

### Что вы создадите в этом уроке (конечный результат)
* Мини-проект на `Flask` с структурой файлов;
* Подключённые HTML-страницы как Jinja-шаблоны;
* Маршруты: /, /register, /login, /logout, /chat, /send;
* Простая сессионная авторизация (в памяти + хеширование паролей);
* Локальный запуск приложения и базовая инструкция по тестированию.

### Рекомендуемая структура проекта
```
appsec_stand/
├─ app.py
├─ requirements.txt
├─ templates/
│  ├─ base.html
│  ├─ register.html   (из урока)
│  ├─ login.html
│  ├─ chat.html       (из урока)
├─ static/
│  ├─ style.css
└─ data/
   └─ users.json     (простая «бд» в файле для обучения)
```
Примечание: для учебной цели используем лёгкую локальную «базу» — JSON-файл. В реальной разработке используйте СУБД. 

Важно: создайте точно такие же папки

### Установка зависимостей
В `requirements.txt` положим:

Flask==2.x

Werkzeug==2.x

(Используйте актуальные 2.x версии; можно установить командой `pip install -r requirements.txt`.)

### Файл app.py — общий план
Ниже — пример минимального кода с комментариями, постарайтесь прогнать его у себя, а потом разбирать по частям.
```python
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = 'change_this_to_secure_random_value'  #  — заменить 

DATA_FILE = os.path.join('data', 'users.json')

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        if not username or not password or not email:
            flash('Заполните все поля', 'error')
            return render_template('register.html')
        users = load_users()
        if username in users:
            flash('Пользователь уже существует', 'error')
            return render_template('register.html')
        # Хешируем пароль
        pw_hash = generate_password_hash(password)
        users[username] = {"email": email, "password": pw_hash}
        save_users(users)
        flash('Регистрация прошла успешно. Войдите.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        users = load_users()
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Вы успешно вошли', 'success')
            return redirect(url_for('chat'))
        flash('Неверный логин или пароль', 'error')
        return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Вы вышли', 'info')
    return redirect(url_for('login'))

@app.route('/chat', methods=['GET'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    # На начальном этапе просто отображаем шаблон с чатом (пустым)
    return render_template('chat.html', username=session['username'])

@app.route('/send', methods=['POST'])
def send():
    if 'username' not in session:
        return redirect(url_for('login'))
    message = request.form.get('message', '')
    # Для демонстрации: просто передаем сообщение в шаблон; позже здесь будут показываться XSS и защита
    # В учебном стенде можно хранить сообщения в памяти или в файле
    # Простейший вариант — временно сохранить в сессии (не для продакшна)
    msgs = session.get('messages', [])
    msgs.append({"user": session['username'], "text": message})
    session['messages'] = msgs
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)
```
### Объяснения к коду (простым языком):
`app.secret_key` — необходим для подписанных cookies (сессий). В учебном проекте можно использовать простую строку, но в рабочем проекте её нужно генерировать случайно и хранить безопасно.

`load_users()` / `save_users()` — читают и записывают JSON-файл с пользователями. Маршруты (@app.route) — это URL-адреса, на которые реагирует приложение.

В регистрационной логике пароль хешируется (через `generate_password_hash`) —  никогда не храните пароли в открытом виде.

`session` — простая модель, как мы помним, кто сейчас залогинен.

### Шаблоны Jinja (templates)
В папке `templates/` разместите HTML-файлы. Можно взять ваши `register.html` и `chat.html`, но сделать их немного более «шаблонными»:
1. `base.html` — общий каркас:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{% block title %}AppSec Stand{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <div class="container">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <ul class="flashes">
          {% for category, msg in messages %}
            <li class="{{ category }}">{{ msg }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
  </div>
</body>
</html>
```
2. `register.html` — расширяет `base.html` и использует поля формы, которые вы уже создавали.

`login.html` — простая форма логина.
`chat.html` — отображает список сообщений из `session['messages']` и форму отправки.

*Важно про шаблоны: `Jinja` автоматически экранирует переменные при выводе `{{ variable }}`, что даёт базовую защиту от `XSS`.*

### Простая авторизация
В этом уроке авторизация реализована элементарно:
* Учётные записи хранятся в `data/users.json` (имя пользователя → хеш пароля и email).
* При логине сравниваем хэш пароля через `check_password_hash`.
* При успешном входе в `session` сохраняем `username`.
* Для доступа к `/chat` и `/send` проверяем наличие `username` в сессии.

### Пояснение безопасности
* `Хешируйте пароли` — это обязателеная практика.
* Для простоты используем сессионные `cookies`. В реальности `session cookie` должно быть `Secure`, `HttpOnly`, иметь политику `SameSite` и передаваться только по `TLS`.
* Не используйте `session` для долговременного или чувствительного хранения (например, секретных ключей).

### Как запускать и тестировать локально
1. Создайте виртуальное окружение:
```
python -m venv venv
source venv/bin/activate # Linux / macOS
venv\Scripts\activate # Windows
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
3. Запустите приложение:
```
python app.py
```
4. Откройте в браузере `http://127.0.0.1:5000/` и пройдите регистрацию/логин.

Проверьте: отправьте сообщение в чате, выйдите и войдите снова — убедитесь, что сессия работает.

### Точки внимания с позиции AppSec (что обсуждать и фиксировать)
* `secret_key` в app.secret_key — обозначьте, где хранить и как генерировать в продакшне (env vars, vault).
* Хранение пользователей — json-файл удобен для уроков, но в дальнейшем обсудим `SQL/ORM` и риски `SQL injection` при неправильной работе.
* `CSRF` — в текущей простой реализации CSRF-защита отсутствует. Это специально: позже вы покажете CSRF-атаки и как защититься (Flask-WTF / CSRF токены).
* `XSS` — проверьте, как `Jinja` экранирует вывод; затем можно явно показать что происходит, если выводить `|safe`.
* Логирование и отладка — `debug=True` удобен при разработке, но в продакшне опасен (не показывайте stacktrace).
* `Cookies` и `HTTPS` — локально это не критично, но в обсуждении отметьте важность TLS для защиты cookies и трафика.
* `Валидация` — и на клиенте и на сервере; в данном уроке делаем базовую проверку (непустые поля), глубокая валидация будет позже.

### Итоги урока
Вы только что собрали свой первый рабочий веб-стенд — это важный шаг: теперь у вас есть контролируемая платформа для изучения реальных проблем AppSec. Понимание того, как клиент и сервер взаимодействуют, куда идут данные и как реализована авторизация, позволит вам впоследствии точно воспроизводить уязвимости и отрабатывать защиту.

На следующем уроке - продемонстрируем реальные уязвимости на этом стенде: `XSS` (отображение сообщений), `CSRF` (операции, изменяющие состояние), и подготовим лабораторию по `SQLi` (если заменим JSON на базу данных). Обсудим и реализуем простые контрмеры: экранирование вывода, CSRF токены, перемещение секретов в переменные окружения.

## 👨🏻‍🎓 Полезные ресурсы для самообразования:
Официальная документация
* `Flask Documentation`: https://flask.palletsprojects.com/ Официальное руководство Flask с примерами, объяснениями маршрутов, шаблонов и работы с сессиями..

Для веб-безопасности
* `MDN Web Docs — HTTP`: Основы протокола: https://developer.mozilla.org/ru/docs/Web/HTTP/Overview Понимание того, как работают запросы, ответы и cookies — основа безопасности веб-приложений.

