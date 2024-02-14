import subprocess
import speech_recognition as sr
import pyttsx3
import pygame
import sys

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 0.9)

# Voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # change index based on your system

# Initialize pygame for playing animal sounds
pygame.mixer.init()

def recognize_speech(recognizer, timeout=5):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            print("\nListening for your command...")
            audio = recognizer.listen(source, timeout=timeout)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            print("Sorry, I didn't hear anything.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError:
            print("Sorry, there was a problem with the speech recognition service.")
            return None

def speak(text, engine):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def play_animal_sound(animal):
    sounds = {
        "lion": "lion.wav",
        "elephant": "elephant.wav",
        # Add more animal sounds here
    }
    sound_file = sounds.get(animal)
    if sound_file:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    else:
        speak(f"Sorry, I don't have a sound for {animal}.", engine)

# Welcome message
speak("Welcome to the animal sounds for the blind. Speak or type the name of the animal you would like to hear.", engine)

# Main loop
while True:
    print("\nSpeak or type the name of the animal you would like to hear. Type 'quit' to exit.")
    text = input("Your input: ").lower()

    if text == 'quit':
        speak("Goodbye!", engine)
        break

    if text:
        play_animal_sound(text)
    else:
        speak("Could you please repeat that?", engine)
