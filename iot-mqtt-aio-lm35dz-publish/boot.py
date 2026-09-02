# GEEK FACTORY - Dale vuelo a tus proyectos
# https://www.geekfactory.mx
#
# Ejemplo para conectarse a una red WiFi en modo estación (STA) usando
# MicroPython.
#
# NOTA: Este programa puede guardarse como boot.py. MicroPython ejecuta
# este archivo automáticamente al iniciar la Raspberry Pi Pico W, por lo
# que cuando se ejecute main.py la conexión WiFi ya estará establecida.

# Importar los módulos de python usados por este programa
import network
import time
import machine

# Variables que almacenan el nombre de la red inalámrica (SSID)
# y la contraseña que usaremos para autenticarnos con nuestro router.
SSID = 'geek-ejemplos'
PASSWORD = 'geekfactorymx'

# Creamos el objeto que nos permitirá acceder a las funcionalidades
# de la interfaz inalámbrica. Usamos el parámetro network.STA_IF para indicar que
# la interfaz WiFi se utilizará en modo estación (STA) para conectarnos a un router.
wlan = network.WLAN(network.STA_IF)

# Activamos el hardware de la interfaz WiFi
wlan.active(True)

print(f'Conectando a WiFi {SSID}', end='')

# Damos la instrucción de conexión al access point que tenemos configurado
wlan.connect(SSID, PASSWORD)

# Intentar conectar por 30 segundos, registramos el tiempo al iniciar
connect_start = time.ticks_ms()
# Iniciamos un ciclo en el que revisamos cada segundo si se logró la conexión
while not wlan.isconnected():
    print('.', end='')
    time.sleep(1)
    if time.ticks_diff(time.ticks_ms(), connect_start) >= 30_000:
        break

# Llamada a print() para saltar a la siguiente linea
print()

# Revisar si estamos conectados e imprimir la configuración IP que le asignó el router
# a nuestra tarjeta de desarrollo Raspberry Pi Pico.
if wlan.isconnected():
    print('Conectado a AP WiFi')
    print(wlan.ifconfig())
else:
    print(f'No se puede conectar al AP WiFi {SSID}')
    # En caso de que no logremos conectarnos podemos esperar unos segundos
    # y posteriormente reiniciar la tarjeta para intentarlo de nuevo.
    time.sleep(10)
    machine.reset()
