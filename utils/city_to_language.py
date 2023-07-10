from geopy.geocoders import Nominatim
from babel import Locale

def get_language_localization(city):
    geolocator = Nominatim(user_agent="WeatherAIReport/0.1")
    location = geolocator.geocode(city, exactly_one=True, addressdetails=True)

    if location is not None:
        country_code = location.raw['address']['country_code']
        print(f"country_code: {country_code}")
        if country_code is not None:
            try:
                locale = Locale.parse('und_' + country_code, sep='_')
                print(f"locale: {locale}")
                if locale is not None:
                    # replace separator '_' for '-' to match BING_NEWS_SEARCH_API_KEY
                    locale = str(locale).replace('_', '-')
                    return locale 
            except (ValueError, KeyError):
                pass

    return None

