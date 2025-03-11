import socket
import logging
from datetime import datetime
import threading

# Configuration
HONEYPOT_IP = "0.0.0.0"  # Listen on all interfaces
HONEYPOT_PORT = 2222      # Port to mimic a vulnerable service
LOG_FILE = "honeypot.log"  # Log file to store attacker activity

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def handle_connection(client_socket, client_address):
    """
    Handle incoming connections and log attacker activity.
    """
    try:
        # Log the connection
        logging.info(f"Connection from {client_address[0]}:{client_address[1]}")
        print(f"[+] Connection from {client_address[0]}:{client_address[1]}")

        # Simulate a vulnerable service (e.g., a fake SSH banner)
        client_socket.send(b"SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3\r\n")

        while True:
            # Receive data from the attacker
            data = client_socket.recv(1024)
            if not data:
                break

            # Log the received data
            logging.info(f"Data from {client_address[0]}:{client_address[1]} - {data.decode('utf-8', errors='ignore')}")
            print(f"[+] Data from {client_address[0]}:{client_address[1]} - {data.decode('utf-8', errors='ignore')}")

            # Simulate a response (optional)
            client_socket.send(b"Access denied.\r\n")

    except Exception as e:
        logging.error(f"Error handling connection from {client_address[0]}:{client_address[1]} - {str(e)}")
        print(f"[-] Error handling connection from {client_address[0]}:{client_address[1]} - {str(e)}")

    finally:
        # Close the connection
        client_socket.close()
        logging.info(f"Connection closed from {client_address[0]}:{client_address[1]}")
        print(f"[-] Connection closed from {client_address[0]}:{client_address[1]}")

def start_honeypot():
    """
    Start the honeypot server.
    """
    try:
        # Create a TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HONEYPOT_IP, HONEYPOT_PORT))
        server_socket.listen(5)

        logging.info(f"Honeypot started on {HONEYPOT_IP}:{HONEYPOT_PORT}")
        print(f"[*] Honeypot started on {HONEYPOT_IP}:{HONEYPOT_PORT}")

        while True:
            # Accept incoming connections
            client_socket, client_address = server_socket.accept()

            # Handle the connection in a separate thread
            client_thread = threading.Thread(target=handle_connection, args=(client_socket, client_address))
            client_thread.start()

    except Exception as e:
        logging.error(f"Error starting honeypot - {str(e)}")
        print(f"[-] Error starting honeypot - {str(e)}")

    finally:
        # Close the server socket
        server_socket.close()
        logging.info("Honeypot stopped")
        print("[-] Honeypot stopped")

if __name__ == "__main__":
    start_honeypot()