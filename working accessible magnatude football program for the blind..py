import pyttsx3
import speech_recognition as sr
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Define player roles and their respective number
roles = {'Quarterback': 1, 'Running Back': 1, 'Wide Receiver': 2, 'Center': 1, 'Guard': 2, 'Tackle': 2}
role_averages = {'Quarterback': 0, 'Running Back': 1, 'Wide Receiver': 10, 'Center': -1, 'Guard': -2, 'Tackle': -3}

# Define end zones and field size
END_ZONES = 10
FIELD_LENGTH = 100
FIELD_WIDTH = 53

def speak(text, audio_prompt):
    if audio_prompt:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat, please?", True)
            return listen()
        except sr.RequestError:
            speak("Sorry, the speech recognition service failed. Please, try again later.", True)
        except sr.WaitTimeoutError:
            speak("No input detected. Please, try again.", True)

def prompt_input(prompt, input_method, audio_prompt):
    speak(prompt, audio_prompt)
    if input_method == 'speech':
        return listen()
    else:
        return input(prompt)

def enter_coordinate(input_method, coordinate, side, role, audio_prompt):
    while True:
        average_location = role_averages[role]
        prompt = f"Enter the {coordinate} coordinate for the {side} player {role}. The average X-coordinate for this role is usually around {average_location}. Note that for the X coordinate, the left end zone starts at -10, the right end zone ends at 110, and the field ranges from 0 to 100. For the Y coordinate, the bottom sideline starts at 0, and the top sideline ends at 53: "
        coord = prompt_input(prompt, input_method, audio_prompt)
        try:
            coord = float(coord)
        except ValueError:
            speak("Please, enter a valid number.", audio_prompt)
            continue
        return coord

def enter_player_locations(input_method, side, audio_prompt):
    locations = {}
    for role, count in roles.items():
        for i in range(count):
            while True:
                speak(f"Now placing: {side} {role}", audio_prompt)
                x = enter_coordinate(input_method, 'X', side, role, audio_prompt)
                y = enter_coordinate(input_method, 'Y', side, role, audio_prompt)
                if role == "Quarterback":
                    y = locations["Center"][1] - 1  # QB's Y-coordinate is 1 less than the C's
                if -END_ZONES <= x <= FIELD_LENGTH + END_ZONES and 0 <= y <= FIELD_WIDTH:
                    locations[role] = (x, y)
                    break
                else:
                    speak(f"X coordinate must be between {-END_ZONES} and {FIELD_LENGTH + END_ZONES}, and Y coordinate must be between 0 and {FIELD_WIDTH}.", audio_prompt)
    return locations

def main():
    audio_prompt = input("Would you like to hear audio prompts? (yes/no) ").lower() == 'yes'
    input_method = input("Would you like to provide input by speech or by typing? (speech/type) ").lower()
    
    enter_player_locations(input_method, 'offense', audio_prompt)

# In the `main` function call
if __name__ == "__main__":
    main()
