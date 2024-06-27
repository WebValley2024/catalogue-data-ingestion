# Script to download and convert from XLS to CSV the data from the following URL with specific parameters
# https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3query.pl

import requests
import pandas as pd
from time_related import mjd_to_epoch

def download_fermi_data():
    # Download the data
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

        # Convert the time columns from MJD to epoch
        df["time"] = df["time"].apply(mjd_to_epoch)
        df["end_time"] = df["end_time"].apply(mjd_to_epoch)
        df["trigger_time"] = df["trigger_time"].apply(mjd_to_epoch)

        df = df.rename(columns={"trigger_time": "Trigger Time"})


        # Save the DataFrame as a CSV file
        df.to_csv("fermi.csv", index=False)

if __name__ == "__main__":
    download_fermi_data()