# imports required for script
import csv
from MapLocation import *


# Time Complexity: O(n^2)
def extract_graphic_locations_from_file(filename):
    """Creates an array of Location objects from the string path to a prepared csv file.

            Args:
                filename (str): relative path to the .csv file.

            Returns:
                packages (Package[]): array of Package objects.
    """

    # opens the filename under the alias csv_file
    with open(filename) as csv_file:
        my_reader = csv.reader(csv_file, delimiter=",", quotechar='"')

        # skips the header row
        next(my_reader)

        # add each row to a list of rows
        rows = []
        for row_data in my_reader:
            rows.append(row_data)

        # create empty arrays to store individual package data properties
        location_id = []
        x = []
        y = []

        # parse each column of a row
        for row in rows:
            count = 1
            location_distances = []
            distance_index = 0
            for col in row:
                if count == 1:
                    location_id.append(col)
                elif count == 2:
                    x.append(col)
                elif count == 3:
                    y.append(col)
                count = count + 1

        # create and return an array of MapLocation's
        map_locations = []
        i = 0
        while i < len(location_id):
            map_locations.append(MapLocation(location_id[i], x[i], y[i]))
            i += 1
        return map_locations
