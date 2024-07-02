from astrosat import download_astrosat_data
from fermi import download_fermi_data
from integral import download_integral_data
from swift import download_swift_data
from konus import download_konus_data
import pandas as pd
from time import strftime, localtime

import threading
from sqlalchemy import create_engine
import pandas as pd
import os

from rich.console import Console
from rich.progress import Progress
from rich import print
from time import strftime, localtime

console = Console()

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


def step4():
    with open(FINAL, 'r') as file:
        lines = file.readlines()

        new_lines = []
        new_lines.append(lines[0])

        columns = [1, 7, 8]

        for line in lines[1:]:
            data = line.strip().split(",")
            for c in columns:
                if data[c] != "":
                    epoch_int = int(float(str(data[c])))
                    utc_dt = strftime('%Y-%m-%d %H:%M:%S', localtime(epoch_int))
                    data[c] = utc_dt
            new_line = ",".join(data)
            new_line = new_line.replace("--", "")
            new_lines.append(new_line + "\n")

    with open(FINAL, 'w') as file:
        file.writelines(new_lines)


if __name__ == "__main__":
    with Progress() as progress:
        download_task = progress.add_task("[green]Downloading data...", total=5)

        threads = []
        threads.append(threading.Thread(target=lambda: [download_fermi_data("grb"), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [download_astrosat_data(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [download_integral_data(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [download_swift_data(), progress.advance(download_task)]))
        threads.append(threading.Thread(target=lambda: [download_konus_data(), progress.advance(download_task)]))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        if not progress.finished:
            progress.stop()

    step1()
    step2()
    step3()
    step4()
