import pandas as pd
import pyttsx3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def read_excel_file(filename):
    try:
        df = pd.read_excel(filename, engine='openpyxl', sheet_name=None)
        sheets_dict = {sheet_name: sheet_data for sheet_name, sheet_data in df.items()}
        return sheets_dict
    except FileNotFoundError:
        logging.error("The file does not exist.")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

def find_and_speak_formula(formula_name, sheets):
    try:
        for sheet_name, sheet_data in sheets.items():
            # Validate necessary columns
            if all(col in sheet_data.columns for col in ['Formula', 'Equation', 'Units']):
                if formula_name.lower() in sheet_data['Formula'].str.lower().values:
                    formula = sheet_data[sheet_data['Formula'].str.lower() == formula_name.lower()]
                    speak("In sheet: " + sheet_name)
                    speak("Formula: " + formula['Formula'].values[0])
                    speak("Equation: " + formula['Equation'].values[0])
                    speak("Units: " + formula['Units'].values[0])
                    return
            else:
                logging.warning(f"Missing columns in the sheet: {sheet_name}")
        speak("Formula not found in any sheet.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

filename = 'C:\\path\\to\\your\\excel\\file.xlsx'  # Replace with your file path
sheets = read_excel_file(filename)

if sheets:
    formula_name = "Newton's second law"  # Replace with your desired formula
    find_and_speak_formula(formula_name, sheets)
else:
    logging.info("Failed to read the Excel file.")
