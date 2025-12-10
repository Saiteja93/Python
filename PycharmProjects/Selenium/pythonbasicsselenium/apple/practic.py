import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait
product = input("Enter product (iphone, ipad, mac): ").strip().lower()
#model = input("Enter model of selected product: ").strip().lower()
driver = webdriver.Chrome()
driver.maximize_window()
#product = input("Enter product (iphone, ipad, mac): ").strip().lower()
driver.get("https://apple.com")
#wait = WebDriverWait(driver, 20)
#ixpath =  f"(//a[@data-analytics-title='{product}'])"
product_xpath = f"(//div[@class = 'globalnav-menu-list'] / div[@data-analytics-element-engagement = 'globalnav hover - {product}'])"
model_xpath = f"(//li[@data-analytics-gallery-item-id='apple watch se 3'])"


#selected_product = wait.until(EC.element_to_be_clickable((By.XPATH, xpath )))
selected = driver.find_element(By.XPATH, product_xpath)
selected.click()


selected_model = driver.find_element(By.XPATH, model_xpath)
selected_model.click()

driver.find_element(By.XPATH, '//div[@class = "detail-inner-group"]/a/span').click()
#driver.find_element(By.XPATH, "//ul[@class = 'colornav-items']/li/label/span[text()='Midnight']").click()
driver.find_element(By.XPATH, '//ul[@class = "colornav-items"]/li/label/span[text()='Midnight']')
print(selected)
print(selected_model)
time.sleep(10)







                    
