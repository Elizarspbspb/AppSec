from flask import Flask, request, send_file, render_template_string
import os

app = Flask(__name__)

# HTML шаблон с красивым интерфейсом
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Файловый менеджер</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 40px;
            max-width: 500px;
            width: 100%;
            text-align: center;
        }
        
        .logo {
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 30px;
            font-weight: 600;
        }
        
        .description {
            color: #666;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .form-group {
            margin-bottom: 25px;
            text-align: left;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            color: #856404;
            font-size: 14px;
        }
        
        .file-list {
            text-align: left;
            margin-top: 20px;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
        }
        
        .file-list h3 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .file-item {
            padding: 8px;
            border-bottom: 1px solid #e9ecef;
            color: #495057;
        }
        
        .file-item:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">📁</div>
        <h1>Файловый менеджер</h1>
        
        <p class="description">
            Введите имя файла для скачивания. Доступные файлы находятся в папке 'files'.
        </p>
        
        <form action="/download" method="get">
            <div class="form-group">
                <label for="file">Имя файла:</label>
                <input type="text" id="file" name="file" placeholder="Введите имя файла..." required>
            </div>
            <button type="submit" class="btn">
                📥 Скачать файл
            </button>
        </form>
        
        <div class="file-list">
            <h3>📋 Примеры файлов:</h3>
            <div class="file-item">document.txt</div>
            <div class="file-item">report.pdf</div>
            <div class="file-item">image.jpg</div>
        </div>
        
        <div class="warning">
            ⚠️ <strong>Внимание:</strong> Эта демонстрационная версия содержит уязвимость Directory Traversal.
            Не используйте в production среде!
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# УЯЗВИМЫЙ КОД - неправильная обработка пользовательского ввода
@app.route('/download')
def download_file():
    filename = request.args.get('file')  # Пользовательский ввод без валидации
    
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ: прямое использование пользовательского ввода
    file_path = os.path.join('files', filename)
    
    return send_file(file_path)

if __name__ == '__main__':
    # Создаем тестовую папку с файлами
    if not os.path.exists('files'):
        os.makedirs('files')
        # Создаем несколько тестовых файлов
        with open('files/document.txt', 'w') as f:
            f.write('Это тестовый документ.')
        with open('files/report.pdf', 'w') as f:
            f.write('PDF content would be here.')
        with open('files/image.jpg', 'w') as f:
            f.write('Image content would be here.')
    
    app.run(host='0.0.0.0', port=5000, debug=True)
