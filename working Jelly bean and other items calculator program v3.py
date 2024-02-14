import math
import pyttsx3
from word2number import w2n
import pyperclip
from fuzzywuzzy import process

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Maps various input variants to the canonical object names
OBJECT_VARIANTS = {
    'sphere': ['sphere', 'ball', 'spherical'],
    'cylinder': ['cylinder', 'cylindrical'],
    'cuboid': ['cuboid', 'cube', 'box', 'rectangular prism'],
    # Add new shapes here as necessary
}

# Volume calculation functions
def volume_of_sphere(radius):
    return (4/3) * math.pi * (radius ** 3)

def volume_of_cylinder(radius, height):
    return math.pi * (radius ** 2) * height

def volume_of_cuboid(length, width, height):
    return length * width * height

def volume_of_object(shape, dimensions):
    if shape == 'sphere':
        return volume_of_sphere(dimensions['radius'])
    elif shape == 'cylinder':
        return volume_of_cylinder(dimensions['radius'], dimensions['height'])
    elif shape == 'cuboid':
        return volume_of_cuboid(dimensions['length'], dimensions['width'], dimensions['height'])
    else:
        speak("Unsupported shape provided.")
        return None

# Function to get dimensions based on shape
def get_dimensions_for_shape(shape):
    dimensions = {}
    if shape == 'sphere':
        dimensions['radius'] = float(input("Enter the radius of the sphere in cm: "))
    elif shape == 'cylinder':
        dimensions['radius'] = float(input("Enter the radius of the cylinder in cm: "))
        dimensions['height'] = float(input("Enter the height of the cylinder in cm: "))
    elif shape == 'cuboid':
        dimensions['length'] = float(input("Enter the length of the cuboid in cm: "))
        dimensions['width'] = float(input("Enter the width of the cuboid in cm: "))
        dimensions['height'] = float(input("Enter the height of the cuboid in cm: "))
    else:
        speak("Shape not recognized. Please enter a valid shape.")
    return dimensions

# Function to calculate the number of objects
def calculate_number_of_objects(container_volume, object_volume, packing_efficiency):
    return int(container_volume * packing_efficiency / object_volume)

# Packing efficiencies
packing_efficiencies = {
    'sphere': 0.74,
    'cylinder': 0.82,
    'cuboid': 1.0
    # Add more shapes and their efficiencies as necessary
}

# The main function with updates
def main():
    speak("Welcome to the Object Volume Calculator!")

    container_shape = 'cuboid'  # Default container shape
    speak(f"Please enter the dimensions for the {container_shape}.")
    container_dimensions = get_dimensions_for_shape(container_shape)
    container_volume = volume_of_object(container_shape, container_dimensions)

    speak("What is the shape of the objects you are calculating for?")
    object_shape = input("Enter the shape of the objects: ").lower()
    object_dimensions = get_dimensions_for_shape(object_shape)
    object_volume = volume_of_object(object_shape, object_dimensions)

    packing_efficiency = packing_efficiencies.get(object_shape, 0.74)  # Default to sphere if not found
    num_objects = calculate_number_of_objects(container_volume, object_volume, packing_efficiency)

    speak(f"The estimated number of {object_shape} in the container is: {num_objects}")
    if input("Would you like to copy the result to the clipboard? (yes/no): ").lower() == 'yes':
        pyperclip.copy(str(num_objects))
        speak("The result has been copied to the clipboard.")

    if input("Would you like to calculate again? (yes/no): ").lower() == 'yes':
        main()

if __name__ == "__main__":
    main()
