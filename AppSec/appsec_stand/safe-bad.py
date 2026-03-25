from flask import Flask, render_template, request, redirect, url_for, session, flash, g as flask_session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_user_by_username, create_user
from session_manager import create_session, get_session_data
import json
import os
from functools import wraps

import unicodedata                  # нормализует Unicode 
from urllib.parse import unquote    # декодирует URL
import bleach                       # Санитизация
import re                           # Валидация
#from flask import escape            # Энкодинг - старая версия
from markupsafe import escape, Markup   # Энкодинг - новая версия

app = Flask(__name__)
app.secret_key = '6G6A906SBHP7@J0KX0'  #  — заменить 

DATA_FILE = os.path.join('data', 'users.json')
'''
def load_users():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
'''
'''
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = g.session_id = session.get('session_id')
        if not session_id:
            return redirect(url_for('login'))

        session_data = get_session_data(session_id)
        if not session_data:
            session.pop('session_id', None)
            return redirect(url_for('login'))

        # Сохраняем username в контексте запроса
        g.current_user = session_data['data']['username']
        return f(*args, **kwargs)
    return decorated_function
'''
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = flask_session.get('session_id')
        if not session_id:
            return redirect(url_for('login'))

        session_data = get_session_data(session_id)
        if not session_data:
            flask_session.pop('session_id', None)
            return redirect(url_for('login'))

        # Сохраняем username в контексте запроса для удобства
        flask_g.current_user = session_data['data']['username']
        return f(*args, **kwargs)
    return decorated_function
    
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
        exist_user = get_user_by_username(username)
        if exist_user:
            flash('Пользователь уже существует', 'error')
            return render_template('register.html')
        # Хешируем пароль
        pw_hash = generate_password_hash(password)
        
        # Регистрируем пользователя        
        if create_user(username, email, pw_hash):
            flash('Регистрация прошла успешно. Войдите.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Ошибка при регистрации', 'error')
            return render_template('register.html')
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Заполните все поля', 'error')
            return render_template('login.html')
        #users = load_users()
        exist_user = get_user_by_username(username)
        #user = users.get(username)
        if exist_user and check_password_hash(generate_password_hash(password), password):
            #session['username'] = username
            create_session(exist_user[0], username)     # exist_user[0] - ID пользователя
            flash('Вы успешно вошли', 'success')
            
            # полезная нагрузка для выполнения уязвимости
            admin_message = "<script>alert(1)</script>"
            msgs = session.get('messages', [])
            #msgs.append({'text': f'<strong>Admin: </strong> Добро пожаловать в чат поддержки!', 'type': 'admin'})
            decoded = unquote(admin_message)                    # декодирует URL
            normalized = unicodedata.normalize('NFC', decoded)  # нормализует Unicode
            clean = bleach.clean(normalized)                    # Санитизация
            print("Message 3 :", clean)
            msgs.append({'text': f'<strong>Admin: </strong> {clean}', 'type': 'admin'})
            session['messages'] = msgs
            print("exist_user:", exist_user)
            print("check_password_hash(user['password']:", check_password_hash(generate_password_hash(password), password))
            print("password:", password)
        
            return redirect(url_for('chat'))
        flash('Неверный логин или пароль', 'error')
        return render_template('login.html')
    return render_template('login.html')
    
'''@app.route('/register_json', methods=['GET', 'POST'])
def register_json():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        if not username or not password or not email:
            flash('Заполните все поля', 'error')
            return render_template('register_json.html')
        users = load_users()
        if username in users:
            flash('Пользователь уже существует', 'error')
            return render_template('register_json.html')
        # Хешируем пароль
        pw_hash = generate_password_hash(password)
        users[username] = {"email": email, "password": pw_hash}
        save_users(users)
        flash('Регистрация прошла успешно. Войдите.', 'success')
        return redirect(url_for('login'))
    return render_template('register_json.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Заполните все поля', 'error')
            return render_template('login.html')
        users = load_users()
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Вы успешно вошли', 'success')
            
            # полезная нагрузка для выполнения уязвимости
            admin_message = "<script>alert(1)</script>"
            msgs = session.get('messages', [])
            #msgs.append({'text': f'<strong>Admin: </strong> Добро пожаловать в чат поддержки!', 'type': 'admin'})

            decoded = unquote(admin_message)                    # декодирует URL
            normalized = unicodedata.normalize('NFC', decoded)  # нормализует Unicode
            clean = bleach.clean(normalized)                    # Санитизация
            print("Message 3 :", clean)

            msgs.append({'text': f'<strong>Admin: </strong> {clean}', 'type': 'admin'})
            session['messages'] = msgs

            print("user:", user)
            print("check_password_hash(user['password']:", check_password_hash(user['password'], password))
            print("password:", password)
        
            return redirect(url_for('chat'))
        flash('Неверный логин или пароль', 'error')
        return render_template('login.html')
    return render_template('login.html')
'''
@app.route('/chat', methods=['GET'])
@login_required
def chat():
    # Теперь username берётся из g.current_user, а не из session
    #messages = get_messages_from_db(g.current_user)  # Ваша функция получения сообщений
    #return render_template('chat.html', username=g.current_user, messages=messages)
    return render_template('chat.html', username=g.current_user, messages=session.get('messages', []))

