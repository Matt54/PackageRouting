class PackagesHashTable:
    """Hash Table storing all the packages to be delivered"""

    # Time Complexity O(1), Space Complexity O(n)
    def __init__(self, number_of_buckets=50):
        """Contructor sets default values for our hash table buckets

        :param number_of_buckets: number of buckets the hash table should have
        """
        self.EMPTY_SINCE_START = EmptyBucket()
        self.EMPTY_AFTER_REMOVAL = EmptyBucket()
        self.number_of_buckets = number_of_buckets
        self.hash_table = [self.EMPTY_SINCE_START] * self.number_of_buckets

    # Time Complexity: O(1)
    def hash_function(self, key):
        """Hash function for table

        :param key: package id
        :return: bucket index
        """
        return key % self.number_of_buckets

    # Time Complexity O(1)
    def add(self, package_id, address, deadline, city, zip_code, weight, status):
        """ Adds a new package

        :param package_id: unique identifier for package
        :param address: street address
        :param deadline: delivery deadline
        :param city: city
        :param zip_code: zip code
        :param weight: weight of package in kg
        :param status: DeliveryStatus for package
        :return: none
        """

        # get bucket from hash function of package id
        bucket = self.hash_function(package_id)

        # put information into the hash table at the bucket location
        self.hash_table[bucket] = [package_id, address, deadline, city, zip_code, weight, status]

    # Time Complexity O(n)
    def delete(self, package_id):
        """Deletes a package, given the package_id.

        :param package_id:
        :return: True if successfully deleted. False if not found.
        """

        # try to find the bucket where a package id is
        bucket = self.search_for_bucket(package_id)

        # if we found a package, make it empty
        if bucket != -1:
            self.hashTable[bucket] = self.EMPTY_AFTER_REMOVAL
            return True
        else:
            return False

    # Time Complexity O(n)
    def update_package_status(self, package_id, status):
        """ Updates the status of a package, given the id and new status

        :param package_id: unique identifier for package that we are going to update
        :param status: status we are updating pacakge to
        :return: none
        """
        package_list = self.get_package(package_id)
        package_list[6] = status

    # Time Complexity O(n)
    def search_for_bucket(self, key):
        """ Uses linear search to find and return the bucket location for a given package_id

        :param key:
        :return: bucket id
        """

        # get the bucket number from the hash function
        bucket = self.hash_function(key)
        num_probed = 0

        # Keep searching until you find a bucket that is not empty or you search all buckets
        while self.hash_table[bucket] is not self.EMPTY_SINCE_START and num_probed < self.number_of_buckets:
            if self.hash_table[bucket][0] == key:
                return bucket
            bucket = self.hash_function(bucket + 1)
            num_probed = num_probed + 1
        return -1

    # Time Complexity O(n)
    def get_package(self, package_id):
        """ Uses linear search to find and return the list at the bucket location for a package_id

        :param package_id: unique identifier of package we are searching for
        :return: list stored in bucket
        """

        # get the bucket number from the hash function
        bucket = self.hash_function(package_id)

        # Keep searching until you find a bucket that is not empty or you search all buckets
        num_probed = 0
        while self.hash_table[bucket] is not self.EMPTY_SINCE_START and num_probed < self.number_of_buckets:
            if self.hash_table[bucket][0] == package_id:
                return self.hash_table[bucket]
            bucket = self.hash_function(bucket + 1)
            num_probed += 1
        return None

    # Time Complexity: O(n)
    def print_all_packages(self):
        """ Prints the status of all the packages in the hash table

        :return: none
        """

        # loop through all the buckets
        i = 1
        while i < len(self.hash_table) + 1:
            p = self.get_package(i)

            # if there is information in the bucket, print it
            if p:
                print('Package id: %s, Address: %s, Deadline: %s, City: %s, Zip Code: %s, Weight: %s kg, Status: %s'
                      % (p[0], p[1], p[2].strftime('%H:%M %p'), p[3], p[4], p[5], p[6].value))
            i += 1


class EmptyBucket:
    """Indicates that the bucket is unused"""
    pass
