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