Content-Security-Policy (CSP) не является самостоятельной уязвимостью типа XSS.

Поэтому самый наглядный эксперимент — сделать XSS + CSP и посмотреть, как CSP его блокирует 
http://localhost:8000/?q=<img src=x onerror=alert(1)>

Content-Security-Policy: default-src 'self' -  Разрешать ресурсы только с текущего домена.
В зависимости от конкретной CSP-политики выполнение inline JavaScript будет заблокировано.
Политик много, надо гуглить 

CSP является дополнительным защитным механизмом, который может снизить последствия определённых XSS.

В случае с кодом:
<script>
document.getElementById("output").innerHTML = 'Результаты: ' + q;
</script>
интересны именно: script-src и default-src. Потому что у тебя есть inline JavaScript.

Надо смотреть - 
1. Пользовательский ввод попадает в HTML:
innerHTML
document.write()
outerHTML
insertAdjacentHTML()

2. Есть ли выполнение JavaScript из внешних источников:
<script src="...">
Например:
<script src="https://cdn.example.com/app.js"></script>
Тогда CSP может ограничивать:
script-src 'self'
чтобы разрешать JS только со своего домена.

3. Есть ли inline JavaScript
У заказчика у тебя есть: 
<script>
    const params = ...
</script>

Без CSP <script> разрешён.
С жёсткой CSP: Content-Security-Policy: script-src 'self' он будет заблокирован.


Для работы используем Burp !!!
1. Включаем перехват запросов: Proxy → Intercept
Установи: Intercept is ON
Теперь Burp будет останавливать запросы браузера.

2. Включаем перехват ответов сервера: Proxy → Proxy settings → Proxy → Response interception rules → Intercept responses based on the following rules
Далее можно создать правило.
Теперь Burp будет перехватывать не только:

3. Открываем страницу в браузере - http://62.173.140.174:36101/?q=123
Burp остановит запрос:

GET /?q=123 HTTP/1.1
Host: 62.173.140.174:36101
...
Запрос не изменяем. Нажимаем: Forward

4. Burp перехватывает ответ. Теперь должно появиться что-то вроде:
HTTP/1.1 200 OK
Server: gunicorn
Date: ...
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 1322

Вот здесь мы добавляем после Content-Type: Content-Security-Policy: default-src 'self'

5. Отправляем изменённый ответ браузеру. Нажимаем: Forward. Теперь Burp отправляет браузеру изменённый нами ответ.
Сервер заказчика при этом не изменён. Мы только изменили конкретный ответ, проходящий через твой Burp.

6. Смотрим результат в браузере. Поэтому с Content-Security-Policy: default-src 'self' браузер должен заблокировать выполнение этого inline-скрипта.
В консоли появится сообщение о нарушении CSP, например:
Content Security Policy: The page's settings blocked the execution of an inline script.
И результат не должен появиться.

7. Мы доказали: При наличии CSP default-src 'self' браузер блокирует используемый сайтом inline JavaScript. Это показывает, что CSP реально влияет на работу данного приложения.