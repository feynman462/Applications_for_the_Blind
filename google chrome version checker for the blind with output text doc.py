import pyttsx3
import subprocess

def speak(text):
    """Use text-to-speech to announce the provided text."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_chrome_version():
    try:
        result = subprocess.run(['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'], stdout=subprocess.PIPE)
        version = result.stdout.decode('utf-8').split(' ')[-1].strip()
        return version
    except:
        return None

def main():
    chrome_version = get_chrome_version()
    if not chrome_version:
        message = "Could not determine the version of Google Chrome."
        speak(message)
        with open('output_google_chrome_version.txt', 'w') as file:
            file.write(message)
        return

    message = f"Your Google Chrome version is {chrome_version}."
    speak(message)
    with open('output_google_chrome_version.txt', 'w') as file:
        file.write(message)

if __name__ == "__main__":
    main()
