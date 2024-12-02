# GEEK FACTORY - Dale vuelo a tus proyectos
# https://www.geekfactory.mx
#
# Ejemplo para conectarse a una red WiFi en modo estación (STA) usando
# MicroPython. Este programa puede colocarse en el archivo boot.py en el
# sistema de archivos de la Raspberry Pi Pico W. De esta forma al ejecutar
# el archivo main.py ya tendremos activa la interfaz inalámbrica.
#
    
# importar los módulos de python usados por este programa
import network, time, sys

# variables que almacenan el nombre de la red inalámrica (SSID)
# y la contraseña que usaremos para autenticarnos
netssid = 'geek-ejemplos'
netpass = 'geekfactorymx'

# creamos el objeto que nos permitirá acceder a las funcionalidades
# de la interfaz inalámbrica. Usamos el parámetro network.STA_IF para indicar que
# la interfaz WiFI se utilizará en módo STATION para conectarnos a un router
wlan = network.WLAN(network.STA_IF)

# activamos el hardware de la interfaz WiFi
wlan.active(True)

print(f'Conectando a WiFi {netssid} password {netpass} ',end='')

# damos la instrucción de conexión al access point que tenemos configurado
wlan.connect(netssid, netpass)

# intentar conecter por 30 segundos
connectstart = time.time();
# inciamos un ciclo en el que revisamos cada segundo si se logró la conexión
while not wlan.isconnected() and time.time() - connectstart  < 30:
    print('.',end='')
    time.sleep(1)

# llamada a print() para saltar a la siguiente linea
print()

# revisar si estamos conectados e imprimir la configuración IP que le asignó el router
# a nuestra tarjeta de desarrollo Raspberry Pi Pico
if wlan.isconnected():
    print('Conectado a AP WiFi'), print(wlan.ifconfig())
else:
    print(f'No se puede conectar al AP WiFi {netssid}')
    # en caso de que no logremos conectarnos podemos esperar unos segundos   
    time.sleep(10)
    # y posteriormente realizar un "soft reset" para intentarlo de nuevo
    sys.exit()
    # o quizá también funcione realizar un "hard reset"
    # machine.reset()