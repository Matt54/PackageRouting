# imports required for script
import csv
from Location import *


# Time Complexity: O(n^2)
def extract_locations_from_file(filename):
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
        address = []
        city = []
        state = []
        zip_code = []
        all_distances = []

        # parse each column of a row
        for row in rows:
            count = 1
            location_distances = []
            distance_index = 0
            for col in row:
                if count == 1:
                    location_id.append(col)
                elif count == 2:
                    address.append(col)
                elif count == 3:
                    city.append(col)
                elif count == 4:
                    state.append(col)
                elif count == 5:
                    zip_code.append(col)
                elif count > 5:
                    location_distances.append(float(col))
                    distance_index += 1
                count = count + 1
            all_distances.append(location_distances)

        # create and return a list of Locations
        locations = []
        i = 0
        while i < len(location_id):
            locations.append(Location(address[i], city[i], state[i], zip_code[i], location_id[i]))
            for specific_distance in all_distances[i]:
                locations[i].add_distance(specific_distance)
            i += 1
        return locations
