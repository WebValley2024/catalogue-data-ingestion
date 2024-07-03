from fermi import download_fermi_data
from agile import download_agile_data
import pandas as pd
from time import strftime, localtime
import threading
from time import strftime, localtime

OLD = ["agile.csv", "fermi_tgf.csv"]

FINAL = "tgf.csv"

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


def get_tgf():
    download()
    step1()
    step2()
    step3()
    step4()


def download():
    threads = []
    threads.append(threading.Thread(target=lambda: [download_fermi_data("tgf")]))
    threads.append(threading.Thread(target=lambda: [download_agile_data()]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def step1():
    for dataset in OLD:
        df = pd.read_csv(dataset)
        df['source'] = dataset.split('.')[0]
        df.to_csv(dataset, index=False, quoting=0, quotechar='"', escapechar='\\', doublequote=False, sep=',')


def step2():
    tgf = pd.concat([pd.read_csv(dataset) for dataset in OLD])
    tgf.to_csv("tgf.csv", index=False)


def step3():
    df = pd.read_csv(FINAL, low_memory=False)
    t = df.columns
    df.rename(columns=NAMES, inplace=True, errors='ignore')
    f = df.columns
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df.to_csv(FINAL, index=False)


def increment_char(char_str):
    if char_str == '':
        return 'A'
    last_char = char_str[-1]
    if last_char != 'Z':
        return char_str[:-1] + chr(ord(last_char) + 1)
    return increment_char(char_str[:-1]) + 'A'


def step4():    
    with open(FINAL, 'r') as file:
        lines = file.readlines()

    new_lines = []
    new_lines.append(lines[0])

    columns = [3, 17, 18]

    name_table_dict = {}  # Dictionary to keep track of the last used char for each unique name

    lines = sorted(lines[1:], key=lambda x: int(float(x.split(",")[3])))

    for line in lines:
        data = line.strip().split(",")
        for c in columns:
            if data[c] != "":
                epoch_int = int(float(str(data[c])))
                utc_dt = strftime('%Y-%m-%d %H:%M:%S', localtime(epoch_int))
                data[c] = utc_dt

        data[11] = f"TGF{data[3][2:4]}{data[3][5:7]}{data[3][8:10]}"
        name_key = (data[11], data[14])  # Create a tuple to use as a key in the dictionary

        if name_key in name_table_dict:
            # Increment the character if the name is already in the dictionary
            name_char = increment_char(name_table_dict[name_key])
        else:
            # Start with 'A' if the name is not yet in the dictionary
            name_char = 'A'

        # Update the dictionary with the new character
        name_table_dict[name_key] = name_char

        # Update the data with the new name and character
        data[11] = f"{data[11]}{name_char}"
        new_line = ",".join(data)
        new_line = new_line.replace("--", "")
        new_lines.append(new_line + "\n")

    with open(FINAL, 'w') as file:
        file.writelines(new_lines)


if __name__ == "__main__":
    get_tgf()
