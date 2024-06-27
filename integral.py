from bs4 import BeautifulSoup
import requests
import datetime
import threading
from dateutil.relativedelta import relativedelta

# TODO: REPLACE TIME UTC WITH EPOCH

# Create a lock object
lock = threading.Lock()

def thread_wrapper(url, filename, headers):
    extract_table(url, filename, headers)

threads = []

def extract_table(url, filename, headers=False):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all('table')
    table = tables[1]
    rows = table.find_all('tr')
    
    # Acquire the lock before writing to the file
    with lock:
        with open(filename, 'a') as f:
            for row in rows:
                if headers and row.find('th'):
                    cols = row.find_all('th')
                    cols = [ele.text.strip() for ele in cols]
                    f.write(','.join(cols) + '\n')
                    continue
                if row.find('td'):
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    f.write(','.join(cols) + '\n')

def download_integral_data():
    filename = 'integral.csv'
    URL = "https://www.isdc.unige.ch/integral/ibas/cgi-bin/ibas_acs_web.cgi"

    date = datetime.datetime(2002, 10, 1)
    lastdate = datetime.datetime.now()

    headers = True
    while (date.year != lastdate.year or date.month != lastdate.month + 1):

        if (date != datetime.datetime(2002, 10, 1)):
            headers = False
            thread = True
        else:
            headers = True
            thread = False
        if (date.month < 10):
            URL_table = URL + "?month=" + str(date.year) + "-0" + str(date.month) + "&showall=on"
        else: 
            URL_table = URL + "?month=" + str(date.year) + "-" + str(date.month) + "&showall=on"
        print(URL_table)
        if not thread:
            extract_table(URL_table, filename, headers)
        else:
            t = threading.Thread(target=thread_wrapper, args=(URL_table, filename, headers))
            t.start()  # Start the thread
            threads.append(t)

        date += relativedelta(months=1)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Order the data by date
    with open(filename, 'r') as f:
        data = f.readlines()
        headers = data[0]

    data = data[1:]
    # Remove the headers from the data
    for i in range(len(data)):
        if headers in data[i]:
            data.pop(i)
    # Order the data by date
    data.sort(key=lambda x: (
        datetime.datetime.strptime(x.split(',')[0].split()[0], '%Y-%m-%d'),
        datetime.datetime.strptime(x.split(',')[0].split()[1], '%H:%M:%S')
    ))

    # Write the ordered data to a new file
    with open(filename, 'w') as f:
        f.write(headers)
        f.write(''.join(data))

if __name__ == "__main__":
    download_integral_data()