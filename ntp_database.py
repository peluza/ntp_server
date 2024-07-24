import sqlite3
from datetime import datetime
import time
import os

# Configuración de la base de datos SQLite
DB_NAME = os.environ.get("DB_NAME")


def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS connections (
        ip TEXT PRIMARY KEY,
        last_connection TEXT,
        connection_time TEXT,
        time_since_last_connection INTEGER,
        current_date TEXT,
        time_since_last_sync INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def update_connection(ip):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    cursor.execute("SELECT last_connection FROM connections WHERE ip = ?", (ip,))
    result = cursor.fetchone()
    
    if result:
        last_connection = datetime.fromisoformat(result[0])
        time_since_last = int((datetime.now() - last_connection).total_seconds() /60)
        cursor.execute('''
        UPDATE connections 
        SET last_connection = ?, time_since_last_connection = ?,
            current_date = ?, time_since_last_sync = ?
        WHERE ip = ?
        ''', (now, time_since_last, now, 0, ip))
    else:
        cursor.execute('''
        INSERT INTO connections (ip, last_connection, connection_time, time_since_last_connection, current_date, time_since_last_sync)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (ip, now, now, 0, now, 0))
    
    conn.commit()
    conn.close()

def update_current_date():
    while True:
        time.sleep(60)  # Espera 1 minuto
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute('''
        UPDATE connections
        SET current_date = ?,
            time_since_last_sync = (strftime('%s', ?) - strftime('%s', last_connection)) / 60
        ''', (now, now))
        
        conn.commit()
        conn.close()
