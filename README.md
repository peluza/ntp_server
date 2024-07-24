# NTP Server
Este proyecto implementa un servidor NTP (Network Time Protocol) en Python.

### Requisitos

* Python 3.12

### Instalación

1. Clona el repositorio:
```bash
git clone git@github.com:peluza/ntp_server.git
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Ejecución

1. Ejecuta el servidor NTP:
```bash
python main.py
```

2. Configura tu cliente NTP para que se sincronice con el servidor.

### Funcionamiento

El servidor NTP funciona de la siguiente manera:

1. El servidor escucha en el puerto UDP 123.
2. Cuando recibe una solicitud de tiempo, el servidor responde con la hora actual.
3. El cliente NTP utiliza la información del servidor para sincronizar su reloj.

### Ejemplo de uso

Para sincronizar el reloj de tu sistema con el servidor NTP, puedes utilizar el comando `ntpdate`:

```bash
ntpdate 127.0.0.1
```

Reemplaza `127.0.0.1` con la dirección IP del servidor NTP.

### Nota

El servidor NTP se ejecuta en modo de prueba y no está diseñado para uso en producción.
