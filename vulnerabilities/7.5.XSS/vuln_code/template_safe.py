from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    nickname = request.args.get("nickname", "guest")
    
    # Валидация - ограничиваем длину никнейма на входе
    if len(nickname) > 20:
        nickname = nickname[:20] # Обрезаем или выдаем ошибку
        
    template = """
    <h1>User dashboard</h1>
    <div class="banner">Welcome to the security lab!</div>
    <p>Hello, {{ nickname }}</p>
    """
    
    return render_template_string(template, nickname=nickname)

