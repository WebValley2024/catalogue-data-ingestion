# Script to download data from NASA's SWIFT satellite
# URL: https://swift.gsfc.nasa.gov/archive/grb_table/fullview/
# The website presents a link under a "<a>" tag next to the text "Download this table as a tab-delimited text file:"
# Everything is under a "<li>" tag

import requests
import csv
from bs4 import BeautifulSoup
from time_related import swift_to_epoch

# TODO: REPLACE TIME UTC WITH EPOCH

def download_swift_data():
    # Set the base URL
    url = "https://swift.gsfc.nasa.gov"

    # Get the page content
    response = requests.get(url + "/archive/grb_table/fullview/")

    # Initialize the download URL
    download_url = None

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the download link
        list_items = soup.find_all("li")
        for item in list_items:
            if "Download this table as a tab-delimited text file:" in item.get_text():
                link = item.find("a")
                download_url = link["href"]
                break
        if not download_url:
            print("Failed to find download link")
            return
        response = requests.get(url + download_url)

        # Make the tab-delimited txt file a CSV file
        with open("swift.csv", "w", encoding="utf-8") as file:
            # replace all n/a with a tab
            data = response.text.replace("n/a", "\t")
            # extract the first column and convert it to epoch
            data_rows = data.strip().split('\n')
            # Process header separately
            header = data_rows[0]
            file.write(header + '\n')
            # Process data rows
            for row in data_rows[1:]:
                fields = row.split('\t')
                fields[1] = str(swift_to_epoch(fields[0], fields[1]))
                converted_row = '\t'.join(fields)
                file.write(converted_row + '\n')
            file.close()
    else:
        print("Failed to download data")
        return
    
if __name__ == "__main__":
    download_swift_data()