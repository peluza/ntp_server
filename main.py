import socket
import struct
import time
import threading
import os

from datetime import datetime
from ntp_database import setup_database, update_connection, update_current_date
from telegram_report import schedule_telegram_report

# Configuración del servidor NTP
NTP_PORT = int(os.environ.get("NTP_PORT", 123))
NTP_PACKET_FORMAT = "!B B B b 11I"
NTP_DELTA = 2208988800  # 1970-01-01 00:00:00

def system_to_ntp_time(timestamp):
    return int((timestamp + NTP_DELTA) * 2**32)

def ntp_to_system_time(timestamp):
    return timestamp / 2**32 - NTP_DELTA

def create_response(recv_timestamp, orig_timestamp):
    now = time.time()
    ntp_now = system_to_ntp_time(now)
    
    return struct.pack(NTP_PACKET_FORMAT,
        (0 << 6 | 3 << 3 | 4),  # LI, VN, and Mode
        1,  # Stratum
        0,  # Poll
        -20,  # Precision
        0,  # Root Delay
        0,  # Root Dispersion
        0x4E4C4C00,  # Reference ID ('NULL')
        ntp_now >> 32,  # Reference Timestamp (seconds)
        ntp_now & 0xFFFFFFFF,  # Reference Timestamp (fractional)
        orig_timestamp >> 32,  # Origin Timestamp (seconds)
        orig_timestamp & 0xFFFFFFFF,  # Origin Timestamp (fractional)
        recv_timestamp >> 32,  # Receive Timestamp (seconds)
        recv_timestamp & 0xFFFFFFFF,  # Receive Timestamp (fractional)
        ntp_now >> 32,  # Transmit Timestamp (seconds)
        ntp_now & 0xFFFFFFFF  # Transmit Timestamp (fractional)
    )

def handle_client(sock):
    while True:
        try:
            data, addr = sock.recvfrom(4096)  # Aumentado de 1024 a 4096
            recv_time = time.time()
            recv_timestamp = system_to_ntp_time(recv_time)
            
            client_ip = addr[0]
            update_connection(client_ip)
            
            # Extraer el timestamp original del paquete recibido
            unpacked = struct.unpack('!12I', data[0:48])  # Unpack only the first 48 bytes
            orig_timestamp = (unpacked[6] << 32) | unpacked[7]
            
            response = create_response(recv_timestamp, orig_timestamp)
            sock.sendto(response, addr)
            
            # Imprimir información de depuración (comentado para reducir la salida)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ntp_time = ntp_to_system_time(recv_timestamp)
            ntp_time_str = datetime.fromtimestamp(ntp_time).strftime("%Y-%m-%d %H:%M:%S")
            print(f"Respuesta enviada a {client_ip}")
            print(f"Hora actual del sistema: {current_time}")
            print(f"Hora NTP enviada: {ntp_time_str}")
            print(f"Timestamp NTP (hex): 0x{recv_timestamp:016x}")
            print("--------------------")
        except ConnectionResetError:
            print(f"Conexión reiniciada por el host remoto. Continuando...")
        except Exception as e:
            print(f"Error inesperado: {e}")

def run_server():
    setup_database()
    
    # Iniciar el hilo para actualizar la fecha actual
    update_thread = threading.Thread(target=update_current_date, daemon=True)
    update_thread.start()
    
    # Iniciar el hilo para programar y enviar informes de Telegram
    telegram_thread = threading.Thread(target=schedule_telegram_report, daemon=True)
    telegram_thread.start()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', NTP_PORT))
    print(f"Servidor NTP corriendo en el puerto {NTP_PORT}")
    
    # Iniciar el manejo de clientes en un hilo separado
    client_thread = threading.Thread(target=handle_client, args=(sock,), daemon=True)
    client_thread.start()
    
    # Mantener el hilo principal vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Servidor detenido por el usuario")

if __name__ == "__main__":
    run_server()