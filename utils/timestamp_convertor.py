from datetime import datetime

def iso8601_to_unix_timestamp(iso_str):
    dt_obj = datetime.fromisoformat(iso_str)
    unix_timestamp = int(dt_obj.timestamp())
    return unix_timestamp