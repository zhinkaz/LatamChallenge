# get the location of the cities
def get_location(city: list):
    
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