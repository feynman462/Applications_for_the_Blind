import pytz
import pyttsx3
from datetime import datetime
from geopy.geocoders import OpenCage
from skyfield.api import Topos, load
from geopy.exc import GeocoderTimedOut

api_key = 'your_opencage_api_key'
geocoder = OpenCage(api_key)

def get_location(location_str):
    observer_location = geocoder.geocode(location_str)
    observer_tz = pytz.timezone(observer_location.raw['annotations']['timezone']['name'])
    latitude = observer_location.latitude
    longitude = observer_location.longitude
    observer_location_str = observer_location.address
    return observer_tz, latitude, longitude, observer_location_str

observer_tz, latitude, longitude, observer_location_str = get_location("Your location")

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def planet_info():
    now_utc = datetime.now(pytz.utc)
    now_local = now_utc.astimezone(observer_tz)

    planets = load('de421.bsp')
    observer = Topos(latitude, longitude)

    ts = load.timescale()
    t = ts.utc(now_utc.year, now_utc.month, now_utc.day, now_utc.hour, now_utc.minute, now_utc.second)

    for planet_name in ['sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']:
        planet = planets[planet_name]
        astrometric = observer.at(t).observe(planet)
        alt, az, distance = astrometric.apparent().altaz()

        info = f"{planet_name.capitalize()}: " \
               f"Altitude: {alt.degrees:.2f}°, " \
               f"Azimuth: {az.degrees:.2f}°, " \
               f"Distance: {distance.au:.2f} AU"

        print(info)
        speak(info)
        print()

if __name__ == "__main__":
    try:
        planet_info()
    except GeocoderTimedOut:
        print("Error: Geocoder timed out. Please try again.")
        speak("Error: Geocoder timed out. Please try again.")
    except Exception as e:
        print(f"Error: {e}")
        speak(f"Error: {e}")
