# GEEK FACTORY - Dale vuelo a tus proyectos
# https://www.geekfactory.mx
#
# Ejemplo de para hacer parpadear un LED conectado al pin PG0 de Raspberry
# Pi Pico. Este es un ejemplo básico de cómo manejar salidas digitales.
#

# importar los módulos de python necesarios para que este programa funcione
import machine, time

# crear un objeto a través del cual manipularemos el pin como salida
pinled = machine.Pin(0, machine.Pin.OUT)

# ciclo principal del programa donde alternaremos el estado del pin
while True:
    pinled.value(1)
    time.sleep(1)
    pinled.value(0)
    time.sleep(1)