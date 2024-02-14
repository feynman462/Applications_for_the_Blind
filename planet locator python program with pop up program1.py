import pytz
import pyttsx3
import tkinter as tk
import threading
from datetime import datetime
from geopy.geocoders import OpenCage
from skyfield.api import Topos, load
from geopy.exc import GeocoderTimedOut
from tkinter import Entry, Toplevel
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

def on_entry_click(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.config(fg="black")

def submit_and_close(dialog, city, state, country):
    user_location = f"{city.get()}, {state.get()}, {country.get()}"
    submit_location(user_location)
    dialog.destroy()

def location_dialog():
    dialog = Toplevel(root)
    dialog.title("Planet Locator")
    dialog.geometry("300x150")

    city = Entry(dialog, width=30)
    city.insert(0, "City")
    city.bind('<FocusIn>', lambda event: on_entry_click(event, city, "City"))
    city.config(fg="gray")
    city.pack(pady=5)

    state = Entry(dialog, width=30)
    state.insert(0, "State")
    state.bind('<FocusIn>', lambda event: on_entry_click(event, state, "State"))
    state.config(fg="gray")
    state.pack(pady=5)

    country = Entry(dialog, width=30)
    country.insert(0, "Country")
    country.bind('<FocusIn>', lambda event: on_entry_click(event, country, "Country"))
    country.config(fg="gray")
    country.pack(pady=5)
    
    submit_button = tk.Button(dialog, text="Submit", command=lambda: submit_and_close(dialog, city, state, country))
    submit_button.pack(pady=5)

root = tk.Tk()
root.withdraw()

speak("Welcome to Sun Locator")
location_dialog()

root.mainloop()
