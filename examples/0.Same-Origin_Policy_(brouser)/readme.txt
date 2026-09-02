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

