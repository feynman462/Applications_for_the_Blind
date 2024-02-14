import warnings
import pyttsx3
import speech_recognition as sr
import keyboard
import time
from astroquery.jplhorizons import Horizons
from astroquery.simbad import Simbad

# Suppress Astropy warnings
warnings.filterwarnings('ignore', category=UserWarning, append=True)
warnings.filterwarnings('ignore', category=Warning, append=True)

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.paused = False
        self.speaking = False
        self.set_volume(1.0)
        self.set_rate(150)

    def set_volume(self, volume):
        self.engine.setProperty('volume', volume)

    def set_rate(self, rate):
        self.engine.setProperty('rate', rate)

    def speak_sentence(self, sentence):
        self.speaking = True
        if not self.paused:
            self.engine.say(sentence)
            self.engine.runAndWait()
        self.speaking = False

    def speak(self, text, should_speak=True):
        print(text)
        if should_speak:
            sentences = text.split(". ")
            for sentence in sentences:
                while self.paused:
                    time.sleep(0.1)  # Wait while paused
                if self.speaking:  # If still speaking (i.e., paused in middle), then skip
                    continue
                self.speak_sentence(sentence + ".")

    def pause_or_resume(self, e):
        if self.speaking:  # Only allow pausing/resuming if currently speaking
            self.paused = not self.paused
            if self.paused:
                self.engine.stop()

speaker = Speaker()
keyboard.on_press_key("p", speaker.pause_or_resume)  # Use the 'p' key to pause/resume

def get_audio_preference():
    user_input = input("Do you want to hear audio prompts? (yes/no): ").strip().lower()
    return user_input == 'yes'

def get_input_method():
    while True:
        user_input = input("Choose input method (microphone/type): ").strip().lower()
        if user_input not in ['microphone', 'type']:
            speaker.speak("Invalid input method. Please try again.", get_audio_preference())
        else:
            return user_input

def search_object(name):
    id_types = ['smallbody', 'majorbody', 'spacecraft', 'natural satellite']
    major_body_codes = {'mercury': '199', 'venus': '299', 'earth': '399', 'mars': '499',
                        'jupiter': '599', 'saturn': '699', 'uranus': '799', 'neptune': '899',
                        'pluto': '999'}

    if name.lower() in major_body_codes:
        name = major_body_codes[name.lower()]

    for id_type in id_types:
        try:
            obj = Horizons(id=name, id_type=id_type)  # Fetching the object
            eph = obj.ephemerides()  # Getting the ephemerides of the object
            if len(eph) > 0:
                return eph['RA', 'DEC', 'datetime_jd', 'PABLon', 'PABLat']  # Return the specific columns
        except Exception as e:
            speaker.speak(f"An error occurred while searching for the object with id_type {id_type}. Error: " + str(e), get_audio_preference())

    try:
        result_table = Simbad.query_object(name)
        return result_table
    except Exception as e:
        speaker.speak(f"An error occurred while searching for the object with SIMBAD. Error: " + str(e), get_audio_preference())

    return None

def main():
    should_speak = get_audio_preference()
    input_method = get_input_method()

    while True:
        speaker.speak("Please speak or type the name of the celestial object you want to search.", should_speak)
        if input_method == 'microphone':
            r = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    audio = r.listen(source)
                    name = r.recognize_google(audio)
                except sr.UnknownValueError:
                    speaker.speak("Could not understand audio. Please try again.", should_speak)
                    continue
                except sr.RequestError as e:
                    speaker.speak("Could not request results from Google Speech Recognition service. Please check your internet connection and try again.", should_speak)
                    continue
        else:
            name = input("Enter the name of the celestial object: ").strip()

        result = search_object(name)
        if result is not None:
            speaker.speak("Here are the details of the object: " + str(result), should_speak)
        else:
            speaker.speak("No results found for the object: " + name, should_speak)

        user_input = input("Would you like to search again? (yes/no): ").strip().lower()
        if user_input != 'yes':
            break

if __name__ == "__main__":
    main()
