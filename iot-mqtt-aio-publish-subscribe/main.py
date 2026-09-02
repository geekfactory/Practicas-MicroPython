# GEEK FACTORY - Dale vuelo a tus proyectos
# https://www.geekfactory.mx
#
# Ejemplo de publicación y suscripción MQTT con Adafruit IO.
#
# Este programa realiza dos tareas:
#
# 1. Lee la temperatura de un sensor LM35DZ conectado al ADC de la
#    Raspberry Pi Pico y publica el valor en Adafruit IO.
#
# 2. Se suscribe a un feed de Adafruit IO para controlar el LED
#    integrado de la Raspberry Pi Pico desde Internet.
#
# NOTA:
# Este programa está diseñado para utilizarse junto con el archivo boot.py,
# que establece previamente la conexión a la red WiFi.

import time
import machine
import network
import ubinascii
from umqtt.simple import MQTTClient


# Usuario MQTT de Adafruit IO
AIO_USER = b'geekmx'

# Clave MQTT de Adafruit IO
AIO_KEY = b'REEMPLAZAR_CON_CLAVE_DE_ADAFRUIT_IO'

# Dirección y puerto del servidor MQTT
AIO_SERVER = b'io.adafruit.com'
AIO_PORT = 1883

# Tema MQTT donde se envía la temperatura
TOPIC_TEMPERATURE = b'geekmx/feeds/picotemp'

# Tema MQTT al que nos suscribimos para controlar el LED
TOPIC_LED = b'geekmx/feeds/picoled'

# Intervalo entre publicaciones, en milisegundos
PUBLISH_INTERVAL = 10_000


# Obtener acceso a la interfaz WiFi
wlan = network.WLAN(network.STA_IF)

# Generar el identificador del cliente MQTT usando la dirección MAC
AIO_CLIENT_ID = b'PICO-' + ubinascii.hexlify(wlan.config('mac'))

# Objeto para controlar el LED integrado
led = machine.Pin('LED', machine.Pin.OUT)

# ADC donde está conectado el sensor de temperatura
pin_adc = machine.ADC(0)


def mqtt_callback(topic, message):
    """
    Esta función se ejecuta cuando se recibe un mensaje MQTT.
    """

    print(f'Recibido mensaje en tema {topic}, contenido: {message}')

    if message == b'ON':
        print('LED encendido')
        led.on()

    elif message == b'OFF':
        print('LED apagado')
        led.off()

    else:
        print('Mensaje no reconocido')


def lm35_read_temperature(sensor_adc, vref=3300, samples=10):
    """
    Función para leer un sensor de temperatura LM35DZ.

    :param sensor_adc: Objeto machine.ADC asociado al sensor.
    :param vref: Voltaje de referencia del ADC en milivolts.
    :param samples: Número de muestras para promediar.

    :return: Temperatura medida en grados centígrados.
    """

    total = 0
    LM35_SAMPLE_WAIT = 20

    # Tomar varias mediciones del ADC
    for _ in range(samples):
        total += sensor_adc.read_u16()
        time.sleep_ms(LM35_SAMPLE_WAIT)

    # Calcular el promedio de las lecturas
    readings_average = total / samples

    # Convertir la lectura promedio a milivolts
    voltage_mv = (readings_average * vref) / 65535

    # El LM35 entrega 10 mV por cada grado centígrado
    return voltage_mv / 10.0


# Crear el cliente MQTT
mqtt_client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

# Configurar la función que procesa los mensajes recibidos
mqtt_client.set_callback(mqtt_callback)


try:
    # Conectar al servidor MQTT
    print('Conectando al servidor MQTT...')
    mqtt_client.connect()
    print('Conectado a Adafruit IO')

    # Suscribirnos al tema que controla el LED
    mqtt_client.subscribe(TOPIC_LED)
    print(f'Suscrito a {TOPIC_LED}')

    # Registrar el momento de la última publicación
    last_publish = time.ticks_ms()

    # Ciclo principal
    while True:

        # Procesar los mensajes MQTT entrantes
        mqtt_client.check_msg()

        # Revisar si ya pasó el intervalo entre publicaciones
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_publish) >= PUBLISH_INTERVAL:

            # Leer la temperatura
            temperature = lm35_read_temperature(pin_adc)

            print(f'Temperatura: {temperature:.2f} °C')
            print(f'Publicando en {TOPIC_TEMPERATURE}')

            # Publicar la temperatura
            mqtt_client.publish(TOPIC_TEMPERATURE, str(temperature).encode())

            last_publish = current_time

except Exception as error:
    print('Error MQTT:')
    print(error)