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
    "fermi.csv",
]

# Gamma-ray Bursts (GRB)
GRB = [
    "astrosat.csv",
    "integral.csv",
    "fermi.csv",
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
    print("Harmonizing data...")
    print("[bold red]Not implemented yet[/bold red]")
    print("Data harmonized successfully")
    print("Converting data to SQL...")
    print("[bold red]Not implemented yet[/bold red]")
    print("Data converted successfully")