# Script to extract CSV data from a website using Selenium (because of JavaScript)
# and BeautifulSoup (for parsing the HTML)
# This script is for the website https://www.ssdc.asi.it/mcal3tgfcat/

# TODO: FIX AGILE CSV EXTRACTION BECAUSE SOME COLUMNS ARE BROKEN

import os
import time
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def download_agile_data():
    # Set the URL of the website
    url = "https://www.ssdc.asi.it/mcal3tgfcat/"

    # Set the path to the ChromeDriver executable
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-javascript")
    options.add_argument("--enable-user-scripts")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-gpu")

    # Set the driver
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    while True:
        page_state = driver.execute_script('return document.readyState;')
        if page_state == 'complete':
            break

    driver.execute_script("exportCSV()")

    # A new tab (about:blank) will be opened with the CSV data
    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[1])

    # Wait for the CSV data to be loaded
    time.sleep(5)

    # Get the HTML content
    html = driver.page_source

    # Parse the HTML content
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("body")

    # Get the text content of the body
    text = body.get_text()

    # Split the text content by lines
    lines = text.split("\r\n")

    # Write the CSV data to a file
    with open("agile.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(lines[0].split(","))
        for line in lines[1:]:
            writer.writerow(line.split(","))

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    download_agile_data()