import time
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://rahulshettyacademy.com")
driver.maximize_window()
title = driver.title
print(title)
print(driver.current_url)

time.sleep(5)
