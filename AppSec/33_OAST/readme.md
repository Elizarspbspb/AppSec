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

