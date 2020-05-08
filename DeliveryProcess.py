# imports required for script
from ExtractPackages import *
from ExtractLocations import *
from PackagesHashTable import *
from Truck import *
from LogisticsModel import *
from point import *
from time import sleep


class DeliveryProcess:
    """Interfaces between the ViewController and the LogisticsModel. It tells model what to do next and updates View."""

    # Time Complexity: O(1)
    def __init__(self, truck_location, map_locations, map_width, map_height, truck_image, canvas):
        """constructor that sets default values and provides DeliveryProcess with canvas information

        :param truck_location: current truck location (will be set to 0 because it will start at hub)
        :param map_locations: locations on the canvas where each address has its location represented
        :param map_width: width of canvas
        :param map_height: height of canvas
        :param truck_image: truck image
        :param canvas: canvas name
        """
        self.disable_animation = False
        self.clear_route = True

        self.truck_location = truck_location
        self.map_locations = map_locations
        self.map_width = map_width
        self.map_height = map_height
        self.truck_image = truck_image
        self.canvas = canvas

        self.locations_hit = 0
        self.move_to_location(0)
        self.fast_speed = False

        self.canvas_id_list = []

        # Get information from csv file containing location information and store in a list of Location objects
        locations = extract_locations_from_file("csvFiles/Locations.csv")

        # Get information from csv file containing package information and store in a list of PackageData objects
        packages = extract_packages_from_file("csvFiles/Packages.csv")

        # Make a blacklist for packages that will not be available from the start
        self.delay_list_id = []
        self.delay_list_time = []

        # Instantiate Hash Table Object
        self.package_table = PackagesHashTable(50)

        # create packages hash table from the array of Package objects
        for p in packages:
            if p.reroute_time != datetime.strptime('23:59 PM', '%H:%M %p').time():
                self.delay_list_id.append(p.package_id)
                self.delay_list_time.append(p.reroute_time)
                self.package_table.add(p.package_id, p.reroute_address, p.deadline, p.reroute_city, p.reroute_zip_code,
                                       p.weight, DeliveryStatus.AT_HUB)
            elif p.time_available != datetime.strptime('8:00 AM', '%H:%M %p').time():
                self.delay_list_id.append(p.package_id)
                self.delay_list_time.append(p.time_available)
                self.package_table.add(p.package_id, p.address, p.deadline, p.city, p.zip_code, p.weight,
                                       DeliveryStatus.AT_HUB)
            else:
                self.package_table.add(p.package_id, p.address, p.deadline, p.city, p.zip_code, p.weight,
                                       DeliveryStatus.AT_HUB)

        # set starting time
        current_time = datetime.strptime('8:00 AM', '%H:%M %p').time()

        # all package information will print out at these times (per assignment requirements)
        print_times = [datetime.strptime('9:00 AM', '%H:%M %p').time(),
                       datetime.strptime('10:00 AM', '%H:%M %p').time(),
                       datetime.strptime('13:00 PM', '%H:%M %p').time()]

        # Create truck number 1 (this truck will deliver all packages with deadlines)
        self.truck1 = Truck(1)
        # Create truck number 2 (will wait at hub until its time for priority packages)
        self.truck2 = Truck(2)

        # create logistics model object
        self.logistics_model = LogisticsModel(locations, self.package_table, current_time, print_times)

    # Time complexity O(n)
    def add_additional_package(self, p_id, address, deadline, city, zip_code, weight):
        """adds another package to be delivered to our package hash table

        :param p_id: unique package identifier
        :param address: delivery street address
        :param deadline: delivery deadline
        :param city: delivery city
        :param zip_code: delivery zip code
        :param weight: weight of package in kg
        :return:
        """
        self.package_table.add(p_id, address, deadline, city, zip_code, weight, DeliveryStatus.AT_HUB)

    # Time complexity O(1)
    def add_status_time(self, time):
        """forwards provided time to the logistics_model so that it knows when to print package status's

        :param time: new time to print out the package status's
        :return: none
        """
        self.logistics_model.add_status_time(time)

    # Time complexity O(n^2)
    def deliver_truck_one(self):
        """loops the process of loading truck 1 and delivering packages until all packages are delivered
        truck one deals with all packages that have a deadline
        :return: none
        """

        # already at hub so we can start at one (indicating that we can draw a circle at the next location)
        self.locations_hit = 1

        # load priority packages
        i = 1
        for p in self.package_table.hash_table:
            if type(p) is not EmptyBucket:
                if p[2] != datetime.strptime('23:59 PM', '%H:%M %p').time() and \
                        p[0] not in self.delay_list_id:
                    self.logistics_model.load_package(self.truck1, p[0])

        # Add additional packages that are heading to the same destination as a package with a deadline
        # time complexity: O(n^2)
        for included_package in self.truck1.loaded_packages:
            included_package_info = self.package_table.get_package(included_package)

            # loop through each package to see if we can find any that will be delivered to a location we are
            # already heading to
            for p in self.package_table.hash_table:
                if type(p) is not EmptyBucket:
                    # catch same location based on street name
                    if not p[0] in self.truck1.loaded_packages and p[1] == included_package_info[1] \
                            and p[6] == DeliveryStatus.AT_HUB:
                        if len(self.truck1.loaded_packages) < 15:
                            self.logistics_model.load_package(self.truck1, p[0])

        # package 19 will be loaded with 13 and 15, but will not be dropped off until packages with deadlines are gone
        self.logistics_model.load_package(self.truck1, 19)

        # begin delivering packages
        # time complexity: O(n^3)
        while len(self.truck1.loaded_packages) > 0:
            self.logistics_model.deliver_nearest_package(self.truck1)
            if self.locations_hit == 0:
                self.move_to_location(self.truck1.location_id, True, False, True)
            else:
                self.move_to_location(self.truck1.location_id, True, True, True)

            # when delayed packages become available we return to the hub to get any packages with deadlines
            has_returned = self.logistics_model.check_time_for_delayed_deliveries(self.truck1)
            if has_returned:
                self.locations_hit = 0
                self.move_to_location(self.truck1.location_id, True, True, True)
                i = 0
                while i < len(self.delay_list_id):

                    # check if the package is available
                    if self.delay_list_time[i] < self.logistics_model.current_time:
                        p_list = self.package_table.get_package(self.delay_list_id[i])

                        # only load packages that have a deadline
                        if p_list[2] != datetime.strptime('23:59 PM', '%H:%M %p').time():
                            self.logistics_model.load_package(self.truck1, self.delay_list_id[i])
                    i += 1

                #self.move_to_location(self.truck1.location_id, True, True, True)
            print("There are %s packages left on truck %s." % (len(self.truck1.loaded_packages),
                                                               self.truck1.truck_number))

    # Time complexity O(n^2)
    def deliver_truck_two(self):
        """loops through the process of loading truck 2 and delivering packages until all packages are delivered
        truck two deals with all packages that do not have a deadline
        :return: none
        """

        # reset locations
        self.locations_hit = 0

        # set truck image to hub, and delete last route from canvas if required
        if self.clear_route:
            self.reset_canvas()
        else:
            self.move_to_location(0)

        # Load the truck with as many packages as possible
        for p_add in self.package_table.hash_table:
            if type(p_add) is not EmptyBucket:
                if p_add[6] == DeliveryStatus.AT_HUB:
                    self.logistics_model.load_package(self.truck2, p_add[0])
                    # see if we can find any other packages heading to this location
                    for p in self.package_table.hash_table:
                        if type(p) is not EmptyBucket:
                            # catch same location based on street name
                            if not p[0] in self.truck2.loaded_packages and p[1] == p_add[1] \
                                    and p[6] == DeliveryStatus.AT_HUB:
                                if len(self.truck2.loaded_packages) < 15:
                                    self.logistics_model.load_package(self.truck2, p[0])

        # Deliver packages in the order of the nearest package
        while len(self.truck2.loaded_packages) > 0:
            self.logistics_model.deliver_nearest_package(self.truck2)
            if self.locations_hit == 0:
                self.move_to_location(self.truck2.location_id, True, False, True)
            else:
                self.move_to_location(self.truck2.location_id, True, True, True)
            print("There are %s packages left on truck %s." % (len(self.truck2.loaded_packages),
                                                               self.truck2.truck_number))

        # Drive back to the hub to pick up more packages
        self.logistics_model.return_to_hub(self.truck2)
        self.locations_hit = 0
        self.move_to_location(self.truck2.location_id, True, True, True)

        # Load the truck with as many packages as possible (This will load all remaining packages)
        for p in self.package_table.hash_table:
            if type(p) is not EmptyBucket:
                if p[6] == DeliveryStatus.AT_HUB:
                    self.logistics_model.load_package(self.truck2, p[0])

        # Deliver packages in the order of the nearest package
        # Time complexity O(n^2)
        while len(self.truck2.loaded_packages) > 0:
            self.logistics_model.deliver_nearest_package(self.truck2)
            self.move_to_location(self.truck2.location_id, True, True, True)
            print("There are %s packages left on truck %s." % (len(self.truck2.loaded_packages),
                                                               self.truck2.truck_number))

    # Time complexity O(n)
    def print_out_results(self):
        # Final print out statement to verify all packages have been delivered
        print("")
        print("FINAL PRINTOUT:")
        self.package_table.print_all_packages()

    # Time complexity O(n)
    def move_to_location(self, location_id, draw_line=False, draw_circle=False, should_animate=False):
        """ sends truck to a new location based on the location_id

        :param location_id: new location to travel to
        :param draw_line: bool determines if a line should be drawn
        :param draw_circle: bool determines if a circle should be drawn (no longer required)
        :param should_animate: bool determines if we should animate between locations
        :return: none
        """

        # do not draw circle if we haven't hit a location yet (prevents hub circle draw)
        if self.locations_hit == 0:
            draw_circle = False
        else:
            draw_circle = True
        self.locations_hit = self.locations_hit + 1
        self.relative_move_image(self.truck_location, float(self.map_locations[location_id].x),
                                 float(self.map_locations[location_id].y),self.map_width, self.map_height,
                                 self.truck_image, self.canvas, draw_line, draw_circle,should_animate)

    # Time complexity O(n)
    def relative_move_image(self, start_location, x_ratio, y_ratio, width, height, image, canvas,
                            should_draw_line=False, should_draw_circle=False, should_animate=False):
        """ Moves the truck location to new location and updates the canvas accordingly


        :param start_location: current location of the truck
        :param x_ratio: the ratio of the x coordinate for where the truck is going to the total width of the canvas
        :param y_ratio: the ratio of the y coordinate for where the truck is going to the total height of the canvas
        :param width: total width of the canvas
        :param height: total height of the canvas
        :param image: truck image
        :param canvas: canvas name
        :param should_draw_line: bool that determines if we will draw a line between the locations
        :param should_draw_circle: bool that determines if we will add a circle to the location traveled to
        :param should_animate: bool that determines if we will animate between locations
        :return: none
        """

        # determine how far in x and y pixels on the canvas the image needs to move
        # the x_ratio and y_ratio describe the amount in those directions relative to the width and height
        # so, the ratio values are provided in the range of (0.0 - 1.0)
        move_amount = Point()
        move_amount.x = width * x_ratio - start_location.x
        move_amount.y = height * y_ratio - start_location.y

        # If we would like to animate the truck image movement, we need to calculate what the smaller move amounts to
        # use that will add up to the total move. We then loop, moving small amounts and delaying.
        # Ultimately, the total amount moved (num_movements * delta) will be the same as move_amount
        current_location = Point()
        if self.disable_animation:
            should_animate = False
        if should_animate:
            # keep track of our image's current location
            current_location.x = start_location.x
            current_location.y = start_location.y

            # calculate small movements
            if self.fast_speed:
                num_movements = 35
                sleep_val = 0.005
            else:
                num_movements = 50
                sleep_val = 0.01

            delta_x = move_amount.x / num_movements
            delta_y = move_amount.y / num_movements

            # loop through the movements and delay
            counter = 0
            while counter < num_movements:
                sleep(sleep_val)
                current_location.x = current_location.x + delta_x
                current_location.y = current_location.y + delta_y
                canvas.move(image, delta_x, delta_y)
                canvas.update()
                counter += 1

            # calculate if there is any remaining distance that the animated move fell short of (there will be some
            # small amount due to the limits of floating point operation precision [or at least this is what I believe])
            move_amount.x = width * x_ratio - current_location.x
            move_amount.y = height * y_ratio - current_location.y

        # if we don't want to animate, we can just add the move amount
        else:
            current_location.x = start_location.x + move_amount.x
            current_location.y = start_location.y + move_amount.y

        # draw a line between where we started to the location we ended up at
        if should_draw_line:
            """
            self.canvas_id_list.append(canvas.create_line(start_location.x, start_location.y,
                                       start_location.x + move_point.x, start_location.y + move_point.y))
            """
            self.canvas_id_list.append(canvas.create_line(start_location.x, start_location.y,
                                                          current_location.x,
                                                          current_location.y))

        # create a circle at the location we left displaying how many packages have been dropped off this trip
        if should_draw_circle:
            self.create_circle(current_location.x, current_location.y, 8, canvas)

        # move to the final destination
        canvas.move(image, move_amount.x, move_amount.y)

        # update the reference to the trucks location
        start_location.x = current_location.x
        start_location.y = current_location.y

    # Time Complexity: O(1)
    def create_circle(self, x, y, r, canvas_name):
        """Creates a circle at the coordinates provided with the radius provided."""
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r

        # Draws circle to canvas
        self.canvas_id_list.append(canvas_name.create_oval(x0, y0, x1, y1, fill="#fff"))

        # Draws text to canvas displaying how many packages have been delivered at the time of this delivery
        self.canvas_id_list.append(canvas_name.create_text(x, y, font="Times 8 bold",
                                                           text=self.logistics_model.packages_delivered))

    # Time Complexity: O(n)
    def reset_canvas(self):
        """Removes the lines and circles from the canvas and updates the truck location to the hub for next delivery."""
        for canvas_id in self.canvas_id_list:
            self.canvas.delete(canvas_id)
        self.move_to_location(0)
