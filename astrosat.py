from bs4 import BeautifulSoup
import requests
import csv
import datetime


def add_cols(cols):
    """
    Extracts content from HTML elements and returns a list of extracted data.
    """
    list = []

    # Loop through the HTML elements
    for ele in cols:
        # Initialize content variable
        content = ""

        # Check if the element contains a link and extract the URL
        if ele.find('a'):
            content = ele.find('a').get('href')

        # Check if the element contains a paragraph and extract text
        elif ele.find('p'):
            paragraphs = ele.find_all('p')
            for p in paragraphs:
                content += p.find('strong').text

        else:
            # Extract text content if no specific tag found
            content = ele.text.strip()

        # Append extracted content to list
        list.append(content)

    return list


def download_astrosat_data():
    """
    Downloads data from Astrosat and saves it as a CSV file.
    """
    url = "https://astrosat.iucaa.in/czti/grb"

    # Get the webpage content
    page = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find the table containing data
    table = soup.find('table')

    # Find all rows in the table
    rows = table.find_all('tr')

    # Save the table as a CSV file
    with open('astrosat.csv', 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_NONE, escapechar='\\',
                                skipinitialspace=True, doublequote=False)

        # Process the first row (headers) separately
        if rows:
            first_row = rows[0]
            td_elements = first_row.find_all('td')  # Find all 'td' elements in the first row

            headers_text = []
            for td in td_elements:
                # Extract headers within the same 'td' and join them with a space
                headers = td.find_all(['th', 'strong'])  # Look for 'th' or 'strong' within each 'td'
                joined_headers = ' '.join(header.text for header in headers)
                headers_text.append(joined_headers)

            # Remove the last element from headers_text as it is empty
            headers_text = headers_text[:-1]

            # Append additional headers and modify existing headers
            headers_text += ["CZT", "Veto", "Compton"]
            headers_text[3] = 'Trigger Time'

            # Remove unnecessary columns by index
            headers_text.pop(11)
            headers_text.pop(10)
            headers_text.pop(9)
            headers_text.pop(7)
            headers_text.pop(6)
            headers_text.pop(2)
            headers_text.pop(0)

            headers_text[2] = "Ra"
            headers_text[3] = "Dec"
            headers_text[4] = "T90(sec)"

            headers_text.append("Normalised Duration")

            # Write modified headers to the CSV file
            csv_writer.writerow(headers_text)

            # Remove the first row (headers) from further processing
            rows = rows[1:]

        # Loop through the remaining rows to extract and process data
        for row in rows:
            # Extract columns from the row
            cols = row.find_all('td')

            # Process and extract data from columns using add_cols function
            row_data = add_cols(cols)

            # Convert datetime string to timestamp and then to integer
            row_data[3] = datetime.datetime.strptime(row_data[3], "%Y-%m-%d %H:%M:%S").timestamp()
            row_data[3] = int(row_data[3])

            # Remove unnecessary columns by index
            row_data.pop(11)
            row_data.pop(10)
            row_data.pop(9)
            row_data.pop(7)
            row_data.pop(6)
            row_data.pop(2)
            row_data.pop(0)

            row_data.append(row_data[4])

            # Write processed row data to the CSV file
            csv_writer.writerow(row_data)


if __name__ == "__main__":
    download_astrosat_data()
