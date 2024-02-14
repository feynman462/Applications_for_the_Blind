import tkinter as tk
from tkinter import ttk
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def get_gravitational_force(m1, m2, r):
    G = 6.67430 * (10 ** -11)  # Gravitational constant (m^3 kg^-1 s^-2)
    force = (G * m1 * m2) / (r ** 2)
    return force

def calculate_perturbation():
    m1 = planets[planet_var.get()]['mass']
    m2 = moons[moon_var.get()]['mass']
    r = float(distance_var.get())

    force = get_gravitational_force(m1, m2, r)
    result_text = f"Gravitational force: {force:.2e} Newtons"
    result_label.config(text=result_text)
    
    # Speak the result
    engine.say(result_text)
    engine.runAndWait()

# Separate celestial bodies into planets and moons
planets = {
    'Earth': {'mass': 5.972 * 10**24},
    'Mars': {'mass': 6.417 * 10**23},
    # Add more planets as needed
}

moons = {
    'Moon': {'mass': 7.342 * 10**22},
    'Phobos': {'mass': 1.065 * 10**16},
    'Deimos': {'mass': 1.476 * 10**15},
    # Add more moons as needed
}

app = tk.Tk()
app.title("Gravitational Perturbation Calculator")

# Create dropdown menus for planet and moon selection
planet_var = tk.StringVar()
moon_var = tk.StringVar()

planet_dropdown = ttk.Combobox(app, textvariable=planet_var)
planet_dropdown['values'] = list(planets.keys())
planet_dropdown.current(0)
planet_dropdown.grid(column=0, row=0)

moon_dropdown = ttk.Combobox(app, textvariable=moon_var)
moon_dropdown['values'] = list(moons.keys())
moon_dropdown.current(0)
moon_dropdown.grid(column=1, row=0)

# Create input field for distance
distance_var = tk.StringVar()
distance_entry = tk.Entry(app, textvariable=distance_var)
distance_entry.insert(0, "384400000")  # Default distance Earth-Moon in meters
distance_entry.grid(column=2, row=0)

# Create calculate button
calculate_button = tk.Button(app, text="Calculate", command=calculate_perturbation)
calculate_button.grid(column=3, row=0)

# Create label to display result
result_label = tk.Label(app, text="")
result_label.grid(column=0, row=1, columnspan=4)

app.mainloop()
bodies = [
    ('Sun', planets['sun'], 1.989 * 10 ** 30),
    ('Mercury', planets['mercury'], 3.301 * 10 ** 23),
    ('Venus', planets['venus'], 4.867 * 10 ** 24),
    ('Earth', planets['earth'], 5.972 * 10 ** 24),
    ('Moon', planets['moon'], 7.342 * 10 ** 22),
    ('Mars', planets['mars'], 6.417 * 10 ** 23),
    ('Phobos', planets['mars barycenter'] + 2, 1.065 * 10 ** 16),
    ('Deimos', planets['mars barycenter'] + 1, 1.476 * 10 ** 15),
    ('Jupiter', planets['jupiter'], 1.899 * 10 ** 27),
    ('Io', planets['jupiter barycenter'] + 5, 8.931 * 10 ** 22),
    ('Europa', planets['jupiter barycenter'] + 4, 4.8 * 10 ** 22),
    ('Ganymede', planets['jupiter barycenter'] + 3, 1.482 * 10 ** 23),
    ('Callisto', planets['jupiter barycenter'] + 2, 1.076 * 10 ** 23),
    ('Saturn', planets['saturn'], 5.685 * 10 ** 26),
    ('Titan', planets['saturn barycenter'] + 6, 1.345 * 10 ** 23),
    ('Uranus', planets['uranus'], 8.682 * 10 ** 25),
    ('Titania', planets['uranus barycenter'] + 3, 3.5 * 10 ** 21),
    ('Oberon', planets['uranus barycenter'] + 4, 3.014 * 10 ** 21),
    ('Neptune', planets['neptune'], 1.024 * 10 ** 26),
    ('Triton', planets['neptune barycenter'] + 1, 2.14 * 10 ** 22),
    # Add more celestial bodies as needed, following the format ('Name', planets['planet_key'], mass)
]

observer_location = Topos(latitude_degrees=40.7128, longitude_degrees=-74.0060)  # Example: New York City

# Example usage:
calculate_perturbations()
