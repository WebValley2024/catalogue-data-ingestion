import threading
from time import strftime, localtime, time
from bs4 import BeautifulSoup
import requests
import csv
from datetime import timedelta, datetime, timezone
import requests
import pandas as pd
from time_related import mjd_to_epoch
import warnings
from dateutil.relativedelta import relativedelta
from rich import print
import cloudscraper

def konus_to_epoch(date_str, time_str):
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
                    # print("Error: ", row_data)
                    try:
                        row_data[1] = row_data[1].rsplit(':', 1)[0] + '.' + row_data[1].rsplit(':', 1)[1]
                        timestamp = konus_to_epoch(row_data[0], row_data[1])
                        row_data[0] = timestamp
                        row_data.pop(1)
                        csv_writer.writerow(row_data)
                        # print("Fixed: ", row_data)
                    except:
                        # If the row is still not in the correct format, skip it
                        # print("Still error: ", row_data)
                        pass


def download_konus_data():
    """
    Downloads data from Konus and saves it as a CSV file.
    """
    url = "https://gcn.gsfc.nasa.gov/konus_grbs.html"

    download_data(url, 'w')

    for year in range(2019, 1993, -1):
        url = f"https://gcn.gsfc.nasa.gov/konus_{year}grbs.html"
        # print(year)
        download_data(url, 'a')

def convert_to_float(coord_str):
    """
    Convert a BAT RA or BAT DEC string to a float representing degrees.
    
    Parameters:
    coord_str (str): The coordinate string (e.g., "-60.637-60:38:13.2" or "40.23402:40:56.2")
    
    Returns:
    float: The coordinate in decimal degrees.
    """
    if '-' in coord_str and coord_str[0] != '-':
        parts = coord_str.split('-')
        sign = -1
        decimal_degrees = float(parts[0])
        dms = parts[1]
    else:
        sign = 1
        if coord_str[0] == '-':
            parts = coord_str.split('-', 2)
            sign = -1
            decimal_degrees = float(parts[1])
            dms = parts[2]
        else:
            parts = coord_str.split(':', 1)
            decimal_degrees = float(parts[0][:-2])
            dms = coord_str[len(parts[0][:-2]):]

    dms_parts = dms.split(':')
    if len(dms_parts) != 3:
        raise ValueError("Input string is not in the correct format")
    
    degrees = float(dms_parts[0])
    minutes = float(dms_parts[1])
    seconds = float(dms_parts[2])
    
    # Convert to decimal degrees
    additional_degrees = degrees + minutes / 60 + seconds / 3600
    
    return sign * (decimal_degrees + additional_degrees / 100)

def swift_to_epoch(grb_date, time_ut):
    # Remove any trailing letters from the GRB date
    grb_date = ''.join(filter(str.isdigit, grb_date))
    # Convert GRB date to standard date format
    date_str = f"20{grb_date[0:2]}-{grb_date[2:4]}-{grb_date[4:6]}"
    
    # Normalize time format to HH:MM:SS
    if '.' in time_ut:  # Check for fractional seconds
        time_ut = time_ut.split('.')[0]  # Remove fractional seconds
    
    if time_ut.strip() == '' or time_ut.strip() == 'null':  # Check for empty time
        time_ut = '00:00:00'

    # Split time into hours, minutes, and seconds
    time_parts = time_ut.split(':')
    # Pad hours, minutes, and seconds with zeros if they are missing
    time_parts = [part.zfill(2) for part in time_parts]
    # Ensure time_parts has exactly 3 elements (hours, minutes, seconds)
    while len(time_parts) < 3:
        time_parts.append('00')  # Add missing seconds or minutes as '00'

    # Combine hours, minutes, and seconds
    time_ut = ':'.join(time_parts)
    
    # Combine date and time
    datetime_str = f"{date_str} {time_ut}"
    
    # Convert to epoch
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    epoch_time = datetime_obj.timestamp()
    
    return epoch_time

