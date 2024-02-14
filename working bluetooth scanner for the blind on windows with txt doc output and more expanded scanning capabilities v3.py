import asyncio
from bleak import BleakScanner
import pyttsx3

# Initialize the TTS engine globally to avoid reinitializing it every time speak_and_log is called.
engine = pyttsx3.init()

def speak_and_log(text, file_path='sensor_logs.txt'):
    engine.say(text)
    engine.runAndWait()
    with open(file_path, 'a') as log_file:
        log_file.write(text + '\n')

def is_device_of_interest(device, interest_criteria="SpecificDeviceName", signal_strength=-60):
    if device.name is None:
        return False
    return interest_criteria in device.name or device.rssi > signal_strength

def detection_callback_general(device, advertisement_data):
    device_info = f"Detected Device: {device.name or 'Unknown'}, Address: {device.address}, RSSI: {device.rssi}, Data: {advertisement_data}"
    print(device_info)
    speak_and_log(device_info)

def detection_callback_targeted(device, advertisement_data):
    if is_device_of_interest(device):
        device_info = f"Device of interest found: {device.name}, Address: {device.address}, RSSI: {device.rssi}, Data: {advertisement_data}"
        print(device_info)
        speak_and_log(device_info)

async def advanced_scan(mode="general"):
    detection_callback = detection_callback_general if mode == "general" else detection_callback_targeted
    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    await asyncio.sleep(30)  # Scanning time
    await scanner.stop()

def main():
    print("Choose scanning mode: 'general' for all devices or 'targeted' for specific devices.")
    mode = input("Enter mode: ").strip().lower()
    scan_mode = "general" if mode != "targeted" else "targeted"

    # Providing auditory feedback for the mode selected
    speak_and_log(f"Scanning mode set to {scan_mode}. Beginning scan for Bluetooth devices.")
    asyncio.run(advanced_scan(scan_mode))

if __name__ == "__main__":
    main()
