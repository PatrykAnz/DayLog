import datetime
from backend.common.logging_config import logger


def get_clock():
    current_time = datetime.datetime.now()
    
    clock_data = {
        "year": current_time.year,
        "month": current_time.month,
        "day": current_time.day,
        "hour": current_time.hour,
        "minute": current_time.minute,
    }
    
    logger.info(f"Current time: {clock_data}")
    return clock_data