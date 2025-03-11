from scapy.all import *

def sniff_packets(interface):
    # Define a callback function to process each captured packet
    def process_packet(packet):
        print(f"Packet captured: {packet.summary()}")

    # Start sniffing packets on the specified interface
    sniff(iface=interface, prn=process_packet)

def main():
    # Specify the network interface to sniff packets from
    interface = 'eth0'

    # Start sniffing packets
    sniff_packets(interface)

if __name__ == '__main__':
    main()