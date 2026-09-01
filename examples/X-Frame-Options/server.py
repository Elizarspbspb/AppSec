from http.server import SimpleHTTPRequestHandler, test

class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем заголовок перед отправкой ответа браузеру
    #    self.send_header('X-Frame-Options', 'DENY')
        super().end_headers()

if __name__ == '__main__':
    # Запускаем сервер на порту 8000
    test(HandlerClass=CustomHandler, port=8000)
