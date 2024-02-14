import os
import subprocess
from wifi import Cell, Scheme

def main():
    print("Welcome to the Raspberry Shake Wi-Fi setup!")

    ssid = input("Please enter the SSID of your Wi-Fi network: ")
    password = input("Please enter the password for your Wi-Fi network: ")

    setup_wifi(ssid, password)
    print("Wi-Fi setup complete. Please check your connection.")

def setup_wifi(ssid, password):
    cells = Cell.all('wlan0')

    for cell in cells:
        if cell.ssid == ssid:
            try:
                scheme = Scheme.find('wlan0', ssid)
            except IndexError:
                scheme = Scheme.for_cell('wlan0', ssid, cell, password)
                scheme.save()

            scheme.activate()
            break
    else:
        print("Network not found. Please check the SSID and try again.")

if __name__ == "__main__":
    main()
