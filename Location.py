class Location:
    """A unique identifier tied to a street address, city, state, and zip code"""

    # Time Complexity: O(1)
    def __init__(self, address, city, state, zip_code, location_id):
        """constructor populates the location information

        :param address: street address
        :param city: city
        :param state: state
        :param zip_code: zip code
        :param location_id: unique identifier for location
        """

        # store basic information about the location
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

        # unique identifier for the location
        self.location_id = location_id

        # create empty dictionary to store distances to other locations
        self.distances = []

    # Time Complexity: O(1)
    def __eq__(self, other):
        """equality override - checks if street address, city, state, and zip code are equal

        :param other: another location object
        :return: bool indicating if the locations are equal
        """
        if self.address == other.address and \
           self.city == other.city and \
           self.state == other.state and \
           self.zip_code == other.zip_code:
            return True
        else:
            return False

    # Time Complexity: O(1)
    def is_equal(self, address, city, state, zip_code):
        """checks if inputted street address, city, state, and zip code are equal to our location's fields

        :param address: street address
        :param city: city
        :param state: state
        :param zip_code: zip code
        :return:  bool indicating if the locations are the same
        """
        if self.address == address and \
           self.city == city and \
           self.state == state and \
           self.zip_code == zip_code:
            return True
        else:
            return False

    # Time Complexity: O(1)
    def add_distance(self, distance):
        """adds a distance to the location at the location id that is the same as our list index

        :param distance: distance in miles to another location
        :return: none
        """
        self.distances.append(distance)

    # Time Complexity: O(1)
    def print_distances(self):
        """prints out list of distances for this location

        :return: none
        """
        print(self.distances)

    # Time Complexity: O(1)
    def print_pretty(self):
        """prints out location information

        :return:none
        """
        return self.address + ', ' + self.city + ', ' + self.state + ', ' + self.zip_code
