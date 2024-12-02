# GEEK FACTORY - Dale vuelo a tus proyectos
# https://www.geekfactory.mx
#
# Ejemplo de sensor analógico LM35DZ con Raspberry Pi Pico y lenguaje de programación
# micropython.
#
from machine import ADC
import time

# objeto utilizado para acceder al pin analógico donde conectaremos el sensor de temperatura
tempadc = ADC(0)

# Función para leer sensor de temperatura LM35DZ
#
# Esta función lee el sensor de temperatura 10 veces y calcula el promedio de las lecturas,
# retornando un valor mas preciso libre de ruido.
def lm35_read_temperature():
    temp = 0
    for i in range(0,10):
        temp += tempadc.read_u16() * 330 / 65536
        time.sleep_us(100)
    return temp/10

# ciclo principal del programa
while True:
    # llamar a la función para leer el sensor e imprimir a la terminal
    temperature = lm35_read_temperature()
    print(f"Temperatura leida por LM35DZ: {temperature}")
    # esperar un segundo entre lecturas para no saturar la pantalla
    time.sleep(1)
    