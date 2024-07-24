import sqlite3
import csv

def convert_to_csv(db_file, csv_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM connections")
    rows = cursor.fetchall()

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cursor.description])
        writer.writerows(rows)

    conn.close()

if __name__ == "__main__":
    db_file = "ntp_connections.db"
    csv_file = "ntp_connections.csv"
    convert_to_csv(db_file, csv_file)
    print(f"Archivo SQLite '{db_file}' convertido a CSV '{csv_file}'")
    
# Ejecuta el script para convertir el archivo SQLite a CSV.
# El archivo CSV se creará en la misma carpeta que el script.