def download_swift_data():
    """
    Downloads data from Swift and saves it as a CSV file.
    """
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
        headers.append("Normalised Duration")

        # Remove all other instances of the same header (<thead> tag) and leave only the first one
        for index, thead in enumerate(table.find_all("thead")):
            if index != 0:
                thead.decompose()

        # Replace the first header with "Trigger Time"
        headers[0] = "GRB Name"
        headers[1] = "Trigger Time"
        headers[3] = "BAT Ra"
        headers[4] = "BAT Dec"
        headers[6] = "BAT T90"

        headers = [headers[0], headers[1], headers[3], headers[4], headers[6], headers[7], headers[21]]

        headers.append("Ra")
        headers.append("Dec")

        headers.append("Normalised Duration")

        # Remove all text inside parentheses
        headers = [header.split("(")[0].strip() for header in headers]

        # Write the CSV data to a file
        with open("swift.csv", "w", encoding="utf-8", newline='') as file:
            # write header without csv library
            file.write(";".join(headers) + "\n")
            for row in rows[1:]:  # Skip header row
                cols = [ele.text.strip().replace(";", ",") for ele in row.find_all(["td", "th"])]
                cols = [col if col != "n/a" else "" for col in cols]

                if cols:  # If the row was not empty
                    # Convert the date to epoch time

                    cols = [cols[0], cols[1], cols[3], cols[4], cols[6], cols[7], cols[8], cols[21]]

                    if cols[5] != "" and cols[6] != "":
                        cols[5] = f"{cols[5]}+/-{cols[6]}"

                    cols.pop(6)

                    try:
                        cols.append(str("{:.3f}".format(convert_to_float(cols[2]))))
                        cols.append(str("{:.3f}".format(convert_to_float(cols[3]))))

                        cols[2] = cols[2].rstrip('0').rstrip('.')
                        cols[3] = cols[3].rstrip('0').rstrip('.')
                    except:
                        cols.append("")
                        cols.append("")

                    cols.append(cols[4])
                    cols[1] = str(swift_to_epoch(cols[0], cols[1]))
                    file.write(";".join(cols) + "\n")
    else:
        print("Failed to download data")
        return


# Create a lock object
lock = threading.Lock()
semaphore = threading.Semaphore(5)
SEPARATOR = ','


def thread_wrapper(url, filename, headers, first_write):
    """
    Wrapper function to execute extract_table with semaphore control.
    """
    semaphore.acquire()
    try:
        extract_table(url, filename, headers, first_write)
    finally:
        semaphore.release()


def extract_table(url, filename, headers=False, first_write=False):
    """
    Extracts data from HTML table and writes to CSV file.
    """
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
                    # Process headers row
                    cols = row.find_all('th')
                    cols = [ele.text.strip() for ele in cols]
                    cols[0] = "Trigger Time"

                    # Remove unnecessary columns by index
                    cols.pop(8)
                    cols.pop(7)
                    cols.pop(3)
                    cols.pop(1)
                    cols[3] = "Normalised Duration"

                    f.write(SEPARATOR.join(cols) + '\n')
                    continue
                if row.find('td'):
                    # Process data rows
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]

                    # Remove unnecessary columns by index
                    cols.pop(8)
                    cols.pop(7)
                    cols.pop(3)
                    cols.pop(1)

                    # Convert "," to "." in the data
                    cols = [col.replace(',', '.') for col in cols]

                    # Extract and convert datetime to epoch timestamp
                    try:
                        dt_string = cols[0].split()[0] + ' ' + cols[0].split()[1]
                        dt = datetime.datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
                        epoch_time = int(time.mktime(dt.timetuple()))
                        cols[0] = str(epoch_time)
                    except ValueError:
                        pass

                    f.write(SEPARATOR.join(cols) + '\n')


def download_integral_data():
    """
    Downloads data from Integral and saves it as a CSV file.
    """
    URL = "https://www.isdc.unige.ch/integral/ibas/cgi-bin/ibas_acs_web.cgi"
    filename = 'integral.csv'

    threads = []

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
    data.sort(key=lambda x: int(x.split(SEPARATOR)[0]))

    # Write the ordered data to a new file
    with open(filename, 'w') as f:
        f.write(headers)
        f.write(''.join(data))

def utc_to_epoch(utc_time):
    return utc_time.timestamp()

def mjd_to_utc(mjd):
    # Convert MJD to JD
    jd = mjd + 2400000.5

    # Convert JD to a datetime object
    jd_epoch = datetime(1858, 11, 17, 0, 0, 0)
    days_since_jd_epoch = jd - 2400000.5
    utc_time = jd_epoch + timedelta(days=days_since_jd_epoch)
    
    return utc_time

def mjd_to_epoch(mjd):
    # Convert to UTC and then to EPOCH
    return utc_to_epoch(mjd_to_utc(mjd))

def download_fermi_data(type = 'all'):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning, message=".*Passing bytes to 'read_excel'.*")
        
        # Download data
        download(type)


