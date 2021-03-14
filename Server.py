from flask import Flask, render_template
import lirc
from platypush.context import get_plugin

app = Flask(__name__)
client = lirc.Client()

#mqtt_client = mqtt.Client("P1") #create new instance
#mqtt_client.connect("localhost",1883,60) #connect to broker

projector_remote = "AAXA_P7"
soundbar_remote = "AH59-02767A"


projector_keys = {
    "power":"POWER",
    "menu": "MENU",
    "menuUp": "UP",
    "menuDown": "DOWN",
    "menuLeft": "LEFT",
    "menuRight": "RIGHT",
    "menuOK": "OK",
    "inputMenu":"INPUT_SELECT",
    "keystoneUp": "KEYSTONE_UP",
    "keystoneDown": "KEYSTONE_DOWN",
    "back": "RETURN"
}

soundbar_keys = {
    "power":"POWER",
    "play-pause": "PLAY_PAUSE",
    "inputSwitch": "INPUT_SWITCH",
    "bluetoothPair": "BT_PAIR",
    "EQSwitch": "SOUND_MODE",
    "mute": "MUTE",
    "settings": "SETTINGS",
    "volumeUp": "VOLUME_UP",
    "volumeDown": "VOLUME_DOWN",
    "volumeToZero": "VOLUME_TOZERO",
    "bassUp": "BASS_UP",
    "bassDown": "BASS_DOWN",
    "bassToZero": "BASS_TOZERO",
}

@app.route('/')
def index():
    return render_template('index.html', projector_keys = projector_keys, soundbar_keys = soundbar_keys)

@app.route('/Projector/<key>')
def projector_send_key(key):
    if(key in projector_keys.keys()):
        client.send_once(projector_remote,projector_keys[key],repeat_count=0)
        return "Success"    
    return "that not very poggies of you"

@app.route('/Soundbar/<key>')
def soundbar_send_key(key):
    if(key in soundbar_keys.keys()):
        client.send_once(soundbar_remote,soundbar_keys[key],repeat_count=0)
        return "Success"    
    return "that not very poggies of you"


@app.route('/Lys/brightness/<value>')
def lys_set(value):
    try:
        value = int(value)
        get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='brightness', value=str(value))
        return "Success"
    except:
        return "that not very poggies of you"

@app.route('/Lys/brightness/step/<value>')
def lys_step(value):
    try:
        value = int(value)
        get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='brightness_move', value=str(value))
        return "Success"
    except:
        return "that not very poggies of you"

@app.route('/Lys/')
def lys_():
    get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='state', value='TOGGLE')
    return "Success"

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 8000,debug = True)