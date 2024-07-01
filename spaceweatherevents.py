import cloudscraper
from datetime import datetime
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from time_related import datetime_to_epoch


def download_space_weather_data():
    """
    Downloads data from Space Weather Events and saves it as a CSV file.
    """
    base_url = "https://www.spaceweatherlive.com"

    # Set the URL of the website
    url = base_url + "/en/solar-activity/top-50-solar-flares/year/"

    # File name
    file_name = "spaceweatherevents.csv"

    # Create a cloudscraper instance
    scraper = cloudscraper.create_scraper()

    # Empty the CSV file
    with open(file_name, "w", newline="") as f:
        f.write("")
        f.close()

    # Loop through the years from 1996 to 2024
    for year in range(1996, datetime.now().year + 1):
        # Get the page content using cloudscraper
        response = scraper.get(url + str(year) + ".html")

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the table
            table = soup.find("table")

            # Find all the rows in the table
            rows = table.find_all("tr")

            # Save to the same CSV file
            with open(file_name, "a", newline="") as f:
                csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\', skipinitialspace=True, doublequote=False)
                if year == 1996:
                    # Process the first row (headers) separately
                    first_row = rows[0]
                    th_elements = first_row.find_all("th")
                    headers = [th.text for th in th_elements]
                    headers.pop(2)
                    headers[0] = "Top"
                    headers[1] = "Flux"
                    headers[4] = "Trigger Time"
                    headers[5] = "End"
                    headers[6] = "Links"

                    csv_writer.writerow(headers)
                rows = rows[1:]
                # Loop through the remaining rows
                for row in rows:
                    # Extract the columns from the row
                    cols = row.find_all("td")
                    # Extract the text content from all but the last column
                    row_data = [col.text.strip() for col in cols[:-1]]  # Use strip() to remove leading/trailing whitespace

                    date = row_data[2]
                    row_data.pop(2)

                    row_data[3] = datetime_to_epoch(date, row_data[3])
                    row_data[4] = datetime_to_epoch(date, row_data[4])
                    row_data[5] = datetime_to_epoch(date, row_data[5])

                    # For the last column, check if there is an <a> tag to extract the link
                    last_col = cols[-1].find('a')
                    if last_col and 'href' in last_col.attrs:
                        last_col_data = base_url + last_col['href']
                    else:
                        last_col_data = 'No link'  # Use a placeholder if no link is present
                    # Add the link or placeholder to the row data
                    row_data.append(last_col_data)
                    # Write the row data to the CSV file
                    csv_writer.writerow(row_data)
        else:
            print("Failed to download data for year", year)


if __name__ == "__main__":
    download_space_weather_data()
