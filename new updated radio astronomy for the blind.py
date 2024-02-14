import pyttsx3
import speech_recognition as sr
from astroquery.vizier import Vizier

# Initialize pyttsx3
engine = pyttsx3.init()

# Initialize a list to record all search results
search_results = []

# Function to generate a verbal description
def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_input_method():
    while True:
        speak("Would you like to use a microphone or type in your query? Say 'microphone' or 'type'.")
        user_input = input("Choose input method (microphone/type): ")
        if user_input.lower() not in ['microphone', 'type']:
            speak("Invalid input method. Please try again.")
        else:
            return user_input.lower()

def recognize_speech():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            speak("Please say the name of the astronomical object you want to query:")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            if text:
                speak("You said " + text)
                return text
            else:
                speak("Sorry, I didn't get that. Please try again.")

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that. Please try again.")
            continue
        except sr.RequestError:
            speak("Sorry, there was a problem with the service. Please try again.")
            continue

def recognize_text():
    while True:
        speak("Please type the name of the astronomical object you want to query:")
        text = input("Enter object name: ")
        if text:
            speak("You typed " + text)
            return text
        else:
            speak("Sorry, I didn't get that. Please try again.")

def query_object(object_name):
    catalog_list = Vizier.find_catalogs(object_name)
    result = f"Found {len(catalog_list)} catalogs for {object_name}:\n"
    for name, description in catalog_list.items():
        result += (name + ": " + description.description + "\n")
    # Add the result to the search_results list
    search_results.append(result)
    speak(result)

def continue_search():
    while True:
        speak("Do you want to make another search? Say 'yes' or 'no'.")
        user_input = input("Continue search? (yes/no): ")
        if user_input.lower() not in ['yes', 'no']:
            speak("Invalid input. Please try again.")
        else:
            return user_input.lower() == 'yes'

def show_previous_results():
    speak("Here are all your previous searches:")
    for result in search_results:
        speak(result)

if __name__ == "__main__":
    speak("Welcome to the Vizier astronomical query system.")
    input_method = get_input_method()  # User chooses input method once
    while True:
        if input_method == 'microphone':
            obj_name = recognize_speech()
        elif input_method == 'type':
            obj_name = recognize_text()

        if obj_name:
            query_object(obj_name)

        if continue_search():
            continue
        else:
            speak("Do you want to see all of your previous searches? Say 'yes' or 'no'.")
            user_input = input("Show previous searches? (yes/no): ")
            if user_input.lower() == 'yes':
                show_previous_results()

            speak("Goodbye and see you later for another Astro search of the skies.")
            break