def download(type = 'all'):
    """
    Downloads data from Fermi and saves it as a CSV file.
    """
    url = "https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3query.pl"

    # Set the request headers (you can copy these from the browser's developer tools)
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en,en-US;q=0.9,it-IT;q=0.8,it",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }

    # Set the request data to select all columns of the table (you can copy these from the browser's developer tools)
    data = [
        ("popupFrom", "Query Results"),
        ("tablehead", "name=heasarc_fermigtrig&description=Fermi+GBM+Trigger+Catalog&url=https://heasarc.gsfc.nasa.gov/W3Browse/fermi/fermigtrig.html&archive=Y&radius=180&mission=FERMI&priority=2&tabletype=Object"),
        ("dummy", "Examples of query constraints:"),
        ("varon", "version"),
        ("varon", "trigger_name"),
        ("bparam_trigger_name", ""),
        ("bparam_trigger_name::format", "char11"),
        ("varon", "name"),
        ("bparam_name", ""),
        ("bparam_name::format", "char20"),
        ("varon", "ra"),
        ("bparam_ra", ""),
        ("bparam_ra::unit", "degree"),
        ("bparam_ra::format", "float8:.4f"),
        ("varon", "dec"),
        ("bparam_dec", ""),
        ("bparam_dec::unit", "degree"),
        ("bparam_dec::format", "float8:.4f"),
        ("varon", "lii"),
        ("bparam_lii", ""),
        ("bparam_lii::unit", "degree"),
        ("bparam_lii::format", "float8:.4f"),
        ("varon", "bii"),
        ("bparam_bii", ""),
        ("bparam_bii::unit", "degree"),
        ("bparam_bii::format", "float8:.4f"),
        ("varon", "error_radius"),
        ("bparam_error_radius", ""),
        ("bparam_error_radius::unit", "degree"),
        ("bparam_error_radius::format", "float8:.4f"),
        ("varon", "time"),
        ("bparam_time", ""),
        ("bparam_time::unit", "mjd"),
        ("bparam_time::format", "float8:.7f"),
        ("varon", "end_time"),
        ("bparam_end_time", ""),
        ("bparam_end_time::unit", "mjd"),
        ("bparam_end_time::format", "float8:.7f"),
        ("varon", "trigger_time"),
        ("bparam_trigger_time", ""),
        ("bparam_trigger_time::unit", "mjd"),
        ("bparam_trigger_time::format", "float8:.7f"),
        ("varon", "trigger_type"),
        ("bparam_trigger_type", ""),
        ("bparam_trigger_type::format", "char32"),
        ("varon", "reliability"),
        ("bparam_reliability", ""),
        ("bparam_reliability::format", "float8:.4f"),
        ("varon", "trigger_timescale"),
        ("bparam_trigger_timescale", ""),
        ("bparam_trigger_timescale::unit", "ms"),
        ("bparam_trigger_timescale::format", "int2"),
        ("varon", "trigger_algorithm"),
        ("bparam_trigger_algorithm", ""),
        ("bparam_trigger_algorithm::format", "int1"),
        ("varon", "channel_low"),
        ("bparam_channel_low", ""),
        ("bparam_channel_low::format", "int2"),
        ("varon", "channel_high"),
        ("bparam_channel_high", ""),
        ("bparam_channel_high::format", "int2"),
        ("varon", "adc_low"),
        ("bparam_adc_low", ""),
        ("bparam_adc_low::format", "int2"),
        ("varon", "adc_high"),
        ("bparam_adc_high", ""),
        ("bparam_adc_high::format", "int2"),
        ("varon", "detector_mask"),
        ("bparam_detector_mask", ""),
        ("bparam_detector_mask::format", "char14"),
        ("varon", "geo_long"),
        ("bparam_geo_long", ""),
        ("bparam_geo_long::unit", "degree"),
        ("bparam_geo_long::format", "float8:.4f"),
        ("varon", "geo_lat"),
        ("bparam_geo_lat", ""),
        ("bparam_geo_lat::unit", "degree"),
        ("bparam_geo_lat::format", "float8:.4f"),
        ("varon", "ra_scx"),
        ("bparam_ra_scx", ""),
        ("bparam_ra_scx::unit", "degree"),
        ("bparam_ra_scx::format", "float8:.4f"),
        ("varon", "dec_scx"),
        ("bparam_dec_scx", ""),
        ("bparam_dec_scx::unit", "degree"),
        ("bparam_dec_scx::format", "float8:.4f"),
        ("varon", "ra_scz"),
        ("bparam_ra_scz", ""),
        ("bparam_ra_scz::unit", "degree"),
        ("bparam_ra_scz::format", "float8:.4f"),
        ("varon", "dec_scz"),
        ("bparam_dec_scz", ""),
        ("bparam_dec_scz::unit", "degree"),
        ("bparam_dec_scz::format", "float8:.4f"),
        ("varon", "theta"),
        ("bparam_theta", ""),
        ("bparam_theta::unit", "degree"),
        ("bparam_theta::format", "float8:.4f"),
        ("varon", "phi"),
        ("bparam_phi", ""),
        ("bparam_phi::unit", "degree"),
        ("bparam_phi::format", "float8:.4f"),
        ("varon", "localization_source"),
        ("bparam_localization_source", ""),
        ("bparam_localization_source::format", "char24"),
        ("Entry", ""),
        ("Coordinates", "J2000"),
        ("Radius", "Default"),
        ("Radius_unit", "arcsec"),
        ("NR", "CheckCaches/GRB/SIMBAD+Sesame/NED"),
        ("Time", ""),
        ("ResultMax", "0"),
        ("displaymode", "ExcelDisplay"),
        ("Fields", "All"),
        ("Action", "Start Search"),
        ("table", "heasarc_fermigtrig")
    ]

    # Send the POST request
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Read the response content as a pandas DataFrame
        df = pd.read_excel(response.content, sheet_name=1)

        columns_to_delete = ['version', 'trigger_name', 'lii', 'bii',
                             'error_radius', 'trigger_timescale',
                             'trigger_algorithm', 'channel_low',
                             'channel_high', 'adc_low', 'adc_high',
                             'detector_mask', 'ra_scx', 'dec_scx', 'ra_scz',
                             'dec_scz', 'theta', 'phi', 'localization_source']

        df = df.drop(columns=columns_to_delete)

        # Convert the time columns from MJD to epoch
        df["time"] = df["time"].apply(mjd_to_epoch)
        df["end_time"] = df["end_time"].apply(mjd_to_epoch)
        df["trigger_time"] = df["trigger_time"].apply(mjd_to_epoch)

        df = df.rename(columns={"trigger_time": "Trigger Time"})
        df = df.rename(columns={"time": "Start Time Observation"})
        df = df.rename(columns={"end_time": "End Time Observation"})
        df = df.rename(columns={"ra": "Ra"})
        df = df.rename(columns={"dec": "Dec"})
        df = df.rename(columns={"geo_long": "GeoLon"})
        df = df.rename(columns={"geo_lat": "GeoLat"})

        df["Normalised Duration"] = df["End Time Observation"] - df["Start Time Observation"]

        # Divide the data into GRB and TGF
        df_grb = df[df["trigger_type"].str.contains("GRB")]
        df_tgf = df[df["trigger_type"].str.contains("TGF")]

        df_grb = df_grb.rename(columns={"name": "GRB Name"})
        df_tgf = df_tgf.rename(columns={"name": "TGF Name"})

        df_grb = df_grb.drop(columns=['trigger_type'])
        df_tgf = df_tgf.drop(columns=['trigger_type'])

        # Save the divided data as CSV files

        if type == "grb":
            df_grb.to_csv("fermi_grb.csv", index=False)
        elif type == "tgf":
            df_tgf.to_csv("fermi_tgf.csv", index=False)
        else:
            df_grb.to_csv("fermi_grb.csv", index=False)
            df_tgf.to_csv("fermi_tgf.csv", index=False)



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


