import json
import os
import time
import schedule
from datetime import datetime, timedelta

data_file = "plant_data.json"

# Load plant data or create an empty list if the file doesn't exist
if os.path.exists(data_file):
    with open(data_file, "r") as f:
        plant_data = json.load(f)
else:
    plant_data = []

# Plant health information library
plant_health_info = {
    "Aloe Vera": "Aloe Vera plants require indirect sunlight, well-draining soil, and infrequent watering.",
    "Spider Plant": "Spider plants need bright, indirect sunlight and well-draining soil. Water moderately.",
    "Snake Plant": "Snake plants prefer indirect sunlight and can tolerate low light. Allow soil to dry between waterings.",
    "Peace Lily": "Peace Lilies prefer low to medium light and moist soil. Be cautious not to overwater.",
    "Cannabis Sativa": "Cannabis Sativa plants require plenty of sunlight, well-draining soil, and a moderate climate. Water regularly, but be cautious not to overwater.",
    "Cannabis Indica": "Cannabis Indica plants need ample light, well-draining soil, and consistent temperatures. Maintain a regular watering schedule, avoiding overwatering or underwatering.",
    # Add more plant species and their health information here
}

def save_data():
    with open(data_file, "w") as f:
        json.dump(plant_data, f)

def add_plant():
    name = input("Enter the plant name: ")
    species = input("Enter the plant species: ")
    days_between_feeding = int(input("Enter the number of days between feedings: "))
    last_fed = datetime.now()

    plant = {
        "name": name,
        "species": species,
        "days_between_feeding": days_between_feeding,
        "last_fed": last_fed.strftime("%Y-%m-%d")
    }

    plant_data.append(plant)
    save_data()
    print(f"{name} has been added to the schedule.")
    
    if species in plant_health_info:
        print(f"\nHealth Information for {species}:")
        print(plant_health_info[species])
    else:
        print(f"No specific health information available for {species}.")
        # You could also prompt the user to enter health information for a new species here, and then save it in the plant_health_info dictionary

def view_plants():
    print("\nList of plants:")
    for plant in plant_data:
        print(f"{plant['name']} ({plant['species']}): last fed on {plant['last_fed']}, feed every {plant['days_between_feeding']} days")

def feed_plant(plant):
    print(f"\nIt's time to feed {plant['name']}!")
    plant["last_fed"] = datetime.now().strftime("%Y-%m-%d")
    save_data()

def schedule_feedings():
    for plant in plant_data:
        last_fed = datetime.strptime(plant["last_fed"], "%Y-%m-%d")
        days_between_feeding = plant["days_between_feeding"]
        next_feed = last_fed + timedelta(days=days_between_feeding)

        while next_feed <= datetime.now():
            next_feed += timedelta(days=days_between_feeding)

        schedule.every(days_between_feeding).days.at("10:00").do(feed_plant, plant=plant)

        print(f"{plant['name']} will be reminded to be
