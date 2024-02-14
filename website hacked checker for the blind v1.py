import pandas as pd
import requests
import pyttsx3
import pyperclip

# Initialize the TTS engine once at the beginning.
engine = pyttsx3.init()

def speak(text):
    # Use the global engine instance
    engine.say(text)
    engine.runAndWait()

def check_breach(email, headers):
    api_url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}'
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error checking breach for {email}: {e}")
        speak(f"Error checking breach for {email}")
        return None

def process_csv(file_path, headers):
    df = pd.read_csv(file_path)
    results = []

    for index, row in df.iterrows():
        breach_data = check_breach(row['email'], headers)
        results.append({
            'website': row['website/app name'],
            'email': row['email'],
            'breach_data': breach_data
        })

    return results

def display_results(results):
    for result in results:
        if result['breach_data']:
            msg = f"Breach found for {result['email']}: {result['breach_data']}"
            print(msg)
            speak(msg)
        else:
            msg = f"No breach found for {result['email']}"
        print(msg)
        speak(msg)

def ask_to_copy_to_clipboard(text):
    choice = input("Would you like to copy this information to the clipboard? (yes/no): ").strip().lower()
    if choice == 'yes':
        pyperclip.copy(text)

def manual_email_input(headers):
    email = input("Enter the email address: ")
    breach_data = check_breach(email, headers)
    return [{'email': email, 'breach_data': breach_data}]

def main():
    speak("Welcome to the email hacked checker for the blind.")
    print("Welcome to the email hacked checker for the blind.")
    api_key = 'YOUR_API_KEY'
    headers = {'User-Agent': 'YourAppName', 'hibp-api-key': api_key}

    while True:
        choice = input("Upload a CSV file or enter details manually? (csv/manual): ").strip().lower()
        if choice == 'csv':
            file_path = input("Enter the path to your CSV file: ")
            breach_results = process_csv(file_path, headers)
        elif choice == 'manual':
            breach_results = manual_email_input(headers)
        else:
            speak("Invalid input. Please choose 'csv' or 'manual'.")
            continue

        display_results(breach_results)
        ask_to_copy_to_clipboard(str(breach_results))

        again = input("Check another email? (yes/no): ").strip().lower()
        if again != 'yes':
            speak("Alright, have a lovely day and stay safe.")
            print("Alright, have a lovely day and stay safe.")
            break

if __name__ == "__main__":
    main()
