from spaceweatherevents import download_space_weather_data
import pandas as pd
from time import strftime, localtime

OLD = ["spaceweatherevents.csv"]

FINAL = "swe.csv"

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


def get_swe():
    download()
    step1()
    step2()
    step3()
    step4()


def download():
    download_space_weather_data()


def step1():
    for dataset in OLD:
        df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        df.to_csv(dataset, index=False, quoting=0, quotechar='"', escapechar='\\', doublequote=False, sep=',')


def step2():
    swe = pd.concat([pd.read_csv(dataset) for dataset in OLD])
    swe.to_csv("swe.csv", index=False)


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

        columns = [3, 4, 5]

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


if __name__ == "__main__":
    get_swe()
