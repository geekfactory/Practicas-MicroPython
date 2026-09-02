# GEEK FACTORY - Dale vuelo a tus proyectos
# https://www.geekfactory.mx
#
# Ejemplo de sensor de temperatura que reporta su valor a través del
# protocolo MQTT al servicio Adafruit IO. Diseñado para Raspberry Pi
# Pico W y sensor LM35DZ analógico.
#
# NOTA: Antes de comenzar a ejecutar este programa se ejecuta boot.py
# que inicializa el WiFi y nos conecta a la red configurada en ese
# archivo.

from umqtt.simple import MQTTClient
import ubinascii

# Variables de configuración del servicio Adafruit IO
# DEBES COLOCAR TUS PROPIAS CREDENCIALES AQUÍ PARA QUE EL EJEMPLO FUNCIONE

# usuario MQTT de adafruit IO
USER = b'geekmx'
# clave MQTT de adafruit IO
KEY = b'0c04e62bd5e5414e86c61d48ba70f7bc'
# tema MQTT a donde se envia la temperatura
PUB_TOPIC = b'geekmx/feeds/picotemp'

# normalmente NO hace falta cambiar el puerto ni el servidor o el client id
# dirección del servidor
SERVER = b'io.adafruit.com'
# puerto del servidor
PORT = 1883
# generamos el client id desde la MAC address
CLIENT_ID = b'PICO' + ubinascii.hexlify(wlan.config('mac'))
# intervalo de actualización (publicación) en milisegundos
UPDATE_INTERVAL = 10_000

# objeto utilizado para acceder al pin analógico donde conectaremos el sensor de temperatura
tempadc = machine.ADC(0)
# crear un objeto llamado mqttc a través del cual interactuamos con el modulo uMQTT
mqttc = MQTTClient(CLIENT_ID, SERVER, PORT, USER, KEY)


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


# conectar al broker MQTT
mqttc.connect()
# variable usada para el control de tiempo de las publicaciones
last_publish = time.ticks_ms()

# ciclo principal del programa donde realizamos la publicación al topic MQTT
while True:
    # obtener el tiempo actual para las operaciones basadas en tiempo
    now = time.ticks_ms()

    # revisar si han transcurrido más de 10 segundos desde la última actualización
    if time.ticks_diff(now, last_publish) >= UPDATE_INTERVAL:
        # llamar a la función que definimos para leer el sensor
        temperature = lm35_read_temperature(tempadc)
        print(f'Publicando temperatura {temperature} en {PUB_TOPIC}')
        # realizar la publicacion de los datos
        mqttc.publish(PUB_TOPIC, f"{temperature:.1f}".encode())
        # almacenar el tiempo en el que se envió la lectura
        last_publish = now
