class MapLocation:
    """Connects a location on the canvas representing a destination location to a unique identifier"""

    # Time Complexity: O(1)
    def __init__(self, location_id, x=0, y=0):
        """ constructor adds the desired location id and coordinates to the object

        :param location_id: unique identifier for destination location
        :param x: x coordinate on map image in pixels
        :param y: y coordinate on map image in pixels
        """
        self.location_id = location_id
        self.x = x
        self.y = y
