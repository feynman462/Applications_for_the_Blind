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

# Other existing functions...

def get_measurement_unit():
    speak("Please choose your unit of measurement: inches or centimeters.")
    unit = input("Enter 'inches' or 'cm': ").lower()
    return unit

def get_object_type():
    speak("Please choose the type of object you want to calculate.")
    object_type = input("Enter the object type: ").lower()
    return object_type

# Updated main function
def main():
    speak("Welcome to the Object Volume Calculator!")
    
    # Get the shape of the jar from the user
    speak("Please enter the shape of your jar. You can choose sphere, cylinder, or cuboid.")
    container_shape = input("Enter the shape of your jar: ").lower()
    
    # Get measurement unit
    unit = get_measurement_unit()
    
    # Get the object type
    object_type = get_object_type()

    # Get dimensions for the container
    speak(f"Please enter the dimensions for the {container_shape} in {unit}.")
    container_dimensions = get_dimensions_for_shape(container_shape)
    
    # Convert dimensions if necessary
    if unit == "inches":
        # Convert inches to cm if needed (1 inch = 2.54 cm)
        container_dimensions = {k: v*2.54 for k, v in container_dimensions.items()}
    
    # Calculate volume and number of objects
    container_volume = volume_of_object(container_shape, container_dimensions)
    object_volume = volume_of_object(object_type, container_dimensions)  # Assuming same dimensions for simplicity
    packing_efficiency = packing_efficiencies.get(object_type, 0.74)
    num_objects = calculate_number_of_objects(container_volume, object_volume, packing_efficiency)
    
    # Present results
    result_message = f"The estimated number of {object_type}s that can fit in the {container_shape} is: {num_objects}"
    print(result_message)
    speak(result_message)
    
    # Offer to copy result to clipboard
    if input("Would you like to copy the result to the clipboard? (yes/no): ").lower() == 'yes':
        pyperclip.copy(str(num_objects))
        speak("The result has been copied to the clipboard.")
    
    # Check if the user wants to calculate another jar
    if input("Would you like to calculate another jar? (yes/no): ").lower() == 'yes':
        main()
    else:
        speak("Thank you for using the Object Volume Calculator. Goodbye!")
        exit()

if __name__ == "__main__":
    main()
