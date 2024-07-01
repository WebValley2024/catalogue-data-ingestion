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

AGILE_MISSION_START = datetime.strptime("April 23, 2007 10:00:00 GMT", "%B %d, %Y %H:%M:%S %Z")


def download_agile_data():
    """
    Downloads data from Agile and saves it as a CSV file.
    """
    url = "https://www.ssdc.asi.it/mcal3tgfcat/"

    # Set Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-javascript")
    options.add_argument("--enable-user-scripts")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-gpu")

    # Initialize Chrome driver
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait until page is fully loaded
    while True:
        page_state = driver.execute_script('return document.readyState;')
        if page_state == 'complete':
            break

    # Execute JavaScript to manipulate webpage
    # Select all checkboxes
    driver.execute_script("document.forms['form_table_choix'].elements['selectAll'].checked = true;")
    driver.execute_script("select_deselect_all(document.forms['form_table_choix'].elements['selectAll']);")

    time.sleep(1)

    # Apply checkbox selection
    driver.execute_script("update_table_columns()")
    time.sleep(10)

    # Export CSV data
    driver.execute_script("exportCSV()")

    # Switch to new tab containing CSV data
    driver.switch_to.window(driver.window_handles[1])

    # Wait for the CSV data to be loaded
    time.sleep(5)

    # Get HTML content
    html = driver.page_source

    # Parse HTML content
    soup = BeautifulSoup(html, "html.parser")

    # Find all text blocks divided by <br> tags
    text_blocks = soup.body.decode_contents().split('<br/>')

    # Write CSV data to file
    with open("agile.csv", "w", newline='', encoding='utf-8') as file:
        is_header = True  # Flag to check if current row is header
        for block in text_blocks:
            try:
                # Strip HTML tags and split text by comma
                soup_block = BeautifulSoup(block, "html.parser")
                text = soup_block.get_text().strip()
                row = [element.strip() for element in text.split(",")]
                # Remove first and last empty elements
                row = row[2:-2]
                row.pop(4)
                row.pop(7)
                for i in range(4):
                    row.pop(11)

                if is_header:
                    # Rename headers
                    row[3] = "Trigger Time"
                    row[-2] = "TGF Name"
                    row.append("Normalised Duration")
                    # Normalize and remove non-ASCII characters
                    row = [
                        unicodedata.normalize("NFKD", cell).encode("ascii", "ignore").decode("utf-8")
                        for cell in row
                    ]

                else:
                    # Convert date from UTC to EPOCH
                    row[3] = '"' + str(int(datetime.strptime(row[3].strip('"'), "%Y-%m-%dT%H:%M:%S").timestamp())) + '"'
                    row.append(float(row[4].replace('"', '')) * 2)
                    row[-1] = str(row[-1])

                # Write row to CSV file
                row = [cell.replace('"', '') for cell in row]
                file.write(",".join(row) + "\n")
                is_header = False  # After first iteration, no more header

            except IndexError:
                pass

    # Close the driver
    driver.quit()


if __name__ == "__main__":
    download_agile_data()
