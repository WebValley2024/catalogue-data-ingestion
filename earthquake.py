import requests
import sys
from datetime import datetime, timedelta
from time_related import iso_to_epoch


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


if __name__ == "__main__":
    download_earthquake_data()
