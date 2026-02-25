from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)                       # Создаём экземпляр приложения Flask
app.secret_key = 'simple-secret-key'        # Нужен для работы сессионных данных и flash-сообщений

# Хранилище сообщений
chat_messages = [
    '<p><strong>Admin 1:</strong> Добро пожаловать в чат!</p>'
]

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
            flash('Имя пользователя обязательно!')
        elif not email:
            flash('Email обязателен!')
        elif len(password) < 6:
            flash('Пароль должен быть минимум 6 символов!')
        else:
            # В реальном приложении здесь была бы регистрация в БД
            flash('Регистрация успешна! Теперь войдите в чат.')
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
        chat_messages.append(f'<p><strong>Вы:</strong> {message}</p>')
    # После добавления сообщения перенаправляем обратно на страницу чата
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)
