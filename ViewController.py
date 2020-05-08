# imports required for script
import tkinter
from tkinter import *
from tkinter.ttk import *
from DeliveryProcess import *
from ExtractGraphicLocations import *
from point import *
from platform import system


class ViewController:
    """Maintains the graphical view and the flow of the program based on the user's interaction."""

    # Time complexity: O(1)
    def __init__(self):
        """Creates the graphical window."""

        # Create Window (non-resizable)
        # This is not a GUI focused project, sorry for the lack of responsive design.
        self.root = Tk()
        self.root.title('Package Routing Application - by Matt Pfeiffer')
        self.root.resizable(0, 0)

        # determine our operating system - I designed it on Windows, so default values are for Windows
        # if we catch macOS, things adjust a bit. Still doesn't look ideal; tkinter doesn't play well with macOS.
        self.is_mac = False
        if system() == 'Darwin':
            self.is_mac = True

        # convenient variables for adjusting user interface layout
        x_pad = 12
        x_pad_c = x_pad + 21
        y_pad = 10
        y_pad_minor = 2
        title_font = "Calibri 14"
        my_font = "Calibri 10"
        cb_font = "Calibri 8"
        l_width = 10
        e_width = 18
        combo_width = e_width
        back_color = '#AAAAAA'
        r_space_add = 17
        next_button_width = 31

        # magic GUI adjustment numbers for macOS
        if self.is_mac:
            x_pad_c = x_pad - 5
            next_button_width = 21
            r_space_add = 14

        # Get information from csv file containing location information so we can populate our address Combobox
        # and use the selection to populate the city and zip code fields
        # time complexity O(n)
        self.locations = extract_locations_from_file("csvFiles/Locations.csv")
        self.addresses = []
        for loc in self.locations:
            if loc.address not in self.addresses:
                self.addresses.append(loc.address)

        # this frame will hold the entire user interface
        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.pack(side=LEFT, fill=tkinter.BOTH, expand=1)
        self.main_frame['bg'] = back_color

        # create frame to hold the canvas (this will be our left frame)
        self.canvas_frame = tkinter.Frame(self.root)
        self.canvas_frame.pack(in_=self.main_frame, side=tkinter.LEFT, fill=tkinter.BOTH, expand=1,
                               padx=(x_pad,0), pady=y_pad)
        self.canvas_frame.config(bd=2, relief=tkinter.RAISED)

        # create canvas
        self.canvas = tkinter.Canvas(self.root)

        # Stretch canvas to root window size.
        self.canvas.pack(in_=self.canvas_frame,fill=tkinter.BOTH, expand=1)

        # Create map image
        self.image_map_raw = tkinter.PhotoImage(file="graphics/map.gif")
        self.image_map_canvas = self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.image_map_raw)

        # Create truck image
        self.truck_image_raw = tkinter.PhotoImage(file="graphics/my_truck2.gif")
        self.truck_location = Point(self.truck_image_raw.width() / 2, self.truck_image_raw.height() / 2)
        self.truck_image = self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.truck_image_raw)

        # get the width and height of the map image
        self.map_width = self.image_map_raw.width()
        self.map_height = self.image_map_raw.height()

        # Get information from csv file containing coordinate information for each location (for graphic display)
        self.map_locations = extract_graphic_locations_from_file('csvFiles/GraphicsLocations.csv')

        # Create logical delivery model object (it is provided references to view objects for updating display)
        self.delivery_process = DeliveryProcess(self.truck_location, self.map_locations, self.map_width,
                                                self.map_height, self.truck_image, self.canvas)

        # Create frame to contain the elements on the right side of the user interface
        self.right_frame = tkinter.Frame(self.root)
        self.right_frame.pack(in_=self.main_frame)
        self.right_frame['bg'] = back_color

        # validation method to restrict certain entry fields to numbers only
        numbers_validate = (self.root.register(self.validate_numeric), '%S')

        # Create frame to contain the elements involved in adding a time to check the status of our packages
        self.package_status_frame = tkinter.Frame(self.root)
        self.package_status_frame.pack(in_=self.right_frame, padx=x_pad, pady=y_pad)
        self.package_status_frame.config(bd=2, relief=tkinter.RAISED)
        # title
        self.package_status_title = tkinter.Label(self.root, text="Check Package Status", font=title_font)
        self.package_status_title.pack(in_=self.package_status_frame, side=tkinter.TOP, padx=x_pad, pady=y_pad)
        # hour
        self.hour_frame = tkinter.Frame(self.root)
        self.hour_frame.pack(in_=self.package_status_frame, side=tkinter.TOP, fill=tkinter.BOTH, pady=y_pad_minor)
        self.hour_label = tkinter.Label(self.root, text="Hour", width=l_width, font=my_font)
        self.hour_label.pack(in_=self.hour_frame, side=tkinter.LEFT, padx=(x_pad, 0))
        self.hour_entry = tkinter.Entry(self.root, width=e_width, font=my_font, justify='center',
                                        validate='key', vcmd=numbers_validate)
        self.hour_entry.pack(in_=self.hour_frame, side=tkinter.LEFT, padx=(0, x_pad))
        # minutes
        self.minutes_frame = tkinter.Frame(self.root)
        self.minutes_frame.pack(in_=self.package_status_frame, side=tkinter.TOP, fill=tkinter.BOTH, pady=y_pad_minor)
        self.minute_label = tkinter.Label(self.root, text="Min.", width=l_width, font=my_font)
        self.minute_label.pack(in_=self.minutes_frame, side=tkinter.LEFT, padx=(x_pad, 0))
        self.minute_entry = tkinter.Entry(self.root, width=e_width, font=my_font, justify='center',
                                          validate='key', vcmd=numbers_validate)
        self.minute_entry.pack(in_=self.minutes_frame, side=tkinter.LEFT, padx=(0, x_pad))
        # add time button
        self.add_time_button = self.HoverButton(master=self.root, text='Add Time To Check',
                                              command=lambda: self.run_time_input())
        self.add_time_button.pack(in_=self.package_status_frame, side=tkinter.BOTTOM, padx=x_pad, pady=y_pad)
        self.add_time_button.is_mac = self.is_mac

        # Create frame to contain the elements involved in adding an additional package
        self.package_add_frame = tkinter.Frame(self.root)
        self.package_add_frame.pack(in_=self.right_frame, padx=x_pad, pady=(y_pad + r_space_add, y_pad))
        self.package_add_frame.config(bd=2, relief=tkinter.RAISED)
        self.package_add_title = tkinter.Label(self.root, text="Add Additional Packages", font=title_font)
        self.package_add_title.pack(in_=self.package_add_frame, side=tkinter.TOP, padx=x_pad, pady=y_pad)
        # package_id
        self.id_frame = tkinter.Frame(self.root)
        self.id_frame.pack(in_=self.package_add_frame, fill=tkinter.BOTH, pady=y_pad_minor)
        self.id_label = tkinter.Label(self.root, text="ID", width=l_width, font=my_font)
        self.id_label.pack(in_=self.id_frame, side=tkinter.LEFT, padx=(x_pad, 0))
        self.id_entry = tkinter.Entry(self.root, width=e_width, font=my_font, justify='center')
        self.current_id = 41
        self.set_id(str(self.current_id))
        self.id_entry.configure(state='readonly')
        self.id_entry.pack(in_=self.id_frame, side=tkinter.LEFT, padx=(0, x_pad))
        # weight
        self.weight_frame = tkinter.Frame(self.root)
        self.weight_frame.pack(in_=self.package_add_frame, fill=tkinter.BOTH, pady=y_pad_minor)
        self.weight_label = tkinter.Label(self.root, text="Weight", width=l_width, font=my_font)
        self.weight_label.pack(in_=self.weight_frame, side=tkinter.LEFT, padx=(x_pad, 0))
        self.weight_entry = tkinter.Entry(self.root, width=e_width, font=my_font, justify='center',
                                          validate='key', vcmd=numbers_validate)
        self.weight_entry.pack(in_=self.weight_frame, side=tkinter.LEFT, padx=(0, x_pad))
        # address
        self.address_frame = tkinter.Frame(self.root)
        self.address_frame.pack(in_=self.package_add_frame, fill=tkinter.BOTH, pady=y_pad_minor)
        self.address_label = tkinter.Label(self.root, text="Address", width=l_width, font=my_font)
        self.address_label.pack(in_=self.address_frame, side=tkinter.LEFT, padx=(x_pad, 0))
        self.address_cb = Combobox(self.root, width=combo_width, font=cb_font, justify='center', state="readonly")
        self.address_cb['values'] = self.addresses
        self.address_cb.bind("<<ComboboxSelected>>", lambda _ : self.address_selected())
        self.address_cb.pack(in_=self.address_frame, side=tkinter.LEFT, padx=(0, x_pad))
        # deadline (I decided against letting the user add an extra package with a deadline)
        # any additional package with a deadline would likely make at least one of our packages late
        """
        self.deadline_hour_frame = tkinter.Frame(self.root)
        self.deadline_hour_frame.pack(in_=self.package_add_frame, fill=tkinter.BOTH)
        self.deadline_hour_label = tkinter.Label(self.root, text="Hour Req.", width=my_width, font=my_font)
        self.deadline_hour_label.pack(in_=self.deadline_hour_frame, side=tkinter.LEFT, padx=(x_pad, 0))
        self.deadline_hour_entry = tkinter.Entry(self.root, width=my_width, font=my_font, justify='center',
                                                 validate='key', vcmd=numbers_validate)
        self.deadline_hour_entry.pack(in_=self.deadline_hour_frame, side=tkinter.LEFT, padx=(0, x_pad))
        self.deadline_minute_frame = tkinter.Frame(self.root)
        self.deadline_minute_frame.pack(in_=self.package_add_frame, fill=tkinter.BOTH)
        self.deadline_minute_label = tkinter.Label(self.root, text="Min. Req.", width=my_width, font=my_font)
        self.deadline_minute_label.pack(in_=self.deadline_minute_frame, side=tkinter.LEFT, padx=(x_pad, 0))
        self.deadline_minute_entry = tkinter.Entry(self.root, width=my_width, font=my_font, justify='center',
                                                   validate='key', vcmd=numbers_validate)
        self.deadline_minute_entry.pack(in_=self.deadline_minute_frame, side=tkinter.LEFT, padx=(0, x_pad))
        """
        # city
        self.city_frame = tkinter.Frame(self.root)
        self.city_frame.pack(in_=self.package_add_frame, fill=tkinter.BOTH, pady=y_pad_minor)
        self.city_label = tkinter.Label(self.root, text="City", width=l_width, font=my_font)
        self.city_label.pack(in_=self.city_frame, side=tkinter.LEFT, padx=(x_pad, 0))
        self.city_entry = tkinter.Entry(self.root, width=e_width, font=my_font, justify='center', state="readonly")
        self.city_entry.pack(in_=self.city_frame, side=tkinter.LEFT, padx=(0, x_pad))
        # zip_code
        self.zip_frame = tkinter.Frame(self.root)
        self.zip_frame.pack(in_=self.package_add_frame, fill=tkinter.BOTH, pady=y_pad_minor)
        self.zip_label = tkinter.Label(self.root, text="Zip Code", width=l_width, font=my_font)
        self.zip_label.pack(in_=self.zip_frame, side=tkinter.LEFT, padx=(x_pad, 0))
        self.zip_entry = tkinter.Entry(self.root, width=e_width, font=my_font, justify='center', state="readonly")
        self.zip_entry.pack(in_=self.zip_frame, side=tkinter.LEFT, padx=(0, x_pad))
        # Button To Add Package
        self.add_package_button = self.HoverButton(master=self.root, text='Add Package To Delivery',
                                                   command=lambda: self.add_package())
        self.add_package_button.pack(in_=self.package_add_frame, side=tkinter.BOTTOM, padx=x_pad, pady=y_pad)
        self.add_package_button.is_mac = self.is_mac

        # Create frame to contain the elements involved in manipulating additional features
        self.options_frame = tkinter.Frame(self.root)
        self.options_frame.pack(in_=self.right_frame, padx=x_pad, pady=(y_pad + r_space_add, y_pad))
        self.options_frame.config(bd=2, relief=tkinter.RAISED)
        # title
        self.options_title = tkinter.Label(self.root, text="Animation Options", font=title_font)
        self.options_title.pack(in_=self.options_frame, side=tkinter.TOP, padx=x_pad_c, pady=y_pad)
        # disable animation checkbox
        self.animation_disabled = IntVar(value=0)
        self.animation_check = Checkbutton(self.root, variable=self.animation_disabled, onvalue=1, offvalue=0,
                                           text="Disable Animation")
        self.animation_check.pack(in_=self.options_frame, side=tkinter.TOP, padx=x_pad_c, pady=y_pad, anchor=W)
        # speed up animation checkbox
        self.animation_fast = IntVar(value=0)
        self.fast_check = Checkbutton(self.root, variable=self.animation_fast, onvalue=1, offvalue=0,
                                      text="Fast Animation Speed")
        self.fast_check.pack(in_=self.options_frame, side=tkinter.TOP, padx=x_pad_c, pady=y_pad, anchor=W)

        # clear previous truck route checkbox (defaulted to checked)
        self.animation_clear = IntVar(value=1)
        self.clear_check = Checkbutton(self.root, variable=self.animation_clear, onvalue=1, offvalue=0,
                                       text="Clear Previous Truck Route")
        self.clear_check.pack(in_=self.options_frame, side=tkinter.TOP, padx=x_pad_c, pady=y_pad, anchor=W)

        # Add button used for stepping through the program
        self.next_step_button = self.HoverButton(master=self.root, text='Begin Delivery Process',
                                                 command=lambda: self.run_next_step(), width=next_button_width)
        self.next_step_button.pack(in_=self.right_frame, padx=x_pad, pady=(y_pad + r_space_add + 2, 0))
        self.next_step_button.is_mac = self.is_mac

        # get the width required to fit the elements of the right frame
        self.right_frame.update()
        self.right_width = self.right_frame.winfo_width()

        # fix the width to the combined width of the left and right frames
        self.root.wm_geometry(str(self.map_width + self.right_width) + "x" + str(self.map_height))

        # set step number to zero (this will move us through our program as the user presses the next_step_button)
        self.step_number = 0

    # Time complexity: O(n^2)
    def run_next_step(self):
        """Runs the next step in the delivery process."""

        # lock in features that can't change once the delivery process begins
        self.add_time_button["state"] = "disabled"
        self.add_package_button["state"] = "disabled"
        self.animation_check["state"] = "disabled"
        self.fast_check["state"] = "disabled"
        self.clear_check["state"] = "disabled"

        # runs first delivery step (truck 1 - priority packages with deadlines)
        if self.step_number == 0:

            # relay check button variables
            if self.animation_disabled.get() == 1:
                self.delivery_process.disable_animation = True
            if self.animation_fast.get() == 1:
                self.delivery_process.fast_speed = True
            if self.animation_clear.get() == 0:
                self.delivery_process.clear_route = False

            # user feedback (prevent button from being double clicked)
            self.next_step_button["text"] = 'Truck 1 Delivering'
            self.next_step_button["state"] = "disabled"

            # tells delivery_process to run it's truck one delivery
            self.delivery_process.deliver_truck_one()

            # user feedback (enable button click)
            self.next_step_button["state"] = "normal"
            self.next_step_button["text"] = 'Send Truck 2'

        # runs second delivery step (truck 2 - all remaining packages)
        elif self.step_number == 1:

            # user feedback (prevent button from being double clicked)
            self.next_step_button["text"] = 'Truck 2 Delivering'
            self.next_step_button["state"] = "disabled"

            # tells delivery_process to run it's truck two delivery
            self.delivery_process.deliver_truck_two()

            # user feedback (enable button click)
            self.next_step_button["state"] = "normal"
            self.next_step_button["text"] = 'Print Final Results'

        # prints out final package information
        elif self.step_number == 2:
            self.next_step_button["text"] = 'Exit Program'
            self.delivery_process.print_out_results()

        # exits program
        else:
            self.root.destroy()

        # increments the step to move the delivery process forward
        self.step_number += 1

    # Time complexity: O(1)
    def run_time_input(self):
        """If the time inputs are valid, add a time to check the status of packages to the delivery_process"""

        # validate hours
        hour = self.hour_entry.get()
        valid_input = self.validate_hour(hour)

        # validate minutes
        minute = self.minute_entry.get()
        valid_input = self.validate_minute(minute, valid_input)

        # add the time to delivery_process
        if valid_input:
            add_am_pm = 'AM'
            if int(hour) > 12:
                add_am_pm = 'PM'
            time_to_add = self.hour_entry.get() + ":" + self.minute_entry.get() + " " + add_am_pm
            time_to_check = datetime.strptime(time_to_add, '%H:%M %p').time()
            self.delivery_process.add_status_time(time_to_check)
            print("Status Time Added - Hour: %s, Minute %s" % (self.hour_entry.get(), self.minute_entry.get()))

    # Time complexity: O(1)
    def add_package(self):
        """If package inputs are valid, add the package to the delivery_process."""

        # get package id from entry
        package_id = int(self.id_entry.get())

        # validate address
        is_valid = True
        address = self.address_cb.get()
        if address == "":
            print("address invalid")
            is_valid = False

        # create deadline at EOD
        deadline = datetime.strptime('23:59 PM', '%H:%M %p').time()

        # get city and zip code
        city = self.city_entry.get()
        zip_code = self.zip_entry.get()

        # validate weight
        weight = self.weight_entry.get()
        if address == "":
            print("weight invalid")
            is_valid = False

        # if valid, add package to delivery process
        if is_valid:
            self.delivery_process.add_additional_package(package_id, address, deadline, city, zip_code, weight)
            print("package added")
            self.set_id(self.current_id)

    # Time complexity: N/A - infinite loop
    def show(self):
        """Loops continuously, allowing the user interaction to dictate the flow of the application."""
        self.root.mainloop()

    # Time complexity: O(1)
    def validate_hour(self, hour):
        """Validates that inputted hour is appropriate (should be between 0-23)."""
        if hour == "" or int(hour) > 24:
            print("invalid hour input")
            return False
        return True

    # Time complexity: O(1)
    def validate_minute(self, minute, current_bool):
        """Validates that inputted minutes is appropriate (should be between 0-59)."""
        if minute == "" or int(minute) > 60:
            print("invalid minute input")
            return False
        elif not current_bool:
            return False
        return True

    # Time complexity: O(1)
    def validate_numeric(self, entry_input):
        """Ensures that an entry input is a number."""
        if entry_input in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return True
        return False

    # Time complexity: O(1)
    def set_id(self, text):
        """Populates id entry"""
        self.id_entry.configure(state='normal')
        self.id_entry.delete(0, tkinter.END)
        self.id_entry.insert(0, text)
        self.current_id += 1
        self.id_entry.configure(state='readonly')
        return

    # Time complexity: O(1)
    def set_zip(self, text):
        """Populates zip code entry."""
        self.zip_entry.configure(state='normal')
        self.zip_entry.delete(0, tkinter.END)
        self.zip_entry.insert(0, text)
        self.zip_entry.configure(state='readonly')
        return

    # Time complexity: O(1)
    def set_city(self, text):
        """Populates city entry."""
        self.city_entry.configure(state='normal')
        self.city_entry.delete(0, tkinter.END)
        self.city_entry.insert(0, text)
        self.city_entry.configure(state='readonly')
        return

    # Time complexity: O(1)
    def address_selected(self):
        """Populates city and zip code entries based on address selected."""
        address = self.address_cb.get()
        i = 0
        while i < len(self.locations):
            if address == self.locations[i].address:
                self.set_zip(self.locations[i].zip_code)
                self.set_city(self.locations[i].city)
            i += 1

    class HoverButton(tkinter.Button):
        """Inherits from button, adds hover background color change."""

        # Time complexity: O(1)
        def __init__(self, master, **kw):
            """Sets default background and binds <Enter> and <Leave> events."""
            tkinter.Button.__init__(self, master=master, **kw)
            self.defaultBackground = self["background"]
            self.bind("<Enter>", self.on_enter)
            self.bind("<Leave>", self.on_leave)
            self.is_mac = False

        # Time complexity: O(1)
        def on_enter(self, e):
            """Changes background on <Enter>"""
            if not self.is_mac:
                self['background'] = '#DDDDDD'

        # Time complexity: O(1)
        def on_leave(self, e):
            """Reverts to default background on <Leave>"""
            if not self.is_mac:
                self['background'] = self.defaultBackground
