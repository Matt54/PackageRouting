# imports required for script
from datetime import datetime, timedelta, date


# Time Complexity: O(1)
def add_minutes_to_time(current_time, added_minutes):
    """convenient function for adding minutes to time

    :param current_time: the current time of the day
    :param added_minutes: the amount of minutes we need to add to the time
    :return: the new time
    """
    delta = timedelta(minutes=added_minutes)
    return (datetime.combine(date(1, 1, 1), current_time) + delta).time()


# Time Complexity: O(1)
def calculate_travel_time_in_minutes(distance):
    """converts a distance in miles to the time in minutes it would take traveling at an average of 18 mph

    :param distance: distance to travel
    :return: time it will take to travel distance
    """
    return distance / 18 * 60
