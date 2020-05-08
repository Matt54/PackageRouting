class Truck:
    """Represents a delivery truck"""

    # Time Complexity: O(1)
    def __init__(self, truck_number):

        # Store the truck number for identification
        self.truck_number = truck_number

        # Empty List that will hold our packages currently loaded
        self.loaded_packages = []

        # Start at the hub (location_id for hub is 0)
        self.location_id = 0

    # Time Complexity: O(1)
    def load_package(self, package_id):
        """loads a package as long as the truck is not full

        :param package_id: unique identifier for package to load
        :return: True if loaded, False if truck was full
        """

        # only load the package if it can fit
        if len(self.loaded_packages) < 16:
            self.loaded_packages.append(package_id)
            return True
        else:
            return False

    # Time Complexity: O(1)
    def deliver_package(self, package_id):
        """ removes the package from the truck if it exists

        :param package_id: unique identifier for package to deliver
        :return: True if delivered, False if package was not on truck
        """

        # only deliver the package if it exists on the truck
        if package_id in self.loaded_packages:
            self.loaded_packages.remove(package_id)
            return True
        else:
            print("Truck %s is not loaded with package %s" % (self.truck_number, package_id))
            return False

    # Time Complexity: O(1)
    def set_location(self, location_id):
        """set new location for truck (distance/time will get calculated outside the class)

        :param location_id: Sets the location of the truck to a new location
        :return: none
        """

        # set new value and print for debugging purposes
        self.location_id = location_id
        print("Truck %s location updated to %s" % (self.truck_number, location_id))
