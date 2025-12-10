from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.apple.com/")
driver.maximize_window()
driver.implicitly_wait(15)


#driver.find_element(By.XPATH, '//*[@id="globalnav-list"]/li[2]/div/div/div[3]/ul/li[1]/a/span[1]').click()
#driver.find_element(By.XPATH, '//*[@id = "globalnav-list"]/li[2]/div/div/div[3]').click()
#driver.find_element(By.XPATH, "//a[contains(@data-analytics-title, 'ipad')]").click()
driver.find_element(By.XPATH, "//a[(@data-analytics-title = 'ipad')]/span[1]").click()
driver.execute_script("window.scrollBy(0,2500);")
driver.find_element(By.XPATH, "//a[@href = '/ipad-pro/']/span/div/figure/picture").click()


time.sleep(5)


'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.apple.com/")
driver.maximize_window()

wait = WebDriverWait(driver, 15)

ipad_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@data-analytics-title='ipad']"))
)

# Use JavaScript click to avoid "not interactable" issues
driver.execute_script("arguments[0].click();", ipad_link)

'''