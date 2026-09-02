from http.server import SimpleHTTPRequestHandler, test
from urllib.parse import urlparse, parse_qs
import html

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        #self.send_header('Content-Security-Policy', 'default-src')
        
        # Если это корневой запрос, обрабатываем его динамически
        if parsed_url.path == '/' or parsed_url.path == '/site.html':
            # Получаем параметр 'q'. Если его нет, ставим пустую строку
            q_value = query_params.get('q', [''])[0]
            
            # --- ЗАЩИТА ОТ XSS (Безопасный вариант) ---
            # Раскомментируйте строку ниже, чтобы предотвратить выполнение скрипта:
            # q_value = html.escape(q_value)
            # ------------------------------------------

            try:
                # Читаем ваш HTML-шаблон
                with open('site.html', 'r', encoding='utf-8') as file:
                    html_content = file.read()
                
                # Вставляем параметр в HTML вместо метки {{QUERY}}
                rendered_content = html_content.replace('{{QUERY}}', q_value)
                
                # Отправляем успешный HTTP-ответ
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(rendered_content.encode('utf-8'))
                return
                
            except FileNotFoundError:
                self.send_error(404, "Файл site.html не найден")
                return

        # Для остальных файлов (css, js, картинки) используем стандартное поведение
        super().do_GET()

if __name__ == '__main__':
    print("Сервер запущен на http://localhost:8000/")
    test(HandlerClass=CustomHandler, port=8000)
