import logging

from datetime import datetime
from dateutil import tz
from dateutil.relativedelta import relativedelta

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_current_datetime() -> str:
    return datetime.now(tz = tz.gettz(configs.TIMEZONE_PH)).replace(tzinfo=None)


def get_date_str_from_datetime(date_obj, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    try:
        return date_obj.strftime(format)
    except Exception as error:
        logger.error(f"Failed to parse date: {error}")
        return ""


def is_valid_date_format(date_str: str, format: str) -> bool:
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False
    

def get_date_difference(**kwargs) -> int:
    date_from: str = kwargs.get("date_from", "")
    date_to: str = kwargs.get("date_to", "")
    date_format: str = kwargs.get("date_format", "%Y-%m-%d %H:%M:%S")
    return_unit: str = kwargs.get("return_unit" , "").lower()
    timezone: str = kwargs.get("timezone", "Asia/Manila")

    if not return_unit in ["year", "month", "day", "hour", "minute", "second"]:
        print("Invalid return_unit. Must be year, month, day, hour, minute, or second.")
        return 0

    try:  
        tzinfo = tz.gettz(timezone)
        from_date = datetime.strptime(date_from, date_format).replace(tzinfo=tzinfo)
        to_date = datetime.strptime(date_to, date_format).replace(tzinfo=tzinfo)
    except Exception as error:
        print(f"Error parsing date: {error}")
        return 0

    difference = relativedelta(to_date, from_date)

    if return_unit == "year":
        return difference.years + (difference.months // 12) + (difference.days // 365)
    elif return_unit == "month":
        return difference.years * 12 + difference.months + (difference.days // 30)
    elif return_unit == "day":
        return (to_date - from_date).days
    elif return_unit == "hour":
        return int((to_date - from_date).total_seconds() // 3600)
    elif return_unit == "minute":
        return int((to_date - from_date).total_seconds() // 60)
    elif return_unit == "second":
        return int((to_date - from_date).total_seconds())
    return 0

def to_full_date_format(**kwargs) -> str:
    try:
        date_str = kwargs.get("date", "")
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except Exception as error:
        logger.error(f"Failed to parse date: {error}")
        return ""

def calculate_date_difference(**kwargs) -> int:
    from_date = kwargs.get("from_date", "")
    to_date = kwargs.get("to_date", "")
    unit = kwargs.get("unit", "day")
    format = kwargs.get("format", "%Y-%m-%d %H:%M:%S")
    
    try:
        timezone = tz.gettz('Asia/Manila')
        from_date_obj = datetime.now(timezone)
        to_date_obj = datetime.now(timezone)
        
        if from_date:
            from_date_obj = datetime.strptime(from_date, format).replace(tzinfo=timezone)

        if to_date:
            to_date_obj = datetime.strptime(to_date, format).replace(tzinfo=timezone)

        delta = to_date_obj - from_date_obj

        if unit == "year":
            return delta.days // 365
        elif unit == "month":
            return delta.days // 30
        elif unit == "day":
            return delta.days
        elif unit == "hour":
            return int(delta.total_seconds() // 3600)
        elif unit == "minute":
            return int(delta.total_seconds() // 60)
        elif unit == "second":
            return int(delta.total_seconds())
        else:
            raise ValueError("Invalid unit. Use 'year', 'month', 'day', 'hour', 'minute', or 'second'.")
    except ValueError as e:
        print(f"Error: {e}")
        return -1

def get_issue_start_date() -> str:
    curr_date = datetime.now(tz = tz.gettz(configs.TIMEZONE_PH)).replace(tzinfo=None)
    return curr_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'