# get the location of the cities
from typing import List


def get_location(city: List[str])->List[str]:
    """_summary_

    Args:
        city (list): _description_

    Returns:
        _type_: _description_
    """    
    geolocator = Nominatim(user_agent='myapp')
    loc_nationals = city
    region = []
    for city in loc_nationals:
        location = geolocator.geocode(city)
        if location:
            country = location.raw["display_name"].split(',')[2]
            region.append(country)
        else:
            region.append('Not Found')
    return region

def get_location_comprehesion(cities: List[str]) -> List[str]:
    geolocator = Nominatim(user_agent="myapp")
    return [
        geolocator.geocode(city).raw["display_name"].split(",")[2]
        if geolocator.geocode(city)
        else "Not Found"
        for city in cities
        ]