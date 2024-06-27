from datetime import datetime, timedelta

def mjd_to_utc(mjd):
    # Convert MJD to JD
    jd = mjd + 2400000.5

    # Convert JD to a datetime object
    jd_epoch = datetime(1858, 11, 17, 0, 0, 0)
    days_since_jd_epoch = jd - 2400000.5
    utc_time = jd_epoch + timedelta(days=days_since_jd_epoch)
    
    return utc_time

def utc_to_mjd(utc_time):
    # Convert datetime object to JD
    jd_epoch = datetime(1858, 11, 17, 0, 0, 0)
    days_since_jd_epoch = (utc_time - jd_epoch).days
    jd = 2400000.5 + days_since_jd_epoch

    # Convert JD to MJD
    mjd = jd - 2400000.5

    return mjd

def mjd_to_epoch(mjd):
    # Convert to UTC and then to EPOCH
    return utc_to_epoch(mjd_to_utc(mjd))

def epoch_to_mjd(epoch_time):
    # Convert to UTC and then to MJD
    return utc_to_mjd(epoch_to_utc(epoch_time))

def utc_to_epoch(utc_time):
    return utc_time.timestamp()

def epoch_to_utc(epoch_time):
    return datetime.fromtimestamp(epoch_time)

def swift_to_epoch(grb_date, time_ut):
    # Remove any trailing letters from the GRB date
    grb_date = ''.join(filter(str.isdigit, grb_date))
    # Convert GRB date to standard date format
    date_str = f"20{grb_date[0:2]}-{grb_date[2:4]}-{grb_date[4:6]}"
    
    # Normalize time format to HH:MM:SS
    if '.' in time_ut:  # Check for fractional seconds
        time_ut = time_ut.split('.')[0]  # Remove fractional seconds

    # Split time into hours, minutes, and seconds
    time_parts = time_ut.split(':')
    # Pad hours, minutes, and seconds with zeros if they are missing
    time_parts = [part.zfill(2) for part in time_parts]
    # Ensure time_parts has exactly 3 elements (hours, minutes, seconds)
    while len(time_parts) < 3:
        time_parts.append('00')  # Add missing seconds or minutes as '00'

    # Combine hours, minutes, and seconds
    time_ut = ':'.join(time_parts)
    
    # Combine date and time
    datetime_str = f"{date_str} {time_ut}"
    
    # Convert to epoch
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    epoch_time = datetime_obj.timestamp()
    
    return epoch_time