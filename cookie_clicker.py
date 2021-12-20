from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

chrome_driver_path = "H:\Python_Study\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

time_interval = 5
start_time = time.time()
end_game = start_time + 60 * 2

driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element_by_id("cookie")

store = driver.find_elements_by_css_selector("#store b")[0:8]

items = [''.join(filter(str.isdigit,item.text.strip("[,]-'"))) for item in store]

i_gameon = True

while i_gameon:
    cookie.click()
    if time.time() - start_time >= time_interval:
        money = int(driver.find_element_by_id("money").text)
        store = driver.find_elements_by_css_selector("#store b")[0:8]
        items = [''.join(filter(str.isdigit,item.text.strip("[,]-'"))) for item in store]
        item_price = []
        for item in items:
            item_price.append(''.join(filter(str.isdigit, item)))
        for n in range(len(item_price)-1,-1,-1):
            if money > int(item_price[n]):
                store[n].click()
                print(f"click {n}")
                break

        start_time = time.time()
    if time.time() > end_game:
        i_gameon = False
        cps = driver.find_element_by_id("cps")
        print(cps.text)


