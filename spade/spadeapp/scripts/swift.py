import requests
from bs4 import BeautifulSoup
from time_related import swift_to_epoch


def convert_to_float(coord_str):
    """
    Convert a BAT RA or BAT DEC string to a float representing degrees.
    
    Parameters:
    coord_str (str): The coordinate string (e.g., "-60.637-60:38:13.2" or "40.23402:40:56.2")
    
    Returns:
    float: The coordinate in decimal degrees.
    """
    if '-' in coord_str and coord_str[0] != '-':
        parts = coord_str.split('-')
        sign = -1
        decimal_degrees = float(parts[0])
        dms = parts[1]
    else:
        sign = 1
        if coord_str[0] == '-':
            parts = coord_str.split('-', 2)
            sign = -1
            decimal_degrees = float(parts[1])
            dms = parts[2]
        else:
            parts = coord_str.split(':', 1)
            decimal_degrees = float(parts[0][:-2])
            dms = coord_str[len(parts[0][:-2]):]

    dms_parts = dms.split(':')
    if len(dms_parts) != 3:
        raise ValueError("Input string is not in the correct format")
    
    degrees = float(dms_parts[0])
    minutes = float(dms_parts[1])
    seconds = float(dms_parts[2])
    
    # Convert to decimal degrees
    additional_degrees = degrees + minutes / 60 + seconds / 3600
    
    return sign * (decimal_degrees + additional_degrees / 100)


def download_swift_data():
    """
    Downloads data from Swift and saves it as a CSV file.
    """
    url = "https://swift.gsfc.nasa.gov"

    # Get the page content
    response = requests.get(url + "/archive/grb_table/fullview/")

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Assuming the table is the first or only table in the page
        table = soup.find("table")
        rows = table.find_all("tr")

        # Extracting header
        headers = [header.text for header in rows[0].find_all("th")]

        # Remove the 32th column from the header (Comments column)
        headers.append("Normalised Duration")

        # Remove all other instances of the same header (<thead> tag) and leave only the first one
        for index, thead in enumerate(table.find_all("thead")):
            if index != 0:
                thead.decompose()

        # Replace the first header with "Trigger Time"
        headers[0] = "GRB Name"
        headers[1] = "Trigger Time"
        headers[3] = "BAT Ra"
        headers[4] = "BAT Dec"
        headers[6] = "BAT T90"

        headers = [headers[0], headers[1], headers[3], headers[4], headers[6], headers[7], headers[21]]

        headers.append("Ra")
        headers.append("Dec")

        headers.append("Normalised Duration")

        # Remove all text inside parentheses
        headers = [header.split("(")[0].strip() for header in headers]

        # Write the CSV data to a file
        with open("swift.csv", "w", encoding="utf-8", newline='') as file:
            # write header without csv library
            file.write(";".join(headers) + "\n")
            for row in rows[1:]:  # Skip header row
                cols = [ele.text.strip().replace(";", ",") for ele in row.find_all(["td", "th"])]
                cols = [col if col != "n/a" else "" for col in cols]

                if cols:  # If the row was not empty
                    # Convert the date to epoch time

                    cols = [cols[0], cols[1], cols[3], cols[4], cols[6], cols[7], cols[8], cols[21]]

                    if cols[5] != "" and cols[6] != "":
                        cols[5] = f"{cols[5]}+/-{cols[6]}"

                    cols.pop(6)

                    try:
                        cols.append(str("{:.3f}".format(convert_to_float(cols[2]))))
                        cols.append(str("{:.3f}".format(convert_to_float(cols[3]))))

                        cols[2] = cols[2].rstrip('0').rstrip('.')
                        cols[3] = cols[3].rstrip('0').rstrip('.')
                    except:
                        cols.append("")
                        cols.append("")

                    cols.append(cols[4])
                    cols[1] = str(swift_to_epoch(cols[0], cols[1]))
                    file.write(";".join(cols) + "\n")
    else:
        print("Failed to download data")
        return


if __name__ == "__main__":
    download_swift_data()
