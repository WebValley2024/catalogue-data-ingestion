# Script to download data from NASA's SWIFT satellite
# URL: https://swift.gsfc.nasa.gov/archive/grb_table/fullview/
# Extract the table data and save it as a CSV file

import requests
from bs4 import BeautifulSoup
import csv
from time_related import swift_to_epoch

def download_swift_data():
    # Set the base URL
    url = "https://swift.gsfc.nasa.gov"

    # Get the page content
    response = requests.get(url + "/archive/grb_table/fullview/")

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Assuming the table is the first or only table in the page
        table = soup.find("table")
        rows = table.find_all("tr")
        
        # Extracting header
        headers = [header.text for header in rows[0].find_all("th")]

        # Remove the 32th column from the header (Comments column)
        headers.pop(32)

        # Remove all other instances of the same header (<thead> tag) and leave only the first one
        for index, thead in enumerate(table.find_all("thead")):
            if index != 0:
                thead.decompose()

        # Replace the first header with "Trigger Time"
        headers[0] = "Trigger Time"
        
        # Write the CSV data to a file
        with open("swift.csv", "w", encoding="utf-8", newline='') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)  # Write the header
            
            for row in rows[1:]:  # Skip header row
                cols = [ele.text.strip().replace(";", ",") for ele in row.find_all(["td", "th"])]
                cols = [col if col != "n/a" else "" for col in cols]
                if cols:  # If the row was not empty
                    cols.pop(32) # Remove the 32th column (Comments column)
                    # Convert the date to epoch time
                    cols[1] = str(swift_to_epoch(cols[0], cols[1]))
                    writer.writerow(cols)
    else:
        print("Failed to download data")
        return
    
if __name__ == "__main__":
    download_swift_data()