import requests
import sqlite3
import time

def collect_threat_data():
    # Prompt user for API keys and domain
    vt_api_key = input("Enter your VirusTotal API key: ").strip()
    shodan_api_key = input("Enter your Shodan API key: ").strip()
    domain = input("Enter the domain to investigate: ").strip()

    # Construct URLs using user input
    vt_url = f'https://www.virustotal.com/api/v3/domains/{domain}'
    shodan_url = 'https://api.shodan.io/shodan/host/search'

    # Connect to SQLite DB
    conn = sqlite3.connect('threat_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threat_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            data TEXT,
            timestamp TEXT
        )
    ''')

    # --- VirusTotal Data Collection ---
    try:
        headers = {'x-apikey': vt_api_key}
        response = requests.get(vt_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            cursor.execute('''
                INSERT INTO threat_data (source, data, timestamp)
                VALUES (?, ?, ?)
            ''', ('VirusTotal', str(data), str(int(time.time()))))
            conn.commit()
            print("[+] VirusTotal data collected successfully.")
        else:
            print(f"[!] VirusTotal request failed: {response.status_code}")
    except Exception as e:
        print(f"[!] VirusTotal error: {e}")

    # --- Shodan Data Collection ---
    try:
        params = {'key': shodan_api_key, 'query': domain}
        response = requests.get(shodan_url, params=params)
        if response.status_code == 200:
            data = response.json()
            cursor.execute('''
                INSERT INTO threat_data (source, data, timestamp)
                VALUES (?, ?, ?)
            ''', ('Shodan', str(data), str(int(time.time()))))
            conn.commit()
            print("[+] Shodan data collected successfully.")
        else:
            print(f"[!] Shodan request failed: {response.status_code}")
    except Exception as e:
        print(f"[!] Shodan error: {e}")

    conn.close()

def main():
    collect_threat_data()

if __name__ == '__main__':
    main()
