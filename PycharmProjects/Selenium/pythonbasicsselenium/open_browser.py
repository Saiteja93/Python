import time
from selenium import webdriver
driver = webdriver.Chrome()

#driver.get("http://www.rahulshettyacademy.com/angularpractice/")
driver.get("https://www.apple.com/")



driver.maximize_window()
time.sleep(2)
print(driver.title)

url = driver.current_url
print(url)