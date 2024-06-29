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
        df.to_csv(dataset, index=False)
    
    for dataset in GRB:
        print("Harmonizing", dataset)
        if dataset == "swift.csv":
            df = pd.read_csv(dataset, sep=';')
        else:
            df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        df.to_csv(dataset, index=False)

    for dataset in SWE:
        print("Harmonizing", dataset)
        df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        df.to_csv(dataset, index=False)

    for dataset in EQ:
        print("Harmonizing", dataset)
        df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        df.to_csv(dataset, index=False)

def harmonize_step2():
    # Combine all tables of the same type (e.g. TGF, GRB, SWE, EQ) into a single table
    # This will be useful when converting the data to SQL

    # TGF
    tgf = pd.concat([pd.read_csv(dataset) for dataset in TGF])
    tgf.to_csv("tgf.csv", index=False)

    # GRB
    grb = pd.concat([pd.read_csv(dataset) for dataset in GRB])
    grb.to_csv("grb.csv", index=False)

    # SWE
    swe = pd.concat([pd.read_csv(dataset) for dataset in SWE])
    swe.to_csv("swe.csv", index=False)

    # EQ
    eq = pd.concat([pd.read_csv(dataset) for dataset in EQ])
    eq.to_csv("eq.csv", index=False)

def convert_to_sql():
    # Convert the harmonized data to MySQL
    USER = os.getenv('MYSQL_USER')
    PASSWORD = os.getenv('MYSQL_PASSWORD')
    HOST = os.getenv('MYSQL_HOST')
    DATABASE = os.getenv('MYSQL_DATABASE')
    engine = create_engine('mysql://' + USER + ':' + PASSWORD + '@' + HOST + '/' + DATABASE)
    conn = engine.connect()

    # TGF
    tgf = pd.read_csv("tgf.csv", quotechar='"')
    tgf.columns = tgf.columns.str.strip('"')  # Strip double quotes from column names
    tgf.to_sql("tgf", conn, if_exists='replace', index=False)

    # GRB
    grb = pd.read_csv("grb.csv", quotechar='"', dtype=str)  # Ensure all data is read as string
    grb.columns = grb.columns.str.strip('"')  # Strip double quotes from column names

    # Strip double quotes from data values
    for col in grb.columns:
        grb[col] = grb[col].apply(lambda x: x.strip('"') if isinstance(x, str) else x)

    grb.to_sql("grb", conn, if_exists='replace', index=False)

    # SWE
    swe = pd.read_csv("swe.csv", quotechar='"')
    swe.columns = swe.columns.str.strip('"')  # Strip double quotes from column names
    swe.to_sql("swe", conn, if_exists='replace', index=False)

    # EQ
    eq = pd.read_csv("eq.csv", quotechar='"')
    eq.columns = eq.columns.str.strip('"')  # Strip double quotes from column names
    eq.to_sql("eq", conn, if_exists='replace', index=False)

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

    print("All data downloaded successfully")
    print("Harmonizing data (step 1/2)...")
    harmonize_step1()
    # print("[bold red]Not implemented yet[/bold red]")
    print("Harmonizing data (step 2/2)...")
    harmonize_step2()
    # print("[bold red]Not implemented yet[/bold red]")
    print("Data harmonized successfully")
    print("Converting data to SQL...")
    convert_to_sql()
    # print("[bold red]Not implemented yet[/bold red]")
    print("Data converted successfully")