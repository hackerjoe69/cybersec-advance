from scapy.all import *
import time
import datetime
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import TCP, UDP
from scapy.layers.inet import IP

def analyze_packet(packet):
    # Check if the packet is an HTTP packet
    if packet.haslayer(HTTPRequest):
        http_layer = packet.getlayer(HTTPRequest)
        print(f"[HTTP Request] {http_layer.fields}")
        # Perform additional analysis on HTTP packets
        analyze_http_packet(http_layer)
    elif packet.haslayer(TCP) or packet.haslayer(UDP):
        # Extract relevant fields from TCP/UDP packets
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport if packet.haslayer(TCP) else packet[UDP].sport
        dst_port = packet[TCP].dport if packet.haslayer(TCP) else packet[UDP].dport
        print(f"[TCP/UDP Packet] {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
        # Perform additional analysis on TCP/UDP packets
        analyze_tcp_udp_packet(packet)
    else:
        # Handle other packet types
        print(f"[Other Packet] {packet.summary()}")

def analyze_http_packet(http_packet):
    # Perform HTTP packet analysis
    # Check for suspicious HTTP methods or URIs
    if http_packet.Method.decode() == "POST":
        print("[Suspicious] HTTP POST method detected")
    # Check for unusual headers or values
    # Implement additional HTTP packet analysis logic

def analyze_tcp_udp_packet(tcp_udp_packet):
    # Perform TCP/UDP packet analysis
    # Check for anomalies like port scans or packet floods
    # Implement additional TCP/UDP packet analysis logic

def save_packet_log(packet):
    # Save packet details to a log file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {packet.summary()}\n"
    with open("packet_log.txt", "a") as log_file:
        log_file.write(log_entry)

def main():
    print("Network Traffic Analyzer")
    print("Capturing packets...")
    while True:
        # Capture packets using Scapy's sniff function
        packets = sniff(count=10)
        for packet in packets:
            analyze_packet(packet)
            save_packet_log(packet)
        time.sleep(1)  # Wait for 1 second before capturing more packets

if __name__ == "__main__":
    main()