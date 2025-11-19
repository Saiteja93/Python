import time
from select import select

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome()
driver.get("http://www.rahulshettyacademy.com/AutomationPractice/")
options = select(driver.find_elements(By.XPATH, "//select[@id='dropdown-class-example']"))

for option in options:
    if option.get_attribute("value") == "option2":
        option.click()
        assert option.is_selected()
        break

time.sleep(10)








