import pyttsx3
import textract
import imaplib
import email
import getpass
import os
import ssl

# Initialize the speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    if text is not None:
        engine.say(text)
        engine.runAndWait()

# Function to read files
def read_file():
    for _ in range(3):  # allow 3 attempts
        file_path = getpass.getpass("Please enter the file path of the text file you want me to read: ")
        if os.path.isfile(file_path):
            try:
                text = textract.process(file_path)
                speak(text)
                return
            except Exception as e:
                speak(f"An error occurred while reading the file: {e}")
        else:
            speak("File not found. Please check the file path and try again.")
    speak("Too many failed attempts. Moving on.")

# Function to read emails
def read_emails():
    # Create a secure SSL context
    context = ssl.create_default_context()

    speak("Please enter your email address.")
    user = input().strip()
    speak("Please enter your email password.")
    password = getpass.getpass()  # Securely get the password without showing it in the terminal
    speak("Please enter your email IMAP URL.")
    imap_url = input().strip()

    try:
        # Connect to the mail server
        mail = imaplib.IMAP4_SSL(imap_url, ssl_context=context)

        # Login to the email account
        mail.login(user, password)

        # Select the mailbox you want to check
        mail.select("INBOX")

        # Get the UIDs of the emails
        result, data = mail.uid('search', None, "ALL")
        email_ids = data[0].split()

        # Loop over the emails
        for i in email_ids[-10:]:  # Only read the last 10 emails
            result, email_data = mail.uid('fetch', i, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
            raw_email = email_data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)

            # Get the subject of the email and speak it
            subject = email_message['Subject']
            speak(f"Subject: {subject}")

            result, email_data = mail.uid('fetch', i, '(BODY.PEEK[TEXT])')
            raw_email = email_data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)

            # Get the content of the email and speak it
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    text = part.get_payload(decode=True)
                    speak(text)
    except imaplib.IMAP4.error as e:
        speak("Error occurred during login. Please check your credentials and try again.")
    except Exception as e:
        speak(f"An error occurred while reading emails: {e}")

def main():
    while True:
        speak("Welcome! If you want to read a file, type 'file'. If you want to read emails, type 'email'. To exit, type 'Your script is solid already, but here are a few improvements to consider:

1. Include email subject while reading the email contents.
2. Check if the text extracted from a file is None to avoid potential error while speaking it.
3. Add an "exit" option for the user.
4. Consider an error if the user gives a wrong path multiple times.
5. Add SSL context and check certificate for the email IMAP server to enhance security.

```python
import pyttsx3
import textract
import imaplib
import email
import getpass
import os
import ssl

# Initialize the speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    if text is not None:
        engine.say(text)
        engine.runAndWait()

# Function to read files
def read_file():
    for _ in range(3):  # allow 3 attempts
        file_path = getpass.getpass("Please enter the file path of the text file you want me to read: ")
        if os.path.isfile(file_path):
            try:
                text = textract.process(file_path)
                speak(text)
                return
            except Exception as e:
                speak(f"An error occurred while reading the file: {e}")
        else:
            speak("File not found. Please check the file path and try again.")
    speak("Too many failed attempts. Moving on.")

# Function to read emails
def read_emails():
    # Create a secure SSL context
    context = ssl.create_default_context()

    speak("Please enter your email address.")
    user = input().strip()
    speak("Please enter your email password.")
    password = getpass.getpass()  # Securely get the password without showing it in the terminal
    speak("Please enter your email IMAP URL.")
    imap_url = input().strip()

    try:
        # Connect to the mail server
        mail = imaplib.IMAP4_SSL(imap_url, ssl_context=context)

        # Login to the email account
        mail.login(user, password)

        # Select the mailbox you want to check
        mail.select("INBOX")

        # Get the UIDs of the emails
        result, data = mail.uid('search', None, "ALL")
        email_ids = data[0].split()

        # Loop over the emails
        for i in email_ids[-10:]:  # Only read the last 10 emails
            result, email_data = mail.uid('fetch', i, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
            raw_email = email_data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)

            # Get the subject of the email and speak it
            subject = email_message['Subject']
            speak(f"Subject: {subject}")

            result, email_data = mail.uid('fetch', i, '(BODY.PEEK[TEXT])')
            raw_email = email_data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)

            # Get the content of the email and speak it
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    text = part.get_payload(decode=True)
                    speak(text)
    except imaplib.IMAP4.error as e:
        speak("Error occurred during login. Please check your credentials and try again.")
    except Exception as e:
        speak(f"An error occurred while reading emails: {e}")

def main():
    while True:
        speak("Welcome! If you want to read a file, type 'file'. If you want to read emails, type 'email'. To exit, type 'Here's an enhanced version of your script:

```python
import pyttsx3
import textract
import imaplib
import email
import getpass
import os
import re

# Initialize the speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get user input securely
def secure_input(prompt):
    speak(prompt)
    return getpass.getpass()

# Function to read files
def read_file():
    file_path = secure_input("Please enter the file path of the text file you want me to read.")
    if os.path.isfile(file_path):
        try:
            text = textract.process(file_path)
            speak(text)
        except Exception as e:
            speak(f"An error occurred while reading the file: {e}")
    else:
        speak("File not found. Please check the file path and try again.")

# Function to decode email content
def decode_content(part):
    content = part.get_payload(decode=True)
    charset = part.get_content_charset()
    if charset:
        content = content.decode(charset)
    return content

# Function to read emails
def read_emails():
    user = secure_input("Please enter your email address.")
    password = secure_input("Please enter your email password.")
    imap_url = secure_input("Please enter your email IMAP URL.")

    try:
        # Connect to the mail server
        mail = imaplib.IMAP4_SSL(imap_url)

        # Login to the email account
        mail.login(user, password)

        # Select the mailbox you want to check
        mail.select("INBOX")

        # Get the UIDs of the emails
        result, data = mail.uid('search', None, "ALL")
        email_ids = data[0].split()

        # Loop over the emails
        for i in email_ids[-10:]: # Only read the last 10 emails
            result, email_data = mail.uid('fetch', i, '(BODY.PEEK[])')
            raw_email = email_data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)

            # Get the subject of the email and speak it
            if email_message['Subject']:
                speak(f"Subject: {email_message['Subject']}")

            # Get the content of the email and speak it
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    text = decode_content(part)
                    speak(text)
    except imaplib.IMAP4.error:
        speak("Error occurred during login. Please check your credentials and try again.")
    except Exception as e:
        speak(f"An error occurred while reading emails: {e}")

def main():
    while True:
        speak("Welcome! If you want to read a file, type 'file'. If you want to read emails, type 'email'. To exit, type 'exit'.")
        user_choice = input().strip().lower()
        if user_choice == 'file':
            read_file()
        elif user_choice == 'email':
            read_emails()
        elif user_choice == 'exit':
            break
        else:
            speak("I didn't understand your choice. Let's try again.")

if __name__ == "__main__":
    main()
