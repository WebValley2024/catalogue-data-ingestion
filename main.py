from astrosat import download_astrosat_data
from fermi import download_fermi_data
from earthquake import download_earthquake_data
from integral import download_integral_data
from agile import download_agile_data
from swift import download_swift_data

if __name__ == "__main__":
    print("Downloading data...")
    print("Downloading Astrosat data...")
    download_astrosat_data()
    print("Downloading Fermi data...")
    download_fermi_data()
    print("Downloading earthquake data...")
    download_earthquake_data()
    print("Downloading Integral data...")
    download_integral_data()
    print("Downloading Agile data...")
    download_agile_data()
    print("Downloading Swift data...")
    download_swift_data()
    print("Data downloaded successfully")