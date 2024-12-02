# GEEK FACTORY - Dale vuelo a tus proyectos
# https://www.geekfactory.mx
#
# Ejemplo de publicación y suscripción MQTT con AdafruitIO.
# El programa permite por una parte enviar o publicar lecturas de temperatura de
# un sensor LM35DZ y también permite controlar el LED de la tarjeta Raspberry Pi Pico
# desde internet utilizando una suscripción a un tema especifico.
#
from umqtt.simple import MQTTClient
import ubinascii

# usuario MQTT de adafruit IO
aiouser = b'geekmx'
# clave MQTT de adafruit IO
aiokey = b'0c04e62bd5e5414e86c61d48ba70f7bc'
# dirección del servidor
aioserver = b'io.adafruit.com'
# puerto del servidor
aioport = 1883
# tema MQTT a donde se envia la temperatura
aiopubt = b'geekmx/feeds/picotemp'
# tema MQTT al que nos suscribimos para controlar el LED
aiosubt = b'geekmx/feeds/picoled'
# generamos el client id desde la MAC address
aiocid = b'PICO'+ubinascii.hexlify(wlan.config('mac'))

# objeto para controlar el pin donde tenemos conectado el LED
ledpin = machine.Pin('LED', machine.Pin.OUT)
# objeto utilizado para acceder al pin analógico donde conectaremos el sensor de temperatura
tempadc = machine.ADC(0)

# Definimos la función que llama la librería uMQTT cuando recibe un mensaje
# en un tema (topic) al que estamos suscritos.
def mqtt_callback(topic, message):
    print(f'Recibido mensaje en tema {topic}, contenido: {message}')
    if message == b'ON':
        ledpin.on(), print('LED encendido')
    elif message == b'OFF':
        ledpin.off(), print('LED apagado')
    else:
        print('Mensaje no reconocido')

# Definimos una función que lee el sensor de temperatura LM35DZ conectado en
# el pin analógico 0
def read_temperature():
    temp = 0
    for i in range(0,10):
        temp += tempadc.read_u16() * 330 / 65536
        time.sleep_us(100)
    return temp/10

# crear un objeto llamado mqttc a través del cual interactuamos con el modulo uMQTT
mqttc = MQTTClient(aiocid, aioserver, aioport, aiouser, aiokey)
# configurar la funcion callback
mqttc.set_callback(mqtt_callback)

# suscripción
try:
    # conectar al agente MQTT
    mqttc.connect()
    # suscribirnos al tema que controla el LED
    mqttc.subscribe(aiosubt)
    # variable usada para el control de tiempo de las publicaciones
    lastpublish = time.time()
    
    # ciclo principal del programa donde realizamos la publicación al topic MQTT
    while True:
        # enviar actualizacion de temperatura cada 10 segundos
        if time.time() - lastpublish >= 10:
            temperature = read_temperature()
            print(f'Publicando temperatura {temperature} en {aiopubt}')
            #realizar la publicacion de los datos
            mqttc.publish(aiopubt, str(temperature).encode())
            lastpublish = time.time()
        # procesar los mensajes entrantes 
        mqttc.check_msg()

except Exception as e:
    print(e)