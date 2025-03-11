import re
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

def analyze_log(log_file):
    # Define patterns to search for
    patterns = [
        r'Failed password for .* from .*',
        r'Invalid user .* from .*',
        r'Connection closed by authenticating user .*',
        r'Authentication failure for .* from .*'
    ]

    # Open the log file
    with open(log_file, 'r') as file:
        # Read the log file line by line
        for line in file:
            # Check if any pattern matches the line
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    print("Intrusion detected:", match.group())
                    # Send an alert email
                    send_alert_email(match.group())
                    break

def send_alert_email(intrusion_details):
    # Configure email settings
    sender_email = 'your_email@example.com'
    receiver_email = 'recipient_email@example.com'
    password = 'your_email_password'
    smtp_server = 'smtp.example.com'
    smtp_port = 587

    # Create a MIMEMultipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Intrusion Alert'

    # Add the intrusion details to the message body
    body = f'Intrusion detected: {intrusion_details}'
    message.attach(MIMEText(body, 'plain'))

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def main():
    # Path to the system log file
    log_file = '/path/to/your/system/log'

    print("Intrusion Detection System (IDS)")
    print("Monitoring system logs for intrusions...")

    while True:
        # Analyze the log file
        analyze_log(log_file)
        time.sleep(1)  # Wait for 1 second before checking again

if __name__ == "__main__":
    main()