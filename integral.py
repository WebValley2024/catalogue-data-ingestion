from bs4 import BeautifulSoup
import requests
import datetime
import threading
from dateutil.relativedelta import relativedelta
import time

# Create a lock object
lock = threading.Lock()

def thread_wrapper(url, filename, headers, first_write):
    extract_table(url, filename, headers, first_write)

threads = []

def extract_table(url, filename, headers=False, first_write=False):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all('table')
    table = tables[1]
    rows = table.find_all('tr')
    
    # Determine the file mode
    mode = 'w' if first_write else 'a'
    
    # Acquire the lock before writing to the file
    with lock:
        with open(filename, mode) as f:
            for row in rows:
                if headers and row.find('th'):
                    cols = row.find_all('th')
                    cols = [ele.text.strip() for ele in cols]
                    f.write(','.join(cols) + '\n')
                    continue
                if row.find('td'):
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    
                    # Extract and convert datetime to epoch timestamp
                    try:
                        dt_string = cols[0].split()[0] + ' ' + cols[0].split()[1]
                        dt = datetime.datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
                        epoch_time = int(time.mktime(dt.timetuple()))
                        cols[0] = str(epoch_time)
                    except ValueError:
                        pass
                    
                    f.write(','.join(cols) + '\n')

def download_integral_data():
    filename = 'integral.csv'
    URL = "https://www.isdc.unige.ch/integral/ibas/cgi-bin/ibas_acs_web.cgi"

    date = datetime.datetime(2002, 10, 1)
    lastdate = datetime.datetime.now()

    first_write = True
    headers = True
    while (date.year != lastdate.year or date.month != lastdate.month + 1):

        if (date != datetime.datetime(2002, 10, 1)):
            headers = False
            thread = True
        else:
            headers = True
            thread = False

        if date.month < 10:
            URL_table = URL + "?month=" + str(date.year) + "-0" + str(date.month) + "&showall=on"
        else: 
            URL_table = URL + "?month=" + str(date.year) + "-" + str(date.month) + "&showall=on"
        
        if not thread:
            extract_table(URL_table, filename, headers, first_write)
        else:
            t = threading.Thread(target=thread_wrapper, args=(URL_table, filename, headers, first_write))
            t.start()  # Start the thread
            threads.append(t)

        date += relativedelta(months=1)
        first_write = False

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Order the data by date
    with open(filename, 'r') as f:
        data = f.readlines()
        headers = data[0]

    # Filter out the headers from the data
    data = [line for line in data if headers not in line]
    
    # Order the data by date (using epoch timestamp)
    data.sort(key=lambda x: int(x.split(',')[0]))

    # Write the ordered data to a new file
    with open(filename, 'w') as f:
        f.write(headers)
        f.write(''.join(data))

if __name__ == "__main__":
    download_integral_data()
