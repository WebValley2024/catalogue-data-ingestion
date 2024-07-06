import pandas as pd
from time import strftime, localtime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import strftime, localtime
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

def is_leap_year(year):
    # Check if a year is a leap year
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def day_of_year_to_date(year, day):
    # Determine the corresponding month and day for a given day of the year
    # Use a list of the number of days in each month
    days_in_month = [31, 29 if is_leap_year(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month = 1
    while day > days_in_month[month - 1]:
        day -= days_in_month[month - 1]
        month += 1
    return month, day


def to_epoch_timestamp(year, day, hour, minute):
    # Convert the given parameters to an epoch timestamp
    month, day = day_of_year_to_date(year, day)
    dt = datetime(year, month, day, hour, minute)
    # Convert the datetime to an epoch timestamp
    epoch_timestamp = int(dt.timestamp())
    return str(epoch_timestamp)


def get_data_from_table(second_page_content, empty=False):
    soup = BeautifulSoup(second_page_content, 'html.parser')
    lst_link = soup.find('a').get('href')

    try:
        response = requests.get(lst_link)
    except Exception as e:
        print("Could not get the data (check the data range)")
        return

    if response.status_code == 200:
        file_content = response.text

        new_rows = []

        header = ["Trigger Time", "Field Magnitude Average(nT)", "Speed(km/s)"]

        if empty:
            new_rows.append(f"{','.join(header)}\n")

        rows = file_content.split('\n')

        for i in range(len(rows)-1):
            parts = list(filter(None, rows[i].split(' ')))
            parts[0] = to_epoch_timestamp(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
            parts.pop(1)
            parts.pop(1)
            parts.pop(1)

            if parts[1] == "9999.99":
                parts[1] = ""
            if parts[2] == "99999.9":
                parts[2] = ""

            if parts[0] != "":
                epoch_int = int(float(parts[0]))
                utc_dt = strftime('%Y-%m-%d %H:%M:%S', localtime(epoch_int))
                parts[0] = utc_dt

            if (parts[1] != "" or parts[2] != "") and (parts[0][11:16] == "00:00" or parts[0][11:16] == "06:00" or parts[0][11:16] == "12:00" or parts[0][11:16] == "18:00"):
                new_rows.append(','.join(parts))

        return new_rows

    else:
        print(f"Failed to retrieve the file: {response.status_code}")
        return


def one_year_behind(date_str):
    # Parse the input date string to a datetime object
    date_format = "%Y%m%d"
    original_date = datetime.strptime(date_str, date_format)

    # Subtract one year
    one_year_behind_date = original_date.replace(year=original_date.year - 1)

    # Convert the datetime object back to a string
    return one_year_behind_date.strftime(date_format)


def download_dst_data():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-javascript")
    options.add_argument("--enable-user-scripts")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-gpu")
    # Initialize the WebDriver (here using Chrome)
    driver = webdriver.Chrome(options=options)

    lines_to_write = []

    try:
        # Open the webpage
        driver.get('https://omniweb.gsfc.nasa.gov/form/omni_min.html')  # Replace with the actual URL

        # Wait until the form is loaded and input fields are present
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, 'start_date')))
        wait.until(EC.presence_of_element_located((By.NAME, 'end_date')))

        for i in range(24):

            # Using zfill to pad the year part
            year = str(i+1).zfill(2)
            end_date = f"20{year}0606"

            start_date = one_year_behind(end_date)

            print(f"<dst> Downloading year {start_date[:4]}")

            # Locate the start date input field and set its value
            start_date_input = driver.find_element(By.NAME, 'start_date')
            start_date_input.clear()
            start_date_input.send_keys(start_date)  # Set the desired start date

            # Locate the end date input field and set its value
            end_date_input = driver.find_element(By.NAME, 'end_date')
            end_date_input.clear()
            end_date_input.send_keys(end_date)  # Set the desired end date

            # Select the second radio button ('List data')
            list_radio_button = driver.find_element(By.CSS_SELECTOR, 'input[type="radio"][value="ftp"]')
            list_radio_button.click()

            # Click the submit button
            submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Submit"]')
            submit_button.click()

            # Wait for the second page to load and get its content
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            second_page_content = driver.page_source

            if i != 0:
                lines = get_data_from_table(second_page_content)
            else:
                lines = get_data_from_table(second_page_content, True)

            lines_to_write.extend(lines)

            driver.back()

            wait.until(EC.presence_of_element_located((By.NAME, 'start_date')))
            wait.until(EC.presence_of_element_located((By.NAME, 'end_date')))

        with open("dst.csv", "w") as dst:
            for line in lines_to_write:
                dst.write(f"{line}\n")

    finally:
        # Close the WebDriver
        driver.quit()

OLD = ["dst.csv"]

FINAL = "gms.csv"

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


def get_gms():
    download()
    step1()
    step2()
    step3()
    # step4()


def download():
    download_dst_data()


def step1():
    for dataset in OLD:
        df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        df.to_csv(dataset, index=False, quoting=0, quotechar='"', escapechar='\\', doublequote=False, sep=',')


def step2():
    eq = pd.concat([pd.read_csv(dataset) for dataset in OLD])
    eq.to_csv(FINAL, index=False)


def step3():
    df = pd.read_csv(FINAL, low_memory=False)
    t = df.columns
    df.rename(columns=NAMES, inplace=True, errors='ignore')
    f = df.columns
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df.to_csv(FINAL, index=False)


def step4():
    with open(FINAL, 'r') as file:
        lines = file.readlines()

        new_lines = []
        new_lines.append(lines[0])

        columns = [0]

        for line in lines[1:]:
            data = line.strip().split(",")
            for c in columns:
                if data[c] != "":
                    epoch_int = int(float(data[c]))
                    utc_dt = strftime('%Y-%m-%d %H:%M:%S', localtime(epoch_int))
                    data[c] = utc_dt

            if data[0][14:16] == "00" or data[0][14:16] == "30":
                new_line = ",".join(data)
                new_line = new_line.replace("--", "")
                new_lines.append(new_line + "\n")

    with open(FINAL, 'w') as file:
        file.writelines(new_lines)


if __name__ == "__main__":
    get_gms()
