# This file will contain utility functions for the chat application

import datetime

def get_current_time():
    """
    Returns the current time in ISO format
    """
    return datetime.datetime.now().isoformat()