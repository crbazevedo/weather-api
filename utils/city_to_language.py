from geopy.geocoders import Nominatim

def city_to_language_code(city):
    geolocator = Nominatim(user_agent="WeatherAIReport/0.1") 
    location = geolocator.geocode(city, exactly_one=True, language='en')
    
    if location is not None:
        return location.raw['display_name'].split(",")[-1].strip()

    return None
