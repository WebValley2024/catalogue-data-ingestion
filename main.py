from astrosat import download_astrosat_data
from fermi import download_fermi_data
from earthquake import download_earthquake_data
from integral import download_integral_data
from agile import download_agile_data
from swift import download_swift_data
from spaceweatherevents import download_space_weather_data
from konus import download_konus_data
import threading
from sqlalchemy import create_engine
import pandas as pd
import os

from rich.console import Console
from rich.progress import Progress
from rich import print

console = Console()

# -----------------------
# DIFFERENT DATA SOURCES
# -----------------------

# Terrestrial Gamma-ray Flashes (TGF)
TGF = [
    "agile.csv",
    "fermi_tgf.csv",
]

# Gamma-ray Bursts (GRB)
GRB = [
    "astrosat.csv",
    "integral.csv",
    "fermi_grb.csv",
    "swift.csv",
    "konus.csv",
]

# Solar Flares --> Space Weather Events
SWE = ["spaceweatherevents.csv"]

# Earthquakes
EQ = ["earthquake.csv"]

# Final data
FINAL = ["eq.csv", "grb.csv", "swe.csv", "tgf.csv"]

def thread_download_astrosat_data():
    download_astrosat_data()
    print("<astrosat> Download completed.")

def thread_download_fermi_data():
    download_fermi_data()
    print("<fermi> Download completed.")

def thread_download_earthquake_data():
    download_earthquake_data()
    print("<earthquake> Download completed.")

def thread_download_integral_data():
    download_integral_data()
    print("<integral> Download completed.")

def thread_download_agile_data():
    download_agile_data()
    print("<agile> Download completed.")

def thread_download_swift_data():
    download_swift_data()
    print("<swift> Download completed.")

def thread_download_space_weather_data():
    download_space_weather_data()
    print("<spaceweatherevents> Download completed.")

def harmonize_step1():
    # Add a column to each dataset to indicate the source (e.g. astrosat, fermi, earthquake, etc.)
    # This will be useful when converting the data to SQL
    for dataset in TGF:
        print("Harmonizing", dataset)
        df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        df.to_csv(dataset, index=False, quoting=0, quotechar='"', escapechar='\\', doublequote=False, sep=',')
    
    for dataset in GRB:
        print("Harmonizing", dataset)
        if dataset == "swift.csv":
            df = pd.read_csv(dataset, sep=';')
        else:
            df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        if dataset == "swift.csv":
            df.to_csv(dataset, index=False, quoting=0, quotechar='"', escapechar='\\', doublequote=False, sep=';')
        else:
            df.to_csv(dataset, index=False, quoting=0, quotechar='"', escapechar='\\', doublequote=False, sep=',')

    for dataset in SWE:
        print("Harmonizing", dataset)
        df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        df.to_csv(dataset, index=False, quoting=0, quotechar='"', escapechar='\\', doublequote=False, sep=',')

    for dataset in EQ:
        print("Harmonizing", dataset)
        df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        df.to_csv(dataset, index=False, quoting=0, quotechar='"', escapechar='\\', doublequote=False, sep=',')

def harmonize_step2():
    # Combine all tables of the same type (e.g. TGF, GRB, SWE, EQ) into a single table
    # This will be useful when converting the data to SQL

    # TGF
    tgf = pd.concat([pd.read_csv(dataset) for dataset in TGF])
    tgf.to_csv("tgf.csv", index=False)

    # GRB
    grb = pd.concat([pd.read_csv(dataset) for dataset in GRB if dataset != "integral.csv" and dataset != "swift.csv"])
    integral = pd.read_csv("integral.csv", sep=',')
    swift = pd.read_csv("swift.csv", sep=';')
    grb = pd.concat([grb, integral, swift])
    grb.to_csv("grb.csv", index=False)

    # SWE
    swe = pd.concat([pd.read_csv(dataset) for dataset in SWE])
    swe.to_csv("swe.csv", index=False)

    # EQ
    eq = pd.concat([pd.read_csv(dataset) for dataset in EQ])
    eq.to_csv("eq.csv", index=False)

def harmonize_step3():
    # Convert all csv columns to lowercase and remove spaces (replace with underscores)
    # Also use a dictionary to rename columns to a common name
    # TODO: FIX NAMES
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

    for dataset in FINAL:
        print("Correcting", dataset)
        df = pd.read_csv(dataset, low_memory=False)
        t = df.columns
        print(df.columns)
        df.rename(columns=NAMES, inplace=True, errors='ignore')
        f = df.columns
        print(df.columns)
        print(t == f)
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        df.to_csv(dataset, index=False)

# def convert_to_sql():
#     # Convert the harmonized data to MySQL
#     USER = os.getenv('MYSQL_USER')
#     PASSWORD = os.getenv('MYSQL_PASSWORD')
#     HOST = os.getenv('MYSQL_HOST')
#     DATABASE = os.getenv('MYSQL_DATABASE')
#     engine = create_engine('mysql://' + USER + ':' + PASSWORD + '@' + HOST + '/' + DATABASE)
#     conn = engine.connect()

#     # TGF
#     tgf = pd.read_csv("tgf.csv", quotechar='"')
#     tgf.columns = tgf.columns.str.strip('"')  # Strip double quotes from column names
#     tgf.to_sql("spadeapp_tgf", conn, if_exists='append', index=False)

#     # GRB
#     grb = pd.read_csv("grb.csv", quotechar='"', dtype=str)  # Ensure all data is read as string
#     grb.columns = grb.columns.str.strip('"')  # Strip double quotes from column names

#     # Strip double quotes from data values
#     for col in grb.columns:
#         grb[col] = grb[col].apply(lambda x: x.strip('"') if isinstance(x, str) else x)

#     grb.to_sql("spadeapp_grb", conn, if_exists='append', index=False)

#     # SWE
#     swe = pd.read_csv("swe.csv", quotechar='"')
#     swe.columns = swe.columns.str.strip('"')  # Strip double quotes from column names
#     swe.to_sql("spadeapp_swe", conn, if_exists='append', index=False)

#     # EQ
#     eq = pd.read_csv("eq.csv", quotechar='"')
#     eq.columns = eq.columns.str.strip('"')  # Strip double quotes from column names
#     eq.to_sql("spadeapp_earthquake", conn, if_exists='append', index=False)

if __name__ == "__main__":
    print("Downloading data...")

    with Progress() as progress:
        download_task = progress.add_task("[green]Downloading data...", total=8)

        threads = []
        threads.append(threading.Thread(target=lambda: [thread_download_astrosat_data(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [thread_download_fermi_data(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [thread_download_earthquake_data(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [thread_download_integral_data(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [thread_download_agile_data(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [thread_download_swift_data(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [thread_download_space_weather_data(), progress.advance(download_task)]))
        
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Apparently, the Konus data is not being downloaded correctly when using threads
        # It will be downloaded separately in the main thread after all other data has been downloaded
        download_konus_data()
        print("<konus> Download completed.")
        progress.advance(download_task)
        if not progress.finished:
            progress.stop()

    print("All data downloaded successfully")
    print("Harmonizing data (step 1/3)...")
    harmonize_step1()
    # print("[bold red]Not implemented yet[/bold red]")
    print("Harmonizing data (step 2/3)...")
    harmonize_step2()
    # print("[bold red]Not implemented yet[/bold red]")
    print("Harmonizing data (step 3/3)...")
    harmonize_step3()
    # print("[bold red]Not implemented yet[/bold red]")
    print("Data harmonized successfully")
    print("Data converted successfully")