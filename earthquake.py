# Script to download earthquake data from USGS
# URL: https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime=2024-05-26%2000:00:00&endtime=2024-06-25%2023:59:59&minmagnitude=2.5&reviewstatus=reviewed&eventtype=earthquake,accidental%20explosion,acoustic%20noise,acoustic_noise,anthropogenic_event,building%20collapse,chemical%20explosion,chemical_explosion,collapse,debris%20avalanche,eq,experimental%20explosion,explosion,ice%20quake,induced%20or%20triggered%20event,industrial%20explosion,landslide,meteor,meteorite,mine%20collapse,mine_collapse,mining%20explosion,mining_explosion,not%20existing,not%20reported,not_reported,nuclear%20explosion,nuclear_explosion,other,other%20event,other_event,quarry,quarry%20blast,quarry_blast,rock%20burst,Rock%20Slide,rockslide,rock_burst,snow%20avalanche,snow_avalanche,sonic%20boom,sonicboom,sonic_boom,train%20crash,volcanic%20eruption,volcanic%20explosion&orderby=time

import requests
import sys
import datetime

# TODO: REPLACE TIME UTC WITH EPOCH

def download_earthquake_data(initial_date = datetime.datetime.now() - datetime.timedelta(days=30), end_date = datetime.datetime.now()):
    if initial_date > end_date:
        print("Initial date must be less than end date")
        sys.exit(1)
    if end_date > datetime.datetime.now():
        print("End date must be less than the current date")
        sys.exit(1)
    
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime={initial_date.year}-{initial_date.month}-{initial_date.day}%2000:00:00&endtime={end_date.year}-{end_date.month}-{end_date.day}%2023:59:59&minmagnitude=2.5&reviewstatus=reviewed&eventtype=earthquake,accidental%20explosion,acoustic%20noise,acoustic_noise,anthropogenic_event,building%20collapse,chemical%20explosion,chemical_explosion,collapse,debris%20avalanche,eq,experimental%20explosion,explosion,ice%20quake,induced%20or%20triggered%20event,industrial%20explosion,landslide,meteor,meteorite,mine%20collapse,mine_collapse,mining%20explosion,mining_explosion,not%20existing,not%20reported,not_reported,nuclear%20explosion,nuclear_explosion,other,other%20event,other_event,quarry,quarry%20blast,quarry_blast,rock%20burst,Rock%20Slide,rockslide,rock_burst,snow%20avalanche,snow_avalanche,sonic%20boom,sonicboom,sonic_boom,train%20crash,volcanic%20eruption,volcanic%20explosion&orderby=time"
    response = requests.get(url)

    if response.status_code == 200:
        with open("earthquake.csv", "wb") as file:
            file.write(response.content)
    else:
        print("Failed to download data")
        sys.exit(1)

if __name__ == "__main__":
    download_earthquake_data(datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(days=30))