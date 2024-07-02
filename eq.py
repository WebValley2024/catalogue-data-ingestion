from earthquake import download_earthquake_data
import pandas as pd
from time import strftime, localtime

OLD = ["earthquake.csv"]

FINAL = "eq.csv"

NAMES = {
    'Trigger Time': 'trigger_time',
    'horizontalError': 'horizontal_err',
    'depthError': 'depth_err',
    'magError': 'magnitude_err',
}


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

        for line in lines[1:]:
            data = line.strip().split(",")
            if data[0] != "":
                epoch_int = int(float(data[0]))
                utc_dt = strftime('%Y-%m-%d %H:%M:%S', localtime(epoch_int))
                data[0] = utc_dt
            new_line = ",".join(data)
            new_line = new_line.replace("--", "")
            new_lines.append(new_line + "\n")

    with open(FINAL, 'w') as file:
        file.writelines(new_lines)


if __name__ == "__main__":
    download_earthquake_data()

    step1()
    step2()
    step3()
    step4()
