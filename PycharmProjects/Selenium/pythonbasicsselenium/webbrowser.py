from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By # For locating elements
from selenium.webdriver.chrome.options import Options # For browser options
import time # For demonstration pauses

# --- Recommended Setup for Chrome WebDriver ---
# 1. Specify the path to your ChromeDriver executable
#    If ChromeDriver is in your system's PATH, you might not need this line.
#    Otherwise, download it from https://chromedriver.chromium.org/downloads
#    and provide its path. Make sure the ChromeDriver version matches your Chrome browser version.
# service = Service(executable_path="/path/to/your/chromedriver") # Uncomment and set your path

# 2. (Optional) Set up Chrome options (e.g., headless mode)
# options = Options()
# options.add_argument("--headless") # Run Chrome in headless mode (without opening a visible browser window)
# options.add_argument("--no-sandbox") # Recommended for CI/CD environments
# options.add_argument("--disable-dev-shm-usage") # Recommended for Docker/Linux environments

try:
    # Initialize the Chrome WebDriver
    # If you used 'service' and 'options', pass them here:
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome() # Simpler if chromedriver is in PATH and no options are needed

    print("WebDriver initialized successfully.")

    # --- CORRECT WAY TO OPEN A URL ---
    driver.get("https://www.rahulshettyacademy.com")
    print(f"Opened: {driver.current_url}")

    # --- CORRECT WAY TO INTERACT WITH ELEMENTS ---
    # Find the search box by its name attribute and type something
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("india vs england test cricket score")
    print("Typed 'india vs england test cricket score.")

    # Find the Google Search button and click it
    # Note: Google's button might have different values over time, 'btnK' is common.
    # You might need to inspect the element on Google.com to get the exact name/value.
    # Often, just pressing ENTER after typing in the search box works too.
    # search_button = driver.find_element(By.NAME, "btnK")
    # search_button.click()
    search_box.submit() # A common way to submit a form after typing

    print("Search submitted.")
    time.sleep(15) # Wait for 15 seconds to see the results

    # Print the title of the new page
    print(f"Page title after search: {driver.title}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Always close the browser when done
    if 'driver' in locals() and driver: # Check if driver object was successfully created
        driver.quit()
        print("Browser closed.")