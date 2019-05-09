from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim()
location = geolocator.geocode("Cairo Egypt")
# print((location.latitude, location.longitude))
location2 = geolocator.geocode("Monufia ,Egypt ")
d = (location2.latitude, location2.longitude)
d2 = (location.latitude, location.longitude)
# print((location2.latitude, location2.longitude))
# print(geodesic(d, d2).km)


def getDistance(location1, location3):
    location = geolocator.geocode(location1)
    location2 = geolocator.geocode(location3)
    d = (location2.latitude, location2.longitude)
    d2 = (location.latitude, location.longitude)
    return abs(geodesic(d, d2).km)


print(getDistance("Cairo Egypt", "Monufia ,Egypt "))
