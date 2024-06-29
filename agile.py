# Script to extract CSV data from a website using Selenium (because of JavaScript)
# and BeautifulSoup (for parsing the HTML)
# This script is for the website https://www.ssdc.asi.it/mcal3tgfcat/

import time
import unicodedata
import warnings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from time_related import utc_to_epoch
from datetime import datetime

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

AGILE_MISSION_START = datetime.strptime("April 23,2007 10:00:00 GMT", "%B %d,%Y %H:%M:%S %Z")

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

    # Execute JavaScript functions
    # Select all the checkboxes
    driver.execute_script("document.forms['form_table_choix'].elements['selectAll'].checked = true;")
    driver.execute_script("select_deselect_all(document.forms['form_table_choix'].elements['selectAll']);")
    time.sleep(1)
    # Apply the checkbox selection
    driver.execute_script("update_table_columns()")
    time.sleep(10)
    # Export the CSV data
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
    
    # Find all text blocks divided by <br> tags
    # This assumes `soup` is the parsed HTML of the entire document
    text_blocks = soup.body.decode_contents().split('<br/>')
    
    # Write the CSV data to a file
    with open("agile.csv", "w", newline='', encoding='utf-8') as file:
        is_header = True  # Flag to check if the current row is the header
        for block in text_blocks:
            try:
                # Strip and split each block of text by comma after removing HTML tags
                soup_block = BeautifulSoup(block, "html.parser")
                text = soup_block.get_text().strip()  # Get clean text without HTML tags
                row = [element.strip() for element in text.split(",")]
                row = row[2:-2]  # Remove the first and last element which is an empty string
                row.pop(4)
                row.pop(7)
                for i in range(4):
                    row.pop(11)
                if is_header:
                    # Modify the header of 4 cell of "Date (UTC)" to "Date (EPOCH)"
                    row[3] = "Trigger Time"
                    row = [unicodedata.normalize("NFKD", cell).encode("ascii", "ignore").decode("utf-8") for cell in row]
                    pass

                if not is_header:
                    # Convert the date from UTC to EPOCH
                    row[3] = '"' + str(utc_to_epoch(datetime.strptime(row[3].lstrip('"').rstrip('"'), "%Y-%m-%dT%H:%M:%S")))[:-2] + '"'
                try:
                    row = [cell.replace('"', '') for cell in row]
                    file.write(",".join(row) + "\n")
                except Exception as e:
                    print(f"Error writing row: {row} - {e}")
                is_header = False  # After the first iteration, no more header
            except IndexError as e:
                pass

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    download_agile_data()