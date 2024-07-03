from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime, timedelta


def is_leap_year(year):
    # Check if a year is a leap year
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def day_of_year_to_date(year, day):
    # Determine the corresponding month and day for a given day of the year
    # Use a list of the number of days in each month
    days_in_month = [31, 29 if is_leap_year(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month = 1
    while day > days_in_month[month - 1]:
        day -= days_in_month[month - 1]
        month += 1
    return month, day


def to_epoch_timestamp(year, day, hour, minute):
    # Convert the given parameters to an epoch timestamp
    month, day = day_of_year_to_date(year, day)
    dt = datetime(year, month, day, hour, minute)
    # Convert the datetime to an epoch timestamp
    epoch_timestamp = int(dt.timestamp())
    return str(epoch_timestamp)


def download_dst_data():
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

        # Wait until the form is loaded and input fields are present
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, 'start_date')))
        wait.until(EC.presence_of_element_located((By.NAME, 'end_date')))

        end_date = "20240606"
        start_date = f"{end_date[:3]}{int(end_date[3]) - 1}{end_date[4:]}"

        # Locate the start date input field and set its value
        start_date_input = driver.find_element(By.NAME, 'start_date')
        start_date_input.clear()
        start_date_input.send_keys(start_date)  # Set the desired start date

        # Locate the end date input field and set its value
        end_date_input = driver.find_element(By.NAME, 'end_date')
        end_date_input.clear()
        end_date_input.send_keys(end_date)  # Set the desired end date

        # Select the second radio button ('List data')
        list_radio_button = driver.find_element(By.CSS_SELECTOR, 'input[type="radio"][value="ftp"]')
        list_radio_button.click()

        # Click the submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Submit"]')
        submit_button.click()

        # Wait for the second page to load and get its content
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        second_page_content = driver.page_source

        soup = BeautifulSoup(second_page_content, 'html.parser')
        lst_link = soup.find('a').get('href')

        try:
            response = requests.get(lst_link)
        except Exception as e:
            print("Could not get the data (check the data range)")
            sys.exit(0)

        if response.status_code == 200:
            file_content = response.text

            header = ["Trigger Time", "Field Magnitude Average(nT)", "Speed(km/s)"]

            rows = file_content.split('\n')

            for i in range(len(rows)-1):
                parts = list(filter(None, rows[i].split(' ')))
                parts[0] = to_epoch_timestamp(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
                parts.pop(1)
                parts.pop(1)
                parts.pop(1)

                rows[i] = ','.join(parts)

            with open("dst.csv", "w") as dst:
                dst.write(f"{','.join(header)}\n")
                for row in rows[:-1]:
                    dst.write(f"{row}\n")

        else:
            print(f"Failed to retrieve the file: {response.status_code}")

    finally:
        # Close the WebDriver
        driver.quit()


if __name__ == "__main__":
    download_dst_data()
