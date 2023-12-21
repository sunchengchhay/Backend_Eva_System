from datetime import datetime,timedelta 


#convert string format to datetime format "YYYY-MM-DD HH:MM:SS"
def custom_datetime_cambodia(date_string):
    return datetime.strptime(date_string,'%Y-%m-%d %H:%M:%S')


def current_time_cambodia():
    # Create a timedelta representing the UTC offset for Cambodia (UTC+7)
    cambodia_utc_offset = timedelta(hours=7)

    # Get the current time in UTC
    current_time_utc = datetime.utcnow().replace(microsecond=0)
    
    return current_time_utc + cambodia_utc_offset