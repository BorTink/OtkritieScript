from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic


class Geocodes:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="Geopy Library")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1.1)

    def get_coords_from_address(self, address):
        coords = self.geocode(address)
        if coords:
            return coords.latitude, coords.longitude
        else:
            return None, None

    @staticmethod
    def get_distance(coords_1, coords_2):
        distance = geodesic(coords_1, coords_2).m
        return distance  # в метрах

