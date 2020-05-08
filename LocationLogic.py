# Time Complexity: O(n)
def get_location_id_from_address(locations, address, city, zip_code):
    """gets the location a package is heading to from the street, city, and zip code

    :param locations:  list of all locations
    :param address: street address package is heading to
    :param city: city package is heading to
    :param zip_code: zip code package is heading to
    :return: location package is heading to
    """

    for location in locations:
        if location.is_equal(address, city, 'UT', zip_code):
            return location.location_id


# Time Complexity: O(n)
def get_location_id_from_package_id(locations, hash_table, package_id):
    """ determines the location id from the package id

    :param locations: list of all locations
    :param hash_table: hash table for packages
    :param package_id: package id we are looking for
    :return: none
    """

    # get package bucket from hash table
    package = hash_table.get_package(package_id)

    # return location id after searching for it through
    return get_location_id_from_address(locations, package[1], package[3], package[4])
