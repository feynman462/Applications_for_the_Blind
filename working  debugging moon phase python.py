import pytz
import winsound
from datetime import datetime
from geopy.geocoders import OpenCage
from skyfield.api import Topos, load, utc
from geopy.exc import GeocoderTimedOut

api_key = '61a2c4f033ab4216933d85bc631d2325'
geocoder = OpenCage(api_key)

# Prompt user for location
while True:
    location_str = input("Please enter your city, state, and country (e.g. London, England, UK): ")
    try:
        observer_location = geocoder.geocode(location_str)
        observer_tz = pytz.timezone(observer_location.raw['annotations']['timezone']['name'])
        latitude = observer_location.latitude
        longitude = observer_location.longitude
        observer_location_str = observer_location.address
        break
    except GeocoderTimedOut:
        print("Geocoder service timed out. Please try again.")
    except Exception as e:
        print(f"Could not find location information for the given location. Please try again. Error: {e}")

def speak_moon_phase(phase_name, phase_pct):
    if phase_name == "Full Moon":
        frequency = 1000
        duration = 500
    elif phase_name == "New Moon":
        frequency = 200
        duration = 500
    else:
        frequency = 500
        duration = 500

    winsound.Beep(frequency, duration)

def moon_info():
    try:
        now_utc = datetime.now(utc)
        now_local = now_utc.astimezone(observer_tz)

        planets = load('de421.bsp')
        earth = planets['earth']
        moon = planets['moon']
        observer = earth + Topos(latitude, longitude)

        ts = load.timescale()
        t = ts.utc(now_utc.year, now_utc.month, now_utc.day, now_utc.hour, now_utc.minute, now_utc.second)
        astrometric = observer.at(t).observe(moon).apparent()
        ra, dec, distance_to_moon = astrometric.radec()

        sun = planets['sun']
        elongation = earth.at(t).observe(sun).apparent().separation_from(astrometric)
        phase_pct = (180 - elongation.degrees) / 180 * 100
        if 0 <= phase_pct < 1:
            phase_name = "New Moon"
        elif 1 <= phase_pct < 50:
            phase_name = "Waxing Crescent"
        elif 50 == phase_pct:
            phase_name = "First Quarter"
        elif 50 < phase_pct < 99:
            phase_name = "Waxing Gibbous"
        elif phase_pct == 99:
            phase_name = "Full Moon"
        elif 100 >= phase_pct > 50:
            phase_name = "Waning Gibbous"
        elif phase_pct == 50:
            phase_name = "Last Quarter"
        else:
            phase_name = "Waning Crescent"

        distance_to_sun = earth.at(t).observe(sun).apparent().distance().au

        output_str = "The current moon phase is {phase}, which is {percent:.0f}% illuminated. "\

        "Observer location: {location}. Local time: {time}. Distance to the moon: {moon_distance:.2f} au. "\
            "Distance to the sun: {sun_distance:.2f} au.".format(phase=phase_name, percent=phase_pct,
                                                                 location=observer_location_str, time=now_local,
                                                                 moon_distance=distance_to_moon.au,
                                                                 sun_distance=distance_to_sun)
        print(output_str)

    except Exception as e:
        print(f"An error occurred while fetching moon information: {e}")

moon_info()
