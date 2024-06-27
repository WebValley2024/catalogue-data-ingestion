# Script to download earthquake data from USGS
# URL: https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime=2024-05-26%2000:00:00&endtime=2024-06-25%2023:59:59&minmagnitude=2.5&reviewstatus=reviewed&eventtype=earthquake,accidental%20explosion,acoustic%20noise,acoustic_noise,anthropogenic_event,building%20collapse,chemical%20explosion,chemical_explosion,collapse,debris%20avalanche,eq,experimental%20explosion,explosion,ice%20quake,induced%20or%20triggered%20event,industrial%20explosion,landslide,meteor,meteorite,mine%20collapse,mine_collapse,mining%20explosion,mining_explosion,not%20existing,not%20reported,not_reported,nuclear%20explosion,nuclear_explosion,other,other%20event,other_event,quarry,quarry%20blast,quarry_blast,rock%20burst,Rock%20Slide,rockslide,rock_burst,snow%20avalanche,snow_avalanche,sonic%20boom,sonicboom,sonic_boom,train%20crash,volcanic%20eruption,volcanic%20explosion&orderby=time

import requests
import sys
import datetime
from datetime import datetime, timedelta

# TODO: REPLACE TIME UTC WITH EPOCH

def convert_to_epoch(timestamp):
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return int(dt.timestamp())

def download_earthquake_data(end_date=datetime.now() - timedelta(days=30), initial_date=datetime.now()):
    if initial_date > end_date:
        print("Initial date must be less than end date")
        sys.exit(1)
    if end_date > datetime.now():
        print("End date must be less than the current date")
        sys.exit(1)

    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime={initial_date.date()}%2000:00:00&endtime={end_date.date()}%2023:59:59&minmagnitude=2.5&reviewstatus=reviewed&eventtype=earthquake,accidental%20explosion,acoustic%20noise,acoustic_noise,anthropogenic_event,building%20collapse,chemical%20explosion,chemical_explosion,collapse,debris%20avalanche,eq,experimental%20explosion,explosion,ice%20quake,induced%20or%20triggered%20event,industrial%20explosion,landslide,meteor,meteorite,mine%20collapse,mine_collapse,mining%20explosion,mining_explosion,not%20existing,not%20reported,not_reported,nuclear%20explosion,nuclear_explosion,other,other%20event,other_event,quarry,quarry%20blast,quarry_blast,rock%20burst,Rock%20Slide,rockslide,rock_burst,snow%20avalanche,snow_avalanche,sonic%20boom,sonicboom,sonic_boom,train%20crash,volcanic%20eruption,volcanic%20explosion&orderby=time"
    
    response = requests.get(url)

    if response.status_code == 200:
        with open("earthquake.csv", "w") as file:
            data = response.content.decode('utf-8')
            data_rows = data.strip().split('\n')

            # Process header separately
            header = data_rows[0]
            file.write(header + '\n')

            # Process data rows
            for row in data_rows[1:]:
                fields = row.split(',')
                fields[0] = str(convert_to_epoch(fields[0]))
                converted_row = ','.join(fields)
                file.write(converted_row + '\n')

    else:
        print("Failed to download data")
        sys.exit(1)


if __name__ == "__main__":
    download_earthquake_data(datetime.now(), datetime.now() - timedelta(days=30))