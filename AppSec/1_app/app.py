from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)                       # Создаём экземпляр приложения Flask
app.secret_key = 'simple-secret-key'        # Нужен для работы сессионных данных и flash-сообщений

# Хранилище сообщений
chat_messages = [
    {'text': '<strong>Admin:</strong> Добро пожаловать в чат поддержки!', 'type': 'admin'}
]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Здесь должна быть проверка пользователя в базе данных
        # Для примера — простая проверка фиктивных данных
        if username == 'test' and password == 'test123':
            flash('Успешный вход! Добро пожаловать в чат.', 'success')
            return redirect(url_for('chat'))
        else:
            flash('Неверное имя пользователя или пароль.', 'error')

    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Здесь должна быть проверка email в базе данных
        # Для примера — простая проверка фиктивного email
        if email == 'test@mail.com':
            flash('Инструкция по восстановлению пароля отправлена на email.', 'success')
        else:
            flash('Email не найден в системе.', 'error')

    return render_template('forgot-password.html')
    
# Маршрут для главной страницы ('/')
@app.route('/')
def index():
    return redirect(url_for('register'))    # Главная страница — перенаправляет на регистрацию

# Маршрут для страницы регистрации ('/register')
# Поддерживает методы GET (показать форму) и POST (обработать отправку)
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Если метод запроса — POST (форма отправлена)
    if request.method == 'POST':
        # Получаем данные из полей формы
        #username = request.form.get('username')
        username = request.form.get('username', 'Гость')
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Получено имя пользователя: {username}")
        print(f"Все данные формы: {request.form}")

        # Простая валидация
        if not username:
            flash('Имя пользователя обязательно!', 'error')
        elif not email:
            flash('Email обязателен!', 'error')
        elif len(password) < 6:
            flash('Пароль должен быть минимум 6 символов!', 'error')
        else:
            # В реальном приложении здесь была бы регистрация в БД
            flash('Регистрация успешна! Теперь войдите в чат.', 'success')
            # Перенаправляем на страницу чата
            return redirect(url_for('chat'))
    # Если метод GET или валидация не пройдена — показываем страницу регистрации
    return render_template('register.html')

# Маршрут для страницы чата ('/chat')
@app.route('/chat')
def chat():
    # Передаём список сообщений и рендерим шаблон chat.html
    return render_template('chat.html', messages=chat_messages)

# Маршрут для обработки отправки сообщений ('/send')
# Принимает только POST-запросы (отправка формы)
@app.route('/send', methods=['POST'])
def send_message():
    # Получаем текст сообщения из поля формы, убираем пробелы по краям
    message = request.form.get('message', '').strip()
    print(f"Сообщение: {message}")
    print(f"Текущее количество сообщений: {len(chat_messages)}")
    if message:
        # Форматируем сообщение с указанием автора («Вы») и добавляем в список
        # chat_messages.append(f'<p><strong>Вы:</strong> {message}</p>')
        chat_messages.append({
            'text': f'<strong>Вы:</strong> {message}',
            'type': 'user'
        })
    # После добавления сообщения перенаправляем обратно на страницу чата
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)
