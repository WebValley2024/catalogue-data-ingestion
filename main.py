from astrosat import download_astrosat_data
from fermi import download_fermi_data
from earthquake import download_earthquake_data
from integral import download_integral_data
from agile import download_agile_data
from swift import download_swift_data
from spaceweatherevents import download_space_weather_data
import threading

from rich.console import Console
from rich import print

console = Console()

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

    threads = []
    threads.append(threading.Thread(target=thread_download_astrosat_data))
    threads.append(threading.Thread(target=thread_download_fermi_data))
    threads.append(threading.Thread(target=thread_download_earthquake_data))
    threads.append(threading.Thread(target=thread_download_integral_data))
    threads.append(threading.Thread(target=thread_download_agile_data))
    threads.append(threading.Thread(target=thread_download_swift_data))
    threads.append(threading.Thread(target=thread_download_space_weather_data))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("All data downloaded successfully")