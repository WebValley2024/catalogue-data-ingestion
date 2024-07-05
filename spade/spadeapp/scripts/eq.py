import pandas as pd
from time import strftime, localtime
import requests
import sys
from datetime import datetime, timedelta

def iso_to_epoch(timestamp):
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return int(dt.timestamp())


def download_earthquake_data(initial_date=datetime.now() - timedelta(days=4000), end_date=datetime.now()):
    """
    Downloads data from Earthquakes and saves it as a CSV file.
    """
    if initial_date > end_date:
        print("Initial date must be less than end date")
        sys.exit(1)
    if end_date > datetime.now():
        print("End date must be less than the current date")
        sys.exit(1)

    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime={initial_date.date()}%2000:00:00&endtime={end_date.date()}%2023:59:59&minmagnitude=5.0&reviewstatus=reviewed&eventtype=earthquake,accidental%20explosion,acoustic%20noise,acoustic_noise,anthropogenic_event,building%20collapse,chemical%20explosion,chemical_explosion,collapse,debris%20avalanche,eq,experimental%20explosion,explosion,ice%20quake,induced%20or%20triggered%20event,industrial%20explosion,landslide,meteor,meteorite,mine%20collapse,mine_collapse,mining%20explosion,mining_explosion,not%20existing,not%20reported,not_reported,nuclear%20explosion,nuclear_explosion,other,other%20event,other_event,quarry,quarry%20blast,quarry_blast,rock%20burst,Rock%20Slide,rockslide,rock_burst,snow%20avalanche,snow_avalanche,sonic%20boom,sonicboom,sonic_boom,train%20crash,volcanic%20eruption,volcanic%20explosion&orderby=time"

    # Send GET request to retrieve earthquake data
    response = requests.get(url)

    # Check if data was successfully retrieved
    if response.status_code == 200:
        with open("earthquake.csv", "w", encoding='utf-8') as file:
            data = response.text
            data_rows = data.strip().split('\n')

            # Process header separately
            header = data_rows[0]
            headerlist = header.split(",")
            headerlist[0] = "Trigger Time"
            converted_header = ','.join(headerlist)
            file.write(converted_header + '\n')

            # Process data rows
            for row in data_rows[1:]:
                row = row.replace(", ", " ")
                fields = row.split(',')
                fields[0] = str(iso_to_epoch(fields[0]))
                fields[12] = str(iso_to_epoch(fields[12]))
                converted_row = ','.join(fields)
                file.write(converted_row + '\n')
    else:
        print("Failed to download data")
        sys.exit(1)

OLD = ["earthquake.csv"]

FINAL = "eq.csv"

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


def get_eq():
    download()
    step1()
    step2()
    step3()
    step4()


def download():
    download_earthquake_data()


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

        columns = [0, 12]

        for line in lines[1:]:
            data = line.strip().split(",")
            for c in columns:
                if data[c] != "":
                    epoch_int = int(float(data[c]))
                    utc_dt = strftime('%Y-%m-%d %H:%M:%S', localtime(epoch_int))
                    data[c] = utc_dt
            new_line = ",".join(data)
            new_line = new_line.replace("--", "")
            new_lines.append(new_line + "\n")

        
    with open(FINAL, 'w') as file:
        file.writelines(new_lines)
        file.write("\n\n\n\n")

if __name__ == "__main__":
    get_eq()
