Docker image в формате OCI image archive (архив образа Docker).
Это стандартная структура, когда делают экспорт образа командой вроде: docker save -o lab.tar image_name - или через OCI export.

Импортировать в Docker:
sudo docker load -i sqlmap_lab.tar
sudo docker images

sudo docker run -p 5000:5000 sqlmap_lab

Часть 1.
Запущен стенд sqlmap_lab по URL - http://127.0.0.1:5000/
С помощью FoxyProxy в браузере настроен прокси на ZAP. 
Открыл сайт в браузере и в ZAP в панели Sites появился сайт. Создал Context с именем sqlmap_lab. 
В Include in Context задал область тестирования http://172.17.0.2:5000.* 
Проверил сайт и ZAP увидел основные запросы. 

Часть 2.
Запустил Spider. В результате получил, что http://172.17.0.2:5000/sitemap.xml и http://172.17.0.2:5000/robots.txt не обнаружены. Spider выполнил несколько запросов в search и ответ ОК.

Запустил Active Scan. В результате получил множество запросов. 
Интересно - %3Cxsl%3Avalue-of+select%3D%22system-property%28%27xsl%3Avendor%27%29%22%2F%3E (<xsl:value-of select="system-property('xsl:vendor')"/>). В таком случае сайт возвращает ошибку - Ошибка выполнения запроса: near "xsl": syntax error
system-property('xsl:vendor')/> - Ошибка выполнения запроса: near "xsl": syntax error
a and exists ( select "java.lang.Thread.sleep"(15000) from INFORMATION_SCHEMA.SYSTEM_COLUMNS where TABLE_NAME = 'SYSTEM_COLUMNS' and COLUMN_NAME = 'TABLE_NAME') --  - Ошибка выполнения запроса: near "SYSTEM_COLUMNS": syntax error
Введенные значения попали в SQL-запрос и где-то возможно SQL инъекция. 
Дальше в Alerts видны потенциальные уязвимости. 

Сохранены отчёты ZAP в формате HTML.

Расстановка рисков по приоритету - 
1. Content Security Policy (CSP) Header Not Set (Medium) - нет правил загрузки скриптов браузером.
2. Missing Anti-clickjacking Header (Medium) - нет параметра x-frame-options и позволяет встраивать сайт в iframe на других страницах.
3. Server Leaks Version Information via “Server” HTTP Response Header Field (Low) - утечка версии сервера
4. X-Content-Type-Options Header Missing (Low) - нет заголовка X-Content-Type-Options от снифинга. 
5. User Controllable HTML Element Attribute (Potential XSS) (Informational) - пользователь контролирует html аттрибут. 

Часть 3.
Повторим через Burp. 
1. При тестировании Content Security Policy (CSP) Header Not Set (Medium) в области Response не обнаружен заголовок Content-Security-Policy - Confirmed (Подтверждение)
Content-Security-Policy задаёт правила для браузера: какие источники контента разрешены, а какие — нет.
2. Missing Anti-clickjacking Header (Medium) -  в области Response не обнаружен заголовок X-Frame-Options - Confirmed (Подтверждение)
X-Frame-Options — это HTTP-заголовок ответа, который сообщает браузеру, разрешено ли отображать страницу в HTML-элементах
3. Server Leaks Version Information (Low) - в области Response  приложение возвращает версию сервера и ЯП - Server: Werkzeug/3.1.5 Python/3.11.14  - Confirmed (Подтверждение)
4. X-Content-Type-Options Header Missing (Low) - в области Response не обнаружен заголовок X-Content-Type-Options - Confirmed (Подтверждение)
5. User Controllable HTML Element Attribute (Potential XSS) - При отправке <img src=x onerror=alert(1)> или javascript:alert(1) или " onmouseover=alert(1) ничего не выводится. А если - <script>fetch('/change-email?email=hacker@mail.com')</script> то ответ Ошибка выполнения запроса: near "?": syntax error. Веротянее тут False Positive (Ошибка) но для XSS, а не для SQL-инъекции. 
Ввод admin' выдает - Ошибка выполнения запроса: near "'%'": syntax error, значит ввод ' UNION SELECT NULL,NULL,NULL-- вывел всю базу данных пользователей. 

Часть 4. 
Сформирован HAR файл для последнего случая с SQL-инъекцией.
Сделан скриншот

Часть 5. 
Выполнил

Небольшой вопрос. Вот в задании - Составьте список находок и отсортируйте их по приоритету. Я смотрел в ALerts и там были находки с риском - Information. И вот вопрос, они то же участвуют в сортировке или нет?
