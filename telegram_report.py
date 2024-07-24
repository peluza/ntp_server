import requests
import schedule
import sqlite3
import time
import os

# Configuración de Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram_report():
    conn = sqlite3.connect("ntp_connections.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT ip, time_since_last_sync
    FROM connections
    WHERE time_since_last_sync > 1440
    ''')
    
    results = cursor.fetchall()
    
    if results:
        message = "Connections with more than 24 hours since last sync:\n\n"
        for ip, time_diff in results:
            message += f"IP: {ip}, Time difference: {time_diff}ms\n"
    else:
        message = "No connections with more than 100ms time difference found."
    
    conn.close()
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": message
    }
    
    response = requests.post(url, params=params)
    if response.status_code == 200:
        print("Telegram report sent successfully")
    else:
        print(f"Failed to send Telegram report. Status code: {response.status_code}")

def schedule_telegram_report():
    schedule.every().day.at("17:00").do(send_telegram_report)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
