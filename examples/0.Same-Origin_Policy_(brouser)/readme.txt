Same-Origin Policy - SOP
Это фундаментальное правило самого браузера:
JavaScript одного origin не должен свободно получать доступ к данным другого origin.

POST /change-email HTTP/1.1
Host: bank.com
Origin: https://attacker.com

Origin — кто отправил запрос (origin).

Origin определяется тремя вещами: scheme + host + port
Например: https://example.com:443
Это один origin.

http://example.com:80
https://example.com:443
https://api.example.com:443
https://example.com:8443
— уже другие origins.

JS код - document.cookie на attacker.com не может просто прочитать cookies client.com.

SOP находится в браузере.

Примечание: «Если разработчик выставит заголовок Access-Control-Allow-Origin: * совместно с Allow-Credentials: true, это полностью обнулит защиту Same-Origin Policy. 
Любой вредоносный сайт в интернете сможет через JavaScript делать запросы к нашему API от имени авторизованного пользователя и читать ответы, воруя его данные».