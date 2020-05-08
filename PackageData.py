# imports required for script
from datetime import datetime


class PackageData:
    """PackageData represents all input data about a package.

    Attributes
        package_id (int): unique identifier for the package
        location (obj): container of address, city, state, and zip code
        deadline (datetime): constraint regarding the time the package must arrive by
        mass (int): weight of object in kilograms
        time_available (datetime): constraint regarding when the package can leave the hub
        specific_truck (int): constraint linking to a specific truck that much deliver the package
        co_packages (int[]): constraint linking other specific packages that must travel with this package
        reroute_time (datetime): time that the package gets rerouted to new address
        reroute_location (obj): container of new address, city, state, and zip code that the package is rerouted to
    """

    # Time Complexity: O(n)
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight,
                 time_available, specific_truck, co_packages, reroute_time,
                 reroute_address, reroute_city, reroute_state, reroute_zip):
        """Constructor populates the object with all relevant information about a package

        :param package_id: unique identifier for package
        :param address: street address
        :param city: city
        :param state: state
        :param zip_code: zip code
        :param deadline: delivery deadline
        :param weight: weight of package in kg
        :param time_available: time the package will be available
        :param specific_truck: specific truck that the package must travel on
        :param co_packages: other packages that the package must travel with
        :param reroute_time: time that the package will be rerouted
        :param reroute_address: street address the package will be rerouted to
        :param reroute_city: city the package will be rerouted to
        :param reroute_state: state the package will be rerouted to
        :param reroute_zip: zip code the package will be rerouted to
        """

        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.time_available = datetime.strptime(time_available, '%H:%M %p').time()
        self.specific_truck = specific_truck
        self.reroute_address = reroute_address
        self.reroute_city = reroute_city
        self.reroute_state = reroute_state
        self.reroute_zip_code = reroute_zip

        # Convert strings to an actual time
        if deadline == 'EOD':
            self.deadline = datetime.strptime('23:59 PM', '%H:%M %p').time()
        else:
            self.deadline = datetime.strptime(deadline, '%H:%M %p').time()

        # Create a list of co packages by parsing string
        self.co_packages = []
        if co_packages != '':
            packs = co_packages.split('_')
            for p in packs:
                self.co_packages.append(p)

        # Convert strings to an actual time
        if reroute_time != '':
            self.reroute_time = datetime.strptime(reroute_time, '%H:%M %p').time()
        else:
            self.reroute_time = datetime.strptime('23:59 PM', '%H:%M %p').time()
