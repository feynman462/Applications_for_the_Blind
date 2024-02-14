import scapy.all as scapy
import pyttsx3
import logging
import configparser
import csv
import datetime
from pathlib import Path
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def load_config():

    config = configparser.ConfigParser()
    config_file = Path('config.ini')
    if not config_file.is_file():
        engine.say("Configuration file not found in the script's directory. Please ensure config.ini is present.")
        engine.runAndWait()
        return None
    config.read('config.ini')
    return config

def load_suspicious_ips():
    try:
        with open('suspicious_ips.txt', 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        engine.say("Suspicious IP addresses file not found. Please ensure suspicious_ips.txt is present.")
        engine.runAndWait()
        return []

def is_business_hours(start_hour, end_hour):
    current_hour = datetime.datetime.now().hour
    return start_hour <= current_hour < end_hour

def detect_abnormal_traffic(packet, config, total_traffic, suspicious_ips):
sizes and unusual protocols
    if len(packet) > int(config['ABNORMAL_PACKET_SIZE']):
        return "Large packet size detected"
    
    if packet.haslayer(scapy.IP):
        protocol = packet[scapy.IP].proto
        if protocol in config['UNUSUAL_PROTOCOLS']:
            return f"Unusual protocol {protocol} detected"

        ip_src = packet[scapy.IP].src
        ip_dst = packet[scapy.IP].dst
        if ip_src in config['SUSPICIOUS_IP_ADDRESSES'] or ip_dst in config['SUSPICIOUS_IP_ADDRESSES']:
            return f"Suspicious IP address detected: {ip_src} or {ip_dst}"

    if total_traffic > int(config['HIGH_TRAFFIC_VOLUME_THRESHOLD']) and not is_business_hours(int(config['BUSINESS_HOURS_START']), int(config['BUSINESS_HOURS_END'])):
        return "High traffic volume detected during non-business hours"

    return None
    if packet.haslayer(scapy.IP):
        
        ip_src = packet[scapy.IP].src
        ip_dst = packet[scapy.IP].dst
		    
    return None

def alert_user(message):
    engine.say(message)
    engine.runAndWait()

def log_event(packet, message):
    with open('network_events_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), message, packet.summary(), len(packet)])

def packet_handler(packet, config, total_traffic, suspicious_ips):
    abnormality = detect_abnormal_traffic(packet, config, total_traffic, suspicious_ips)
    if abnormality:
        alert_message = f"Abnormal traffic detected. {abnormality}"
        alert_user(alert_message)
        log_event(packet, abnormality)

def main():
    try:
        config = load_config()
        if config is None:
            return

        suspicious_ips = load_suspicious_ips()  # Load initially
        last_update_time = time.time()

        total_traffic = 0
        logging.basicConfig(filename='network_monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')
        start_time = time.time()

        def update_traffic(packet):
            nonlocal total_traffic, suspicious_ips, last_update_time
            total_traffic += len(packet)
            current_time = time.time()
            if current_time - start_time > 1:  # Reset every second
                total_traffic = 0
            if current_time - last_update_time > 300:  # Update IP list every 5 minutes
                suspicious_ips = load_suspicious_ips()
                last_update_time = current_time

        scapy.sniff(prn=lambda packet: [packet_handler(packet, config, total_traffic, suspicious_ips), update_traffic(packet)], store=False)
    except KeyboardInterrupt:
        goodbye_message()
    except Exception as e:
        engine.say(f"An error occurred: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    main()
