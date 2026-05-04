from seleniumwire import webdriver  # Обратите внимание: seleniumwire, а не selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')

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
<form id="message-form" action="http://127.0.0.1:5000/send" method="post">
	<input type="hidden" name="dialog_id" value="14">	
	<input type="text" id="message" name="message" placeholder="Введите сообщение" required="">
    <button type="submit">Отправить</button>
</form>
"""

driver.get(url='http://127.0.0.1:5000/login')
driver.add_cookie({
    "name": "session",
    "value": "eyJ1c2VybmFtZSI6IjEyMyJ9.adO_8g.k5RNBLcp1MIFmaRu1YumN9i1GGU",
    "domain1": "127.0.0.1",
    "path": "/",
    "httpOnly": True,
    "secure": False
})


driver.get("data:text/html;charset=utf-8," + html_form)

img_url = f"test from python"
try:
    # Находим поле ввода и вставляем ссылку
    input_field = driver.find_element(By.ID, "message")
    input_field.send_keys(img_url)

    # Нажимаем кнопку отправки
    driver.find_element(By.ID, "message-form").submit()

    # Ждём загрузки страницы (настройте под свой случай)
    time.sleep(1)

    # Получаем HTML текущей страницы
    page_html = driver.page_source
    # Выводим в консоль результат запроса
    print(f"\n--- Результат для {img_url} ---")
    print(page_html)
    print("-" * 50)
    # смотрим перехваченные запросы
    print(f"\n--- Перехваченные запросы для {img_url} ---")
    for request in driver.requests:
        if request.method == "POST":
            print("URL:", request.url)
            print("Body:", request.body)
    print("-" * 50)
          
except (NoSuchElementException, TimeoutException) as e:
    print(f"Ошибка при обработке {img_url}: {e}")
except Exception as e:
    print(f"Неожиданная ошибка для {img_url}: {e}")
        
# Закрываем браузер
driver.quit()