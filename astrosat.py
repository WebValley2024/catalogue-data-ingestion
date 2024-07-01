from bs4 import BeautifulSoup
import requests
import csv
import datetime

def add_cols(cols):
    """
    Extracts content from HTML elements and adds them to a list.

    Args:
        cols (list): A list of HTML elements.

    Returns:
        list: A list containing the extracted content from the HTML elements.
    """
    l = []
    
    # Loop through the HTML elements
    for ele in cols:
        # Extract the content from the HTML element
        content = ""
        # Check if the element is a link and extract the URL
        if (ele.find('a')):
            content = ele.find('a').get('href')
        # Check if the element is a paragraph and extract the text
        elif (ele.find('p')):
            paragraphs = ele.find_all('p')
            for p in paragraphs:
                content += p.find('strong').text 
        else:
            content = ele.text.strip()
        # Append the content to the list
        l.append(content)
    return l

def download_astrosat_data():
    url = "https://astrosat.iucaa.in/czti/grb"
    filename = 'astrosat.csv'
    # Get the page content
    page = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(page.content, 'html.parser')
    # Find the table
    table = soup.find('table')
    # Find all the rows in the table
    rows = table.find_all('tr')

    # Save the table as a CSV file
    with open(filename, 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\', skipinitialspace=True, doublequote=False)
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
            # Remove last element from headers_text as it is empty
            headers_text = headers_text[:-1]
            # Append additional headers
            headers_text += ["CZT", "Veto", "Compton"]
            headers_text[3] = 'Trigger Time'

            headers_text.pop(11)
            headers_text.pop(10)
            headers_text.pop(9)
            headers_text.pop(7)
            headers_text.pop(6)
            headers_text.pop(2)
            headers_text.pop(0)

            # Write the modified headers to the CSV
            csv_writer.writerow(headers_text)
            # Remove the first row (headers) from processing
            rows = rows[1:]
        # Loop through the remaining rows
        for row in rows:
            # Extract the columns from the row
            cols = row.find_all('td')

            # Use add_cols to process and extract data from columns
            row_data = add_cols(cols)

            row_data[3] = datetime.datetime.strptime(row_data[3], "%Y-%m-%d %H:%M:%S").timestamp()
            row_data[3] = int(row_data[3])

            row_data.pop(11)
            row_data.pop(10)
            row_data.pop(9)
            row_data.pop(7)
            row_data.pop(6)
            row_data.pop(2)
            row_data.pop(0)

            # Write the row data to the CSV file
            csv_writer.writerow(row_data)

if __name__ == "__main__":
    download_astrosat_data()

