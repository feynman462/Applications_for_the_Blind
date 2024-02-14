import pytz
import pyttsx3
import tkinter as tk
import threading
from datetime import datetime
from geopy.geocoders import OpenCage
from skyfield.api import Topos, load
from geopy.exc import GeocoderTimedOut
from tkinter import simpledialog
from tkinter import messagebox

api_key = '61a2c4f033ab4216933d85bc631d2325'
geocoder = OpenCage(api_key)

def get_location(location_str):
    observer_location = geocoder.geocode(location_str)
    observer_tz = pytz.timezone(observer_location.raw['annotations']['timezone']['name'])
    latitude = observer_location.latitude
    longitude = observer_location.longitude
    observer_location_str = observer_location.address
    return observer_tz, latitude, longitude, observer_location_str

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def submit_location(user_location):
    observer_tz, latitude, longitude, observer_location_str = get_location(user_location)
    threading.Thread(target=planet_info, args=(latitude, longitude, observer_tz)).start()

def planet_info(latitude, longitude, observer_tz):
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

root = tk.Tk()
root.withdraw()

user_location = simpledialog.askstring("Planet Locator", "Enter your location:", parent=root)
if user_location:
    submit_location(user_location)
else:
    messagebox.showerror("Error", "Please enter a valid location.")
