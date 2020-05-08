# imports required for script
from enum import Enum


class DeliveryStatus(Enum):
    """Enum that stores the possible states of a package"""
    AT_HUB = 'At Hub'
    IN_ROUTE = "In Route"
    DELIVERED = "Delivered"
