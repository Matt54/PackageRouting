# imports required for script
import csv
from PackageData import *


# Time Complexity: O(n^2)
def extract_packages_from_file(filename):
    """Creates an array of Package objects from the string path to a prepared csv file.

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
        package_id = []
        address = []
        city = []
        state = []
        zip_code = []
        deadline = []
        mass = []
        time_available = []
        specific_truck = []
        co_packages = []
        reroute_time = []
        reroute_address = []
        reroute_city = []
        reroute_state = []
        reroute_zip = []
        notes = []

        # parse each column of a row
        for row in rows:
            count = 1
            for col in row:
                if count == 1:
                    package_id.append(col)
                elif count == 2:
                    address.append(col)
                elif count == 3:
                    city.append(col)
                elif count == 4:
                    state.append(col)
                elif count == 5:
                    zip_code.append(col)
                elif count == 6:
                    deadline.append(col)
                elif count == 7:
                    mass.append(col)
                elif count == 8:
                    time_available.append(col)
                elif count == 9:
                    specific_truck.append(col)
                elif count == 10:
                    co_packages.append(col)
                elif count == 11:
                    reroute_time.append(col)
                elif count == 12:
                    reroute_address.append(col)
                elif count == 13:
                    reroute_city.append(col)
                elif count == 14:
                    reroute_state.append(col)
                elif count == 15:
                    reroute_zip.append(col)
                elif count == 16:
                    notes.append(col)
                count = count + 1

        # create and return an array of PackageData
        packages = []
        i = 0
        while i < len(package_id):
            packages.append(PackageData(package_id[i], address[i], city[i], state[i], zip_code[i],
                                        deadline[i], mass[i], time_available[i], specific_truck[i],
                                        co_packages[i], reroute_time[i], reroute_address[i],
                                        reroute_city[i], reroute_state[i], reroute_zip[i]))
            i += 1
        return packages
