from flask import Flask, request, render_template_string, send_file
import os

app = Flask(__name__)

# HTML шаблон с красивым интерфейсом
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Просмотрщик файлов</title>
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
            max-width: 800px;
            width: 100%;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo {
            font-size: 3em;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.1em;
        }
        
        .upload-section {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        
        input[type="text"], input[type="file"] {
            width: 100%;
            padding: 12px 15px;
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
            margin-top: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: #6c757d;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
        }
        
        .file-content {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .alert {
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            font-weight: 500;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .file-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        
        .file-item {
            background: white;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid #e1e5e9;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .file-item:hover {
            border-color: #667eea;
            transform: translateY(-2px);
        }
        
        .file-icon {
            font-size: 2em;
            margin-bottom: 5px;
        }
        
        .tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #e1e5e9;
        }
        
        .tab {
            padding: 12px 25px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }
        
        .tab.active {
            border-bottom-color: #667eea;
            color: #667eea;
            font-weight: 600;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">📁</div>
            <h1>Файловый просмотрщик</h1>
            <p class="subtitle">Загружайте и просматривайте файлы</p>
        </div>
        
        <div class="tabs">
            <div class="tab active" onclick="switchTab('view')">👁️ Просмотр файлов</div>
            <div class="tab" onclick="switchTab('upload')">📤 Загрузка файлов</div>
        </div>
        
        <div id="view-tab" class="tab-content active">
            <div class="upload-section">
                <h3>📖 Просмотр файла</h3>
                <form action="/" method="get">
                    <div class="form-group">
                        <label for="file">Путь к файлу:</label>
                        <input type="text" id="file" name="file" placeholder="Введите путь к файлу..." value="{{ request_file }}">
                    </div>
                    <button type="submit" class="btn">👀 Просмотреть файл</button>
                </form>
                
                <div class="form-group">
                    <label>Примеры файлов:</label>
                    <div class="file-list">
                        <div class="file-item" onclick="setFile('files/welcome.txt')">
                            <div class="file-icon">📝</div>
                            welcome.txt
                        </div>
                        <div class="file-item" onclick="setFile('files/config.ini')">
                            <div class="file-icon">⚙️</div>
                            config.ini
                        </div>
                        <div class="file-item" onclick="setFile('/etc/hosts')">
                            <div class="file-icon">🌐</div>
                            /etc/hosts
                        </div>
                        <div class="file-item" onclick="setFile('/etc/passwd')">
                            <div class="file-icon">👤</div>
                            /etc/passwd
                        </div>
                    </div>
                </div>
            </div>
            
            {% if file_content %}
            <div class="file-content">
{{ file_content }}
            </div>
            {% endif %}
            
            {% if error %}
            <div class="alert alert-danger">
                ❌ {{ error }}
            </div>
            {% endif %}
            
            {% if success %}
            <div class="alert alert-success">
                ✅ {{ success }}
            </div>
            {% endif %}
        </div>
        
        <div id="upload-tab" class="tab-content">
            <div class="upload-section">
                <h3>📤 Загрузить файл</h3>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="upload_file">Выберите файл:</label>
                        <input type="file" id="upload_file" name="file" required>
                    </div>
                    <button type="submit" class="btn">🚀 Загрузить файл</button>
                </form>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }
        
        function setFile(filename) {
            document.getElementById('file').value = filename;
        }
        
        // Auto-switch to view tab if there's file content
        {% if file_content or error %}
        switchTab('view');
        {% endif %}
    </script>
</body>
</html>
'''

# УЯЗВИМЫЙ КОД - Local File Inclusion
@app.route('/')
def index():
    file_path = request.args.get('file', '')
    file_content = None
    error = None
    success = None
    
    if file_path:
        try:
            # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ: прямое использование пользовательского ввода
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
            success = f"Файл {file_path} успешно прочитан"
        except Exception as e:
            error = f"Ошибка при чтении файла: {str(e)}"
    
    return render_template_string(HTML_TEMPLATE, 
                                file_content=file_content, 
                                error=error, 
                                success=success,
                                request_file=file_path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Файл не выбран", 400
    
    file = request.files['file']
    if file.filename == '':
        return "Файл не выбран", 400
    
    # Сохраняем файл в папку files
    if not os.path.exists('files'):
        os.makedirs('files')
    
    filename = file.filename
    file.save(os.path.join('files', filename))
    
    return render_template_string(HTML_TEMPLATE, 
                                success=f"Файл {filename} успешно загружен",
                                request_file=f"files/{filename}")

if __name__ == '__main__':
    # Создаем тестовые файлы
    if not os.path.exists('files'):
        os.makedirs('files')
    
    # Создаем тестовые файлы
    with open('files/welcome.txt', 'w') as f:
        f.write('Добро пожаловать в файловый просмотрщик!\nЭто демонстрационный файл.')
    
    with open('files/config.ini', 'w') as f:
        f.write('[database]\nhost=localhost\nport=5432\nuser=admin\n\n[app]\ndebug=true\nsecret_key=supersecret')
    
    
    print("Сервер запущен на http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)


            