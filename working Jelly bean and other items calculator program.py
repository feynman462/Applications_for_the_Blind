import math
import pyttsx3
import speech_recognition as sr
from word2number import w2n
import pyperclip

def initialize_engine():
    engine = pyttsx3.init()
    return engine

def initialize_recognizer():
    recog = sr.Recognizer()
    return recog

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech(recog, engine, prompt=None):
    if prompt:
        speak(engine, prompt)
    with sr.Microphone() as source:
        recog.adjust_for_ambient_noise(source)
        audio = recog.listen(source)
        try:
            return recog.recognize_google(audio)
        except (sr.UnknownValueError, sr.RequestError) as e:
            speak(engine, "I couldn't understand that. Could you please repeat?")
            return recognize_speech(recog, engine, prompt)

def get_float_value(recog, engine, input_method, prompt):
    while True:
        try:
            if input_method == 'speak':
                value_str = recognize_speech(recog, engine, prompt)
                value = float(w2n.word_to_num(value_str))
            else:
                value_str = input(prompt)
                value = float(value_str)

            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            speak(engine, f"Invalid input, please provide a positive number for {prompt}")
        except Exception:
            speak(engine, f"Could not convert {value_str} to a number, please try again.")

def calculate_objects(diameter, height, object):
    volume = math.pi * (diameter / 2) ** 2 * height
    packing_efficiency = 0.67

    if object == 'jelly beans':
        object_size = 1.25
    elif object == 'bouncy balls':
        object_size = 2.5
    elif object == 'pennies':
        object_size = 0.35
    elif object == 'nickels':
        object_size = 0.69
    elif object == 'dimes':
        object_size = 0.20
    elif object == 'quarters':
        object_size = 0.81
    elif object == 'assorted coins':
        object_size = 0.51

    num_objects = int(volume * packing_efficiency / object_size)
    return num_objects

def choose_input_method(engine):
    while True:
        speak(engine, "Would you prefer to speak or type your inputs? Please say 'speak' or 'type'")
        method = input("Would you prefer to speak or type your inputs? Please type 'speak' or 'type': ")
        if method.lower() in ['speak', 'type']:
            return method.lower()
        speak(engine, "Invalid option. Please say 'speak' or 'type'")

def choose_object(engine):
    while True:
        speak(engine, "What kind of object do you want to calculate? Please type one of the following: "
                      "'jelly beans', 'bouncy balls', 'pennies', 'nickels', 'dimes', 'quarters', 'assorted coins'")
        object = input("What kind of object do you want to calculate? Please type one of the following: "
                       "'jelly beans', 'bouncy balls', 'pennies', 'nickels', 'dimes', 'quarters', 'assorted coins': ")
        if object.lower() in ['jelly beans', 'bouncy balls', 'pennies', 'nickels', 'dimes', 'quarters', 'assorted coins']:
            return object.lower()
        speak(engine, "Invalid object. Please type one of the listed options")

def offer_copy_result(engine, input_method, result):
    if input_method == 'type':
        speak(engine, "Do you want to copy the result to your clipboard? Please type 'yes' or 'no': ")
        answer = input("Do you want to copy the result to your clipboard? Please type 'yes' or 'no': ")
        if answer.lower() == 'yes':
            pyperclip.copy(str(result))

def ask_repeat_calculation(engine, recog):
    speak(engine, "Would you like to calculate again? Please say 'yes' or 'no'")
    answer = recognize_speech(recog, engine, "Would you like to calculate again? Please say 'yes' or 'no'")
    if answer.lower() == 'yes':
        main()

def main():
    engine = initialize_engine()
    recog = initialize_recognizer()

    speak(engine, "Welcome to the Object Volume Calculator!")

    input_method = choose_input_method(engine)
    object = choose_object(engine)

    diameter = get_float_value(recog, engine, input_method, "Please say or type the diameter in cm of your jar: ")
    height = get_float_value(recog, engine, input_method, "Now, please say or type the height in cm of your jar: ")

    speak(engine, f"Calculating the number of {object}...")
    num_objects = calculate_objects(diameter, height, object)
    
    speak(engine, f"The estimated number of {object} in the jar is: {num_objects}")
    
    offer_copy_result(engine, input_method, num_objects)

    ask_repeat_calculation(engine, recog)

if __name__ == "__main__":
    main()