'''
@app.route('/chat', methods=['GET'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'], messages=session.get('messages', []))
'''

@app.route('/send', methods=['POST'])
def send():
    if 'username' not in session:
        return redirect(url_for('login'))
    message = request.form.get('message', '')
    print("Message 1 :", message)
    clean = message
    # Санитизация
    '''clean = bleach.clean(
        message,
        #tags=["b", "i", "u"],
        attributes={},
        strip=True
    )
    clean = bleach.clean(message)
    #clean = message
    print("Message 2 :", clean)
    '''
    # Декодирование, нормализация, санитизация
    decoded = unquote(message)      # декодирует URL
    normalized = unicodedata.normalize('NFC', decoded)  # нормализует unicode
    clean = bleach.clean(normalized)  # санитизация
    print("Message 3 :", clean)
    
    # Валидация
    '''if not re.match(r"^[a-zA-Z0-9\s]+$", message):
        flash('Недопустимые символы (<,>,(,),:,;,.,, и т.д.)', 'error')
        return redirect(url_for('chat'))
        #return "Invalid input"
    clean = message
    print("Message 3 :", clean)
    '''
    # "Энкодинг    
    '''clean = escape(message)  # Безопасное экранирование
    print("Message 3 :", clean)
    '''
    # Белый список
    '''white_list = ["b", "i", "a"]  # разрешённые HTML-теги
    clean = bleach.clean(
        message,
        tags = white_list
    )
    print("Message 3 :", clean)
    '''
    # сохранить сообщение в сессии. В учебном стенде можно хранить сообщения в памяти или в файле
    #msgs = []
    msgs = session.get('messages', [])
    #username = session['username'] 
    username = get_user_by_username(username)
    #msgs.append({"user": session['username'], "text": message})
    msgs.append({'text': f'<strong>{username}:</strong> {clean}', 'type': 'user'})
    session['messages'] = msgs
    return redirect(url_for('chat'))
    
# Для демонстрации сохраненной XSS - <script>alert(1)</script>
'''@app.route('/send', methods=['POST'])
def send():
    if 'username' not in session:
        return redirect(url_for('login'))
    message = request.form.get('message', '')
    print("Message:", message)
    # сохранить сообщение в сессии (не для продакшна). В учебном стенде можно хранить сообщения в памяти или в файле
    msgs = session.get('messages', [])
    username = session['username']
    #msgs.append({"user": session['username'], "text": message})
    msgs.append({'text': f'<strong>{username}:</strong> {message}', 'type': 'user'})
    session['messages'] = msgs
    return redirect(url_for('chat'))
'''
# Для демонстрации отраженной XSS - <script>alert(1)</script>
'''@app.route('/send', methods=['GET'])
def send():
    if 'username' not in session:
        return redirect(url_for('login'))
    message = request.args.get('message', '')
    print("Message:", message)
    msgs = session.get('messages', [])
    username = session['username']
    #msgs.append({"user": session['username'], "text": message})
    msgs.append({'text': f'<strong>{username}:</strong> {message}', 'type': 'user'})
    session['messages'] = msgs
    return redirect(url_for('chat'))
'''

@app.route('/logout', methods=['POST'])
def logout():
    session_id = flask_session.get('session_id')
    if session_id:
        delete_session(session_id)
        flask_session.pop('session_id', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug=True)