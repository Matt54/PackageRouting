# imports required for script
from LocationLogic import *
from TimeKeeping import *
from DeliveryStatus import *


class LogisticsModel:
    """Does the actual package delivery based on being signaled to do so by the DeliveryProcess."""

    # Time Complexity: O(1)
    def __init__(self, locations, packages, current_time, print_times):
        """Constructor relays the location, package information, and status times to the object."""
        self.locations = locations
        self.packages = packages
        self.current_time = current_time
        self.traveled_distance = 0
        self.packages_delivered = 0

        self.delivered_list = []

        # these variables will be used for printing out package information at a specific time
        self.print_times = print_times
        self.found_delay_time = False
        self.has_returned_for_delays = False
        self.delay_time = datetime.strptime('9:00 AM', '%H:%M %p').time()

        self.still_priority = True
        self.non_priority_found = 0

    # Time Complexity: O(1)
    def add_status_time(self, time):
        """Adds a new time to print out the packages' status"""
        self.print_times.append(time)

    # Time Complexity: O(1)
    def load_package(self, truck, package_id):
        """Adds package index to truck list as long as it's not full."""

        # load the truck
        did_load = truck.load_package(package_id)

        # truck is full if it doesn't load
        if did_load:
            # set the package status
            self.packages.update_package_status(package_id, DeliveryStatus.IN_ROUTE)

            # print out statement
            print("")
            print("Truck %s has loaded package %s, it is now holding %s packages"
                  % (truck.truck_number, package_id, len(truck.loaded_packages)))

            if len(truck.loaded_packages) == 16:
                print("")
                print("Truck %s is full" % truck.truck_number)

    # Time Complexity: O(n^2)
    # Greedy algorithm - This is a self-adjusting algorithm which chooses the next package based on the logic:
    # "What location is closest to the truck's current location that the truck has a package loaded for?"
    def deliver_nearest_package(self, truck):
        """Determines which package to deliver next, and then delivers that package."""

        # if more than one package is loaded on truck, determine closest location that requires a package
        if len(truck.loaded_packages) > 1:
            package_id_to_deliver = self.determine_closest_delivery_location(truck)
        # if we only have one package, that one will be delivered
        else:
            package_id_to_deliver = truck.loaded_packages[0]
        self.deliver_package(truck, package_id_to_deliver)
        return True

    # Complexity: O(n^2) (Greedy algorithm)
    def determine_closest_delivery_location(self, truck):
        """determine_closest_delivery_location
         Nested loops:
         - loop 1 finds the nearest location to our current location
         - loop 2 determines if the truck has a package that needs to go there (returns the package_id if found)
        """

        # loop through all the locations available to travel to
        index = 0
        while index < len(self.locations):

            # finds the next closest location
            sorted_locations = sorted(self.locations[truck.location_id].distances)
            potential_distance = sorted_locations[index]

            # sometimes there are multiple locations that have the same distance from the current location
            # we deal with this by creating a list to go through of locations at that distance
            # typically it's just a list of one index, but we have to be able to handle more than one
            number_of_locations_at_distance = self.locations[truck.location_id].distances.count(potential_distance)
            location_indexes_at_distance = []

            # search the distances from the trucks current location to determine the index of our current distance
            # location_index = self.locations[truck.location_id].distances.index(potential_distance)
            loc_index = 0
            while loc_index < number_of_locations_at_distance:
                location_indexes_at_distance.append([i for i, n in enumerate(self.locations[truck.location_id].distances)
                                                     if n == potential_distance][loc_index])
                loc_index += 1

            # Loop through all the packages and check if one needs to travel to the location (if so, return package_id)
            for p_id in truck.loaded_packages:
                p_list = self.packages.get_package(p_id)
                for location_index in location_indexes_at_distance:
                    if self.locations[location_index].is_equal(p_list[1], p_list[3], "UT", p_list[4]):
                        # found our package!
                        if p_list[0] != 19:  # we ignore package 19 until no priority packages are left on the truck
                            return p_id
            index += 1

    # Time Complexity: O(1)
    def deliver_package(self, truck, package_id):
        """removes package from truck's loaded package list and updates the package, truck, current time, and distance.
        deliver_package has the following effects:
        1) truck location is updated to input package location
        2) distance to package location from previous location is calculated and added to distance traveled
        3) time required to travel distance is calculated and added to current time
        4) package is removed from truck list and its status is updated to DELIVERED
        """

        # determine where the package is going
        location_id = int(get_location_id_from_package_id(self.locations, self.packages, package_id))

        # determine distance to travel
        distance = float(self.locations[truck.location_id].distances[location_id])
        self.traveled_distance += distance

        # determine amount of time it will take in minutes
        minutes_to_travel = calculate_travel_time_in_minutes(distance)

        # add minutes to current time
        self.current_time = add_minutes_to_time(self.current_time, minutes_to_travel)

        # catch if we need to return back for the delayed packages
        if self.current_time > self.delay_time and not self.found_delay_time:
            print("")
            print("FLAG IS SET TO RETURN TO HUB NEXT FOR DELAYED PACKAGES")
            self.found_delay_time = True

        # catch if we need to print out the packages' statuses
        for check_time in self.print_times:
            if self.current_time > check_time:
                print("")
                print("Printing report for time: %s " % check_time.strftime('%H:%M %p'))
                self.packages.print_all_packages()
                self.print_times.remove(check_time)

        # update truck location
        truck.location_id = location_id

        # update package status
        self.packages.update_package_status(package_id, DeliveryStatus.DELIVERED)

        # remove package from truck list
        truck.deliver_package(package_id)

        # add to number of packages delivered
        self.packages_delivered += 1
        if package_id in self.delivered_list:
            print("Package %s is already delivered" % package_id)
        else:
            self.delivered_list.append(package_id)

        # print out statements for debugging
        print("")
        print("Truck %s has delivered package %s to %s"
              % (truck.truck_number, package_id, self.locations[location_id].print_pretty()))
        print("Delivery took about %s minutes, current time is now %s" % (round(minutes_to_travel), self.current_time))
        print("Delivery distance was %s, current total miles: %s" % (distance, round(self.traveled_distance)))
        print("Total number of packages delivered: %s" % self.packages_delivered)

    # Time Complexity: O(1)
    def return_to_hub(self,truck):
        """returns truck back to hub location and updates current time and distance traveled"""

        # determine distance to travel
        distance = float(self.locations[truck.location_id].distances[0])
        self.traveled_distance += distance

        # determine amount of time it will take in minutes
        minutes_to_travel = calculate_travel_time_in_minutes(distance)

        # add minutes to current time
        self.current_time = add_minutes_to_time(self.current_time, minutes_to_travel)

        # update truck location
        truck.location_id = 0
        self.has_returned_for_delays = True
        print("")
        print("Truck %s has returned to hub." % truck.truck_number)
        print("Driving took about %s minutes, current time is now %s" % (round(minutes_to_travel), self.current_time))
        print("Driving distance was %s, current total miles: %s" % (distance, round(self.traveled_distance)))

    # Time Complexity O(1)
    def check_time_for_delayed_deliveries(self,truck):
        """Signals that we need to return back to hub for delayed packages"""
        if self.found_delay_time and not self.has_returned_for_delays:
            self.return_to_hub(truck)
            return True
        else:
            return False