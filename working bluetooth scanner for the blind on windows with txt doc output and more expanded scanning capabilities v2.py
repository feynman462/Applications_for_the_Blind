import asyncio
from bleak import BleakScanner
import pyttsx3

def speak_and_log(text, file_path='sensor_logs.txt'):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    with open(file_path, 'a') as log_file:
        log_file.write(text + '\n')

def is_device_of_interest(device):
    if device.name is None:
        return False
    # Modify the criteria as needed
    return "SpecificDeviceName" in device.name or device.rssi > -60

def detection_callback(device, advertisement_data):
    if is_device_of_interest(device):
        device_info = f"Device of interest found: {device.name}, Address: {device.address}, RSSI: {device.rssi}, Data: {advertisement_data}"
        print(device_info)
        speak_and_log(device_info)

async def advanced_scan():
    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    await asyncio.sleep(30)
    await scanner.stop()

asyncio.run(advanced_scan())
