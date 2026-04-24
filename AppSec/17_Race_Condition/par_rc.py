from seleniumwire import webdriver  # Обратите внимание: seleniumwire, а не selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

import multiprocessing


#def sequential(calc, proc, driver):
def sequential(calc, proc):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    # Настройки заголовков для всех запросов
    selenium_wire_options = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': 'session=eyJ1c2VybmFtZSI6InN0dWRlbnQifQ.aesYCw.e8w3f1FuOfJ2Bazh51i2rfk5bSo'
            # Добавьте другие заголовки при необходимости
            # 'Referer': 'http://example.com',
            # 'Accept': 'image/webp,image/apng,image/*,*/*'
        }
    }

    driver = webdriver.Chrome(
        options=options,
        seleniumwire_options=selenium_wire_options
    )

    html_form_in = """
    <form method="post" action="http://62.173.140.174:36110/login">
            <input id="username" name="username" value="student">
            <input id="password" name="password" type="password" value="student">
            <button type="submit">Войти</button>
          </form>
    """
    driver.get("data:text/html;charset=utf-8," + html_form_in)
    login = "student"
    passw = "student"
    try:
        input_field = driver.find_element(By.ID, "username")
        input_field.clear()
        input_field.send_keys(login)
        
        input_field = driver.find_element(By.ID, "password")
        input_field.clear()
        input_field.send_keys(passw)
        
        # Нажимаем кнопку отправки
        submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
        submit_btn.click()
        # Ждём загрузки страницы (настройте под свой случай)
        time.sleep(1)
        # Получаем HTML текущей страницы
        page_html = driver.page_source
        # Выводим в консоль результат запроса
        print(f"\n--- Результат для {login} ---")
        print(page_html)
        print("-" * 50)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Ошибка при обработке {login}: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка для {login}: {e}")
        
    time.sleep(1)

    html_form_coupon = """
    <form method="post" action="http://62.173.140.174:36110/coupon">
              <input id="code" name="code" type="text" placeholder="Введите промокод">
              <button type="submit">Применить промокод</button>
            </form>
    """
        
    driver.get("data:text/html;charset=utf-8," + html_form_coupon)

    coupon = "RACE2025"
    
    try:
        # Находим поле ввода и вставляем ссылку
        input_field = driver.find_element(By.ID, "code")
        input_field.clear()
        input_field.send_keys(coupon)

        # Нажимаем кнопку отправки
        submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Применить промокод')]")
        submit_btn.click()
        
        # Ждём загрузки страницы (настройте под свой случай)
        time.sleep(1)

        # Получаем HTML текущей страницы
        page_html = driver.page_source

        # Выводим в консоль результат запроса
        print(f"\n--- Результат для {coupon} ---")
        print(page_html)
        print("-" * 50)
            
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Ошибка при обработке {coupon}: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка для {coupon}: {e}")
    
#def processesed(procs, calc, driver):
def processesed(procs, calc):
    # procs - количество ядер
    # calc - количество операций на ядро
    processes = []
    # делим вычисления на количество ядер
    for proc in range(procs):
        #p = multiprocessing.Process(target=sequential, args=(calc, proc, driver))
        p = multiprocessing.Process(target=sequential, args=(calc, proc))
        processes.append(p)
        p.start()
    # Ждем, пока все ядра 
    # завершат свою работу.
    for p in processes:
        p.join()
        

if __name__ == "__main__":      
    
    # узнаем количество ядер у процессора
    n_proc = multiprocessing.cpu_count()
    print(f"n_proc = ", n_proc)
    # вычисляем сколько циклов вычислений будет приходится
    # на 1 ядро, что бы в сумме получилось 80 или чуть больше
    calc = 6 // n_proc + 1
    #processesed(n_proc, calc, driver)
    processesed(n_proc, calc)
    
    # Закрываем браузер
    driver.quit()