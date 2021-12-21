from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml
import time

chrome_driver_path = "H:\Python_Study\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

SHEET_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdDA0c48GptaefE3J6HAI3OX8NAeYQBubeowzJZNQABlNcSNQ/viewform?usp=sf_link"

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417281103516%2C%22east%22%3A-122.23248518896484%2C%22south%22%3A37.701442270103186%2C%22north%22%3A37.84906694324912%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
ACCEPT_LANG = "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5,fr;q=0.4"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

REQUEST_HEADER = {
    "User-Agent":USER_AGENT,
    "Accept-Language":ACCEPT_LANG
}


response = requests.get(test_url,headers=REQUEST_HEADER)
web_info = response.text

soup = BeautifulSoup(web_info, "html.parser")

listings_price = soup.find_all(class_="list-card-price")
listings_addr = soup.find_all("address",class_="list-card-addr")
listings_link = soup.find_all("a",class_="list-card-link")


price = [price.getText() for price in listings_price]
address = [addr.getText() for addr in listings_addr]
links = [link['href'] for link in listings_link]
links = list(dict.fromkeys(links))
for n in range(len(links)):
    if "http" not in links[n]:
        links[n] = "https://www.zillow.com"+links[n]
    if "/" in price[n]:
        price[n] = price[n].split("/",1)[0]
    if "+" in price[n]:
        price[n] = price[n].split("+",1)[0]


for n in range(len(price)):
    driver.get(url=SHEET_URL)
    time.sleep(3)
    prop_price = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prop_price.send_keys(price[n])
    prop_addr = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prop_addr.send_keys(address[n])
    prop_link = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prop_link.send_keys(links[n])
    button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    button.click()