OLD = ["astrosat.csv", "integral.csv", "fermi_grb.csv", "swift.csv", "konus.csv",]

FINAL = "grb.csv"

NAMES = {
        # Earthquake
        'Trigger Time': 'trigger_time',
        'horizontalError': 'horizontal_err',
        'depthError': 'depth_err',
        'magError': 'magnitude_err',
        # GRB
        'GRB Name': 'name',
        'Trigger Time': 'trigger_time',
        'RA (deg)': 'RA',
        'ra': 'RA',
        'dec': 'DEC',
        'DEC (deg)': 'DEC',
        'T90 (s)': 'T90',
        'T90 (sec)': 'T90',
        'Start Time Observation': 'start_time_obs',
        'End Time Observation': 'end_time_obs',
        'BAT RA': 'BAT_RA',
        'BAT Dec': 'BAT_DEC',
        'BAT 90%Error Radius[arcmin]': 'BAT_90_err',
        'BAT Fluence': 'BAT_fluence',
        'BAT Fluence90% Error': 'BAT_fluence_90_err',
        'BAT 1-sec PeakPhoton Flux': 'BAT_1sec_peak_photon_flux',
        'BAT 1-sec PeakPhoton Flux90% Error': 'BAT_1sec_peak_photon_flux_90_err',
        'BAT Photon Index': 'BAT_photon_index',
        'BAT Photon Index90% Error': 'BAT_photon_index_90_err',
        'XRT RA': 'xrtRA',
        'XRT Dec': 'xrtDEC',
        'XRT 90%Error Radius[arcsec]': 'xrt_90_err',
        'XRT Time to FirstObservation[sec]': 'xrt_time_to_first_obs',
        'XRT Early Flux': 'xrt_early_flux',
        'XRT 11 Hour Flux': 'xrt_11hour_flux',
        'XRT 24 Hour Flux': 'xrt_24hour_flux',
        'XRT InitialTemporalIndex': 'xrt_initial_temp_index',
        'XRTSpectral Index': 'xrt_spectral_index',
        'XRT Column Density': 'xrt_column_density',
        'UVOT RA': 'uvotRA',
        'UVOT Dec': 'uvotDEC',
        'UVOT 90%Error Radius[arcsec]': 'uvot_90_err',
        'UVOT Time toFirst Observation[sec]': 'uvot_time_to_first_obs',
        'UVOT Magnitude': 'uvot_magnitude',
        'UVOT Other FilterMagnitudes': 'uvot_other_filter_magnitudes',
        'Other Observatory Detections': 'other_obs_detects',
        'Redshift': 'redshift',
        'Host Galaxy': 'host_galaxy',
        'References': 'references',
        'Type': 'type',
        'Sigma': 'sigma',
        'Duration [s]': 'duration',
        'Max Count': 'max_count',
}


