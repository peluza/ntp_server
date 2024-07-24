import ntplib
import time

def check_ntp_server(server, port=123):
    client = ntplib.NTPClient()
    try:
        response = client.request(server, port=port)
        print(f"NTP server {server}:{port} is responding.")
        print(f"Offset: {response.offset:.6f} seconds")
        print(f"Server time: {time.ctime(response.tx_time)}")
        return True
    except:
        print(f"NTP server {server}:{port} is not responding.")
        return False

if __name__ == "__main__":
    server = "localhost"  # Cambia esto a la IP de tu servidor si no es local
    port = 123  # Asegúrate de que este es el puerto correcto de tu servidor NTP
    check_ntp_server(server, port)