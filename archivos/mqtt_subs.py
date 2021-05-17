import paho.mqtt.client as mqtt
import time
from queue import Queue
import config


q = Queue() 

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        
    else:
        print("Bad connection Returned code=", rc)



def on_message(client, userdata, message):
    q.put(message)


def on_subscribe(client,obj,mid,granted_qos):
    print("Subscrito a: " + str(mid) + "  qos: " +str(granted_qos[0]) )
   


mqtt.Client.connected_flag = False  # create flag in class


cliente = mqtt.Client(client_id= config.configuraciones_mqtt["nombre"])  # creando una instancia de mqtt
cliente.on_connect = on_connect
cliente.on_message = on_message
cliente.on_subscribe = on_subscribe
cliente.connect(config.configuraciones_mqtt["direccion"])

for tema in config.temas_mqtt :
    try:
        suscripcion=cliente.subscribe(tema,qos=2)
        print ("tema: "+ str(tema)+ "    Respuesta "+ str(suscripcion))
        

    except Exception as e:
        print("ha ocurrido un error de subscripcion:")
        print(e)


for i in range(5):
# cliente.loop_forever()


    cliente.loop_start()
    cliente.publish("house/bulbs/bulb2", "OFF")
    time.sleep(1)
    cliente.loop_stop()

while not q.empty():
    message = q.get()
    if message is None:
        continue
    print("received from queue, message", str(message.payload.decode("utf-8")))
    # print("received from queue, message", str(message.))
    print("received from queue, message topic=", message.topic)
    print("received from queue, message qos=", message.qos)
    print("received from queue, message retain flag=", message.retain)
