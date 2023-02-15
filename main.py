import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
#automate webbrowser
s = Service("C:/Users/shree/Desktop/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service = s, options = options)

#open smartprix link
driver.get("https://www.smartprix.com/mobiles")

#filter mobile phones on smartprix
link1 = driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/aside/div/div[5]/div[2]/label[1]/input')
link1.click()
link2 = driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/aside/div/div[5]/div[2]/label[2]/input')
link2.click()

#Load all the pages
old_height = driver.execute_script('return document.body.scrollHeight')
print(old_height)

while True:
    driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/div[1]/div[2]/div[3]').click()
    time.sleep(2.5)
    new_height = driver.execute_script('return document.body.scrollHeight')
    print(new_height)
    if old_height == new_height:
        break
    else:
        old_height = new_height

#extract html using beautifulsoup
html = driver.page_source
with open('smartprix.html', 'w', encoding = 'utf-8') as f:
    f.write(html)

