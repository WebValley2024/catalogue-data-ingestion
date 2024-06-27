from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime, timezone


def convert_to_epoch(date_str, time_str):
    date_obj = datetime.strptime(date_str, "%Y%m%d")
    
    # Parse the time string without timezone abbreviation
    time_obj = datetime.strptime(time_str.split()[0], "%H:%M:%S.%f")
    
    # Combine date and time
    combined_datetime = datetime.combine(date_obj.date(), time_obj.time())
    
    # Manually convert to UTC timezone aware datetime object
    combined_utc = combined_datetime.replace(tzinfo=timezone.utc)
    
    # Convert to epoch timestamp
    epoch_timestamp = int(combined_utc.timestamp())
    
    return epoch_timestamp


def add_cols(cols):
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


def download_data(url, mod):


    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table')


    rows = table.find_all('tr')

    with open("konus.csv", mod, newline='') as file:
        csv_writer = csv.writer(file)
        rows[0] = ["Trigger Time", "Det", "Event", "Trig"]
        if mod == 'w':
            csv_writer.writerow(rows[0])

        for row in rows[1:]:
            cols = row.find_all('td')[:6]
            row_data = add_cols(cols)
            row_data.pop(1)
            try:
                timestamp = convert_to_epoch(row_data[0], row_data[1])
                row_data[0] = timestamp
                row_data.pop(1)
                csv_writer.writerow(row_data)
            except:
                print("error")


if __name__ == "__main__":
    url = "https://gcn.gsfc.nasa.gov/konus_grbs.html"
    download_data(url, 'w')


    for year in range(2019, 1993, -1):
        url = f"https://gcn.gsfc.nasa.gov/konus_{year}grbs.html"
        print(year)
        download_data(url, 'a')
