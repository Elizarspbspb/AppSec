from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

import unicodedata                  # нормализует Unicode 
from urllib.parse import unquote    # декодирует URL
import bleach                       # Санитизация
import re                           # Валидация

app = Flask(__name__)
app.secret_key = '6G6A906SBHP7@J0KX0'  #  — заменить 

DATA_FILE = os.path.join('data', 'users.json')

def load_users():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
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
        if not username or not password:
            flash('Заполните все поля', 'error')
            return render_template('login.html')
        users = load_users()
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Вы успешно вошли', 'success')
            msgs = session.get('messages', [])
            msgs.append({'text': f'<strong>Admin: </strong> Добро пожаловать в чат поддержки!', 'type': 'admin'})
            session['messages'] = msgs
            
            print("user:", user)
            print("check_password_hash(user['password']:", check_password_hash(user['password'], password))
            print("password:", password)
        
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
    return render_template('chat.html', username=session['username'], messages=session.get('messages', []))

@app.route('/send', methods=['POST'])
def send():
    if 'username' not in session:
        return redirect(url_for('login'))
    message = request.form.get('message', '')
    print("Message 1 :", message)
    
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
    # декодирует Нормализация Санитизация
    '''decoded = unquote(message)      # декодирует URL
    normalized = unicodedata.normalize('NFC', decoded)  # нормализует Unicode
    clean = bleach.clean(normalized)  # Санитизация
    print("Message 3 :", clean)
    '''
    # Валидация
    if not re.match(r"^[a-zA-Z0-9\s]+$", message):
        flash('Недопустимые символы (<,>,(,),:,;,.,, и т.д.)', 'error')
        return redirect(url_for('chat'))
        #return "Invalid input"
    clean = message
    print("Message 3 :", clean)
    
    # сохранить сообщение в сессии (не для продакшна). В учебном стенде можно хранить сообщения в памяти или в файле
    msgs = session.get('messages', [])
    username = session['username']
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
if __name__ == '__main__':
    app.run(debug=True)