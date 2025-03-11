import requests
from bs4 import BeautifulSoup
import sqlite3
import time

def collect_threat_data():
    # VirusTotal API key
    vt_api_key = 'YOUR_VIRUSTOTAL_API_KEY'

    # Shodan API key
    shodan_api_key = 'YOUR_SHODAN_API_KEY'

    # URLs to scrape threat data from
    urls = [
        'https://www.virustotal.com/gui/domain/example.com/detection',
        'https://www.shodan.io/search?query=malware'
    ]

    # Connect to the SQLite database
    conn = sqlite3.connect('threat_data.db')
    cursor = conn.cursor()

    # Create a table to store the threat data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threat_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            data TEXT,
            timestamp TEXT
        )
    ''')

    # Collect data from VirusTotal
    for url in urls:
        if 'virustotal' in url:
            response = requests.get(url, headers={'x-apikey': vt_api_key})
            if response.status_code == 200:
                data = response.json()
                cursor.execute('''
                    INSERT INTO threat_data (source, data, timestamp)
                    VALUES (?, ?, ?)
                ''', ('VirusTotal', str(data), str(int(time.time()))))
                conn.commit()

    # Collect data from Shodan
    for url in urls:
        if 'shodan' in url:
            response = requests.get(url, params={'key': shodan_api_key})
            if response.status_code == 200:
                data = response.json()
                cursor.execute('''
                    INSERT INTO threat_data (source, data, timestamp)
                    VALUES (?, ?, ?)
                ''', ('Shodan', str(data), str(int(time.time()))))
                conn.commit()

    # Close the database connection
    conn.close()

def main():
    collect_threat_data()

if __name__ == '__main__':
    main()