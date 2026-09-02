SameSite атрибут cookie.
Например: Set-Cookie: session=abc123; SameSite=Lax

Он отвечает: Когда браузеру разрешено отправлять эту cookie в cross-site запросах.

1. SameSite=Strict
Максимально ограничительный вариант.
Set-Cookie: session=abc123; SameSite=Strict
Cookie практически не используется в cross-site контекстах.

2.SameSite=Lax
Более мягкий и распространённый вариант.
Set-Cookie: session=abc123; SameSite=Lax
Некоторые cross-site сценарии разрешаются, другие блокируются.

3. SameSite=None
Разрешает cookie использоваться в cross-site контексте.
Но требуется: SameSite=None; Secure