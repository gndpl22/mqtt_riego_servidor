
import paho.mqtt.client as mqtt
import time
from queue import Queue
import config


q = Queue()     # objeto para almacenar mensajes recividos
#direccion = "192.168.1.15"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("conectado !!")
    else:
        print("Bad connection Returned code=", rc)


#    print("Connected with result code "+str(rc))

# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.

def on_message(client, userdata, message):
    q.put(message)


mqtt.Client.connected_flag = False  # create flag in class

cliente = mqtt.Client("master")  # creando una instancia de mqtt

cliente.on_connect = on_connect
cliente.on_message = on_message

cliente.loop_start()
print(cliente.connect(config.configuiaraciones_mqtt["direccion"]))
while not cliente.connected_flag:  # wait in loop
    print("esperando coneccion")
    time.sleep(1)
print("Subscribing to topic", "house/bulbs/bulb1")
cliente.subscribe("house/bulbs/bulb1")
print("Publishing message to topic", "house/bulbs/bulb1")
cliente.publish("house/bulbs/bulb1", "OFF")
time.sleep(4)  # wait
cliente.loop_stop()


while not q.empty():
    message = q.get()
    if message is None:
        continue
    print("received from queue, message", str(message.payload.decode("utf-8")))
    print("received from queue, message topic=", message.topic)
    print("received from queue, message qos=", message.qos)
    print("received from queue, message retain flag=", message.retain)

