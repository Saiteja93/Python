import time
from select import select

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome()
driver.get("http://www.rahulshettyacademy.com/angularpractice/")
driver.maximize_window()
driver.find_element(By.CSS_SELECTOR, "input[name = 'name']").send_keys("SAI")
driver.find_element(By.NAME, 'email').send_keys("saitejaraj.guvvala@gmail.com")
driver.find_element(By.ID,'exampleInputPassword1').send_keys("1234")
dropdown = Select(driver.find_element(By.ID,'exampleFormControlSelect1'))
dropdown.select_by_visible_text("Female")
driver.find_element(By.XPATH, "//input[@type='submit']").click()
message = driver.find_element(By.CLASS_NAME, "alert-success").text
print (message)
time.sleep(15)