from flask import request, render_template_string, Flask, render_template, make_response
import secrets

app = Flask(__name__)

# http://localhost:5000/xss?code=<script>alert()</script>
@app.route("/xss")
def index():

    code = request.args.get('code')
    # unsafe - 1; alert(document.cookie)
    return render_template_string("<script> var a={{code}}; console.log(a); </script>", code=code)
    # safe - Фильтр | tojson
    return render_template_string("<script> var a={{ code | tojson }}; console.log(a); </script>", code=code)
    
    # В старых шаблонизаторах - unsafe - '; alert(document.cookie); //
    # В новых шаблонизаторах - safe - Добавление '' дает современной Jinja подсказку, от чего именно нужно защищать строку 
    return render_template_string("<script> var a='{{code}}'; console.log(a); </script>", code=code)

    # unsafe - alert(document.cookie)
    return render_template_string("<script> var a='{{code}}'; eval(a); console.log(a); </script>", code=code)

@app.route("/xss")
def handle_request():
    code = request.args.get("code", "")
    nonce = secrets.token_urlsafe(16)

    html = render_template("xss3.html", code=code, nonce=nonce)

    response = make_response(html)
    # response = make_response(f"<h1>{code}</h1> <script nonce=\"{nonce}\">alert('Ваш скрипт выполнился'); </script>")
    response.headers["Content-Security-Policy"] = f"script-src 'nonce-{nonce}';"
    # nonce - специальный одноразовый секретный ключ (nonce), совпадающий с ключом в заголовке
    # Content-Security-Policy: 
        # default-src 'self'; 
        # script-src 'self' 'nonce-rAnd0mK3y' https://trusted-cdn.com; 
        # img-src 'self' https://unsplash.com data:; 
        # connect-src 'self' https://yourproject.com; 
        # object-src 'none';

    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)

# Небезопасный xss3.html
'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>XSS Lab</title>
</head>
<body>
    <script nonce="{{ nonce }}">
        var a = {{ code }};
    </script>
</body>
</html>
'''

# Безопасный 
'''
var a = {{ code | tojson }};
'''
# Безопасный 2
'''
var a = '{{ code }}';
'''
# Безопасный 3
'''
<body>
    <!-- Этот тег браузер НИКОГДА не выполняет как код, даже если там будет скрипт -->
    <script id="server-data" type="application/json">
        {{ code | tojson }}
    </script>

    <script nonce="{{ nonce }}">
        // Безопасно забираем данные из тега выше
        const rawData = document.getElementById('server-data').textContent;
        const a = JSON.parse(rawData);
        console.log(a);
    </script>
</body>
'''