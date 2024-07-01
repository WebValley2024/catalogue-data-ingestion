from bs4 import BeautifulSoup
from time_related import konus_to_epoch
from rich import print
import cloudscraper
import time
import csv

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
    # Create a cloudscraper instance
    scraper = cloudscraper.create_scraper()
    try:
        page = scraper.get(url)
    except Exception as e:
        print(f"<konus> [bold red]Error while downloading data[/bold red] -- URL: {url} -- [bold yellow]RETRYING[/bold yellow]: ", e)
        try:
            time.sleep(5)
            page = scraper.get(url)
        except Exception as e:
            print(f"<konus> [bold red]Error while downloading data[/bold red] -- URL: {url}: ", e)
            return None
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')

    with open("konus.csv", mod, newline='') as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\', skipinitialspace=True, doublequote=False)
        rows[0] = ["Trigger Time", "Type"]
        if mod == 'w':
            csv_writer.writerow(rows[0])

        for row in rows[1:]:
            cols = row.find_all('td')[:6]
            row_data = add_cols(cols)
            row_data.pop(1)
            row_data.pop(2)
            row_data.pop(-1)
            if row_data[2] == "" or row_data[2] == "GRB":
                try:
                    timestamp = konus_to_epoch(row_data[0], row_data[1])
                    row_data[0] = timestamp
                    row_data.pop(1)
                    csv_writer.writerow(row_data)
                except:
                    # This row may not be in the correct format, instead of being '.' it may be ':'
                    # This is a workaround to fix the issue
                    print("Error: ", row_data)
                    try:
                        row_data[1] = row_data[1].rsplit(':', 1)[0] + '.' + row_data[1].rsplit(':', 1)[1]
                        timestamp = konus_to_epoch(row_data[0], row_data[1])
                        row_data[0] = timestamp
                        row_data.pop(1)
                        csv_writer.writerow(row_data)
                        print("Fixed: ", row_data)
                    except:
                        # If the row is still not in the correct format, skip it
                        print("Still error: ", row_data)
                        pass


def download_konus_data():
    url = "https://gcn.gsfc.nasa.gov/konus_grbs.html"
    # print("Today --> 2020")
    download_data(url, 'w')

    for year in range(2019, 1993, -1):
        url = f"https://gcn.gsfc.nasa.gov/konus_{year}grbs.html"
        # print(year)
        download_data(url, 'a')

if __name__ == "__main__":
    download_konus_data()