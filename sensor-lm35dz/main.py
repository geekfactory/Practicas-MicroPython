# GEEK FACTORY - Dale vuelo a tus proyectos
# https://www.geekfactory.mx
#
# Ejemplo para leer un sensor de temperatura LM35DZ utilizando una
# Raspberry Pi Pico y MicroPython.
#
import machine
import time

# Objeto para acceder al ADC donde está conectado el LM35DZ
pin_adc = machine.ADC(0)


def lm35_read_temperature(sensor_adc, vref = 3300, samples = 10):
    """
    Función para leer un sensor de temperatura LM35DZ.

    :param sensor_adc: Objeto machine.ADC asociado al sensor.
    :param vref: Voltaje de referencia del ADC en milivolts.
    :param samples: Número de muestras para promediar.
    
    :return: Temperatura medida en grados centígrados.
    """
    total = 0
    SAMPLE_WAIT_TIME = 20

    # Tomar varias mediciones del ADC
    for _ in range(samples):
        total += sensor_adc.read_u16()
        time.sleep_ms(SAMPLE_WAIT_TIME)
        
    # Calcular el promedio de las lecturas
    readings_average = total / samples
    
    # Convertir la lectura promedio a milivolts
    voltage_mv = (readings_average * vref) / 65535
    
    # El LM35 entrega 10 mV por cada grado centígrado
    return voltage_mv / 10.0


# Ciclo principal del programa
while True:
    # Llamar a la función para leer el sensor
    temperature = lm35_read_temperature(pin_adc)
    
    # Imprimir a la terminal
    print(f"Temperatura leida por LM35DZ: {temperature:.1f}")
    
    # Esperar un segundo entre lecturas para no saturar la pantalla
    time.sleep(1)
    