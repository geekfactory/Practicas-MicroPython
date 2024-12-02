# GEEK FACTORY - Dale vuelo a tus proyectos
# https://www.geekfactory.mx
#
# Ejemplo para leer el sensor de temperatura interno de un microcontrolador RP2040
# Creamos una función que podemos reutilizar en nuestros proyectos para leer la temperatura
# con el sensor interno.
#
import machine,time

# objeto utilizado para acceder al pin canal analógico del sensor de temperatura interno
tempadc = machine.ADC(4)

# Función para leer sensor de temperatura interno de un microcontrolador RP2040
#
# Esta función lee el sensor de temperatura 10 veces y calcula el promedio de las lecturas,
# retornando un valor mas preciso y libre de ruido.
def tsensor_read_temperature():
    temp = 0
    for i in range(0,10):
        temp += 27 - ((tempadc.read_u16() * (3.3 / 65536)) - 0.706) / 0.001721
        time.sleep_us(100)
    return temp/10

# ciclo principal del programa
while True:
    # llamar a la función para leer el sensor e imprimir a la terminal
    temperature = tsensor_read_temperature()
    print(f"Temperatura leida por sensor interno: {temperature}")
    # esperar un segundo entre lecturas para no saturar la pantalla
    time.sleep(1)