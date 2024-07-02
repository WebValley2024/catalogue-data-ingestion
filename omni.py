from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests



options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--enable-javascript")
options.add_argument("--enable-user-scripts")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-gpu")
# Initialize the WebDriver (here using Chrome)
driver = webdriver.Chrome(options=options)

try:
    # Open the webpage
    driver.get('https://omniweb.gsfc.nasa.gov/form/omni_min.html')  # Replace with the actual URL

    # Wait until the form is loaded and radio buttons are clickable
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.NAME, 'activity')))

    # Select the second radio button ('List data')
    list_radio_button = driver.find_element(By.CSS_SELECTOR, 'input[type="radio"][value="ftp"]')
    list_radio_button.click()

    list_radio_button2 = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Submit"]')
    list_radio_button2.click()



    # Submit the form if needed (depends on the form setup)
    # form = driver.find_element(By.NAME, 'frm')
    # form.submit()

    # Or click the submit button directly if there's one
    # submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    # submit_button.click()

    # Wait for the second page to load and get its content
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    second_page_content = driver.page_source

    soup = BeautifulSoup(second_page_content, 'html.parser')
    lst_link = soup.find('a').get('href')
    

    
    print(lst_link)
    response = requests.get(lst_link)
    if response.status_code == 200:
        file_content = response.text
        with open("omni.txt", "w") as omni:
            omni.write(file_content)
    else:
        print(f"Failed to retrieve the file: {response.status_code}")

finally:
    # Close the WebDriver
    driver.quit()