def get_grb():
    download()
    step1()
    step2()
    step3()
    step4()


def download():
    threads = []
    threads.append(threading.Thread(target=lambda: [download_fermi_data("grb")]))
    threads.append(threading.Thread(target=lambda: [download_astrosat_data()]))
    threads.append(threading.Thread(target=lambda: [download_integral_data()]))
    threads.append(threading.Thread(target=lambda: [download_swift_data()]))
    threads.append(threading.Thread(target=lambda: [download_konus_data()]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def step1():
    for dataset in OLD:
        if dataset == "swift.csv":
            df = pd.read_csv(dataset, sep=';')
        else:
            df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        if dataset == "swift.csv":
            df.to_csv(dataset, index=False, quoting=0, quotechar='"', escapechar='\\', doublequote=False, sep=';')
        else:
            df.to_csv(dataset, index=False, quoting=0, quotechar='"', escapechar='\\', doublequote=False, sep=',')


def step2():
    grb = pd.concat([pd.read_csv(dataset) for dataset in OLD if dataset != "integral.csv" and dataset != "swift.csv"])
    integral = pd.read_csv("integral.csv", sep=',')
    swift = pd.read_csv("swift.csv", sep=';')
    grb = pd.concat([grb, integral, swift])
    grb.to_csv("grb.csv", index=False)


def step3():
    df = pd.read_csv(FINAL, low_memory=False)
    t = df.columns
    df.rename(columns=NAMES, inplace=True, errors='ignore')
    f = df.columns
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df.to_csv(FINAL, index=False)


def increment_char(char_str):
    if char_str == '':
        return 'A'
    last_char = char_str[-1]
    if last_char != 'Z':
        return char_str[:-1] + chr(ord(last_char) + 1)
    return increment_char(char_str[:-1]) + 'A'


def step4():
    with open(FINAL, 'r') as file:
        lines = file.readlines()

    new_lines = []
    new_lines.append(lines[0])

    columns = [1, 7, 8]

    name_table_dict = {}  # Dictionary to keep track of the last used char for each unique name

    lines = sorted(lines[1:], key=lambda x: int(float(x.split(",")[1])))

    for line in lines:
        data = line.strip().split(",")
        for c in columns:
            if data[c] != "":
                epoch_int = int(float(str(data[c])))
                utc_dt = strftime('%Y-%m-%d %H:%M:%S', localtime(epoch_int))
                data[c] = utc_dt

        data[0] = f"GRB{data[1][2:4]}{data[1][5:7]}{data[1][8:10]}"
        name_key = (data[0], data[6])  # Create a tuple to use as a key in the dictionary

        if name_key in name_table_dict:
            # Increment the character if the name is already in the dictionary
            name_char = increment_char(name_table_dict[name_key])
        else:
            # Start with 'A' if the name is not yet in the dictionary
            name_char = 'A'

        # Update the dictionary with the new character
        name_table_dict[name_key] = name_char

        # Update the data with the new name and character
        data[0] = f"{data[0]}{name_char}"
        new_line = ",".join(data)
        new_line = new_line.replace("--", "")
        new_lines.append(new_line + "\n")

    with open(FINAL, 'w') as file:
        file.writelines(new_lines)


if __name__ == "__main__":
    get_grb()
