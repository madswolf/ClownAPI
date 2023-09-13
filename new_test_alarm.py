import os
from paho.mqtt import client as mqtt_client
from dotenv import load_dotenv
import pygame
load_dotenv()

zigbee2mqtt_host = os.environ.get("zigbee2mqtt_host")
zigbee2mqtt_port = int(os.environ.get("zigbee2mqtt_port"))

zigbee2mqtt_client_id = os.environ.get("zigbee2mqtt_client_id")
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(zigbee2mqtt_client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(zigbee2mqtt_host, zigbee2mqtt_port)
    return client

client = connect_mqtt()
topic = f"zigbee2mqtt/Amplifier/set"
msg = "{ \"state\": \"ON\" }"
result = client.publish(topic,msg)

path = '/home/pi/ClownAPI/sounds/CantinaBand3.wav'
#os.system("omxplayer --vol 100 -o local sounds/CantinaBand3.wav")

pygame.mixer.init()
sound = pygame.mixer.Sound('/home/pi/ClownAPI/sounds/CantinaBand60.wav')
sound.set_volume(0.01)
volume = 0.01
playing = sound.play()
while playing.get_busy():
    volume = volume + 0.01
    sound.set_volume(volume)
    print("current volume: " + str(volume))
    pygame.time.delay(100)

topic = f"zigbee2mqtt/Amplifier/set"
msg = "{ \"state\": \"OFF\" }"
result = client.publish(topic,msg)