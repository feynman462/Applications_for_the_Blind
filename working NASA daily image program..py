# Install required libraries:
# pip install gtts requests

import requests
from gtts import gTTS
import os
import sys
import platform

def get_nasa_apod_data(api_key):
    # NASA APOD API URL
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

    try:
        # Send an HTTP GET request to the NASA APOD API
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()

            # Extract the desired information (modify as needed)
            title = data['title']
            explanation = data['explanation']
            return title, explanation
        else:
            print(f"Error: Unable to retrieve data from the NASA APOD API. Status code: {response.status_code}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error: Request to NASA APOD API failed: {e}")
        return None, None

def text_to_speech(data):
    tts = gTTS(text=data, lang='en')
    tts.save("data_speech.mp3")
    if platform.system() == "Windows":
        os.system("start data_speech.mp3")
    else:
        os.system("mpg321 data_speech.mp3")

if __name__ == "__main__":
    api_key = "vzHq8frkde4mUL5D6tVUWfGU4c2e77ZAQXmglGhy"  # Replace with your actual NASA API key
    title, explanation = get_nasa_apod_data(api_key)
    if title and explanation:
        print("Today's Astronomy Picture of the Day is titled:")
        print(title)
        print("Explanation:")
        print(explanation)
        print("Converting the explanation text to speech:")
        text_to_speech(explanation)
    else:
        print("No data received from the NASA APOD API.")
