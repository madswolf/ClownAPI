from flask import Flask, render_template,request
import lirc
from platypush.context import get_plugin
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
client = lirc.Client()

projector_remote = "AAXA_P7"
soundbar_remote = "AH59-02767A"


projector_keys = {
    "power":"POWER",
    "menu": "MENU",
    "menuup": "UP",
    "menudown": "DOWN",
    "menuleft": "LEFT",
    "menuright": "RIGHT",
    "menuok": "OK",
    "inputmenu":"INPUT_SELECT",
    "keystoneup": "KEYSTONE_UP",
    "keystonedown": "KEYSTONE_DOWN",
    "back": "RETURN"
}

soundbar_keys = {
    "power":"POWER",
    "play-pause": "PLAY_PAUSE",
    "inputswitch": "INPUT_SWITCH",
    "bluetoothpair": "BT_PAIR",
    "eqSwitch": "SOUND_MODE",
    "mute": "MUTE",
    "settings": "SETTINGS",
    "volumeup": "VOLUME_UP",
    "volumedown": "VOLUME_DOWN",
    "volumetozero": "VOLUME_TOZERO",
    "bassup": "BASS_UP",
    "bassdown": "BASS_DOWN",
    "basstozero": "BASS_TOZERO",
}

ir_devices = {
    "soundbar": [soundbar_keys,soundbar_remote],
    "projector": [projector_keys,projector_remote]
}


api_key = os.environ.get("api_key")
app.locked = False

@app.route('/')
def index():
    return render_template('index.html', projector_keys = projector_keys, soundbar_keys = soundbar_keys)

@app.route('/lock', methods=['POST'])
def lock():
    if (api_key == request.form['api_key']):
        app.locked = not app.locked
    return "locked" if app.locked else "unlocked"

@app.route('/<device>/<key>')
def projector_send_key(device,key):
    if(request.form.get('api_key',"",type=str) != api_key and app.locked):
        return "Not now kiddo"

    device = device.lower()
    key = key.lower()

    if(device in ir_devices.keys()):
        commands,remote = ir_devices[device]
        if(key in commands.keys()):
            client.send_once(remote,commands[key],repeat_count=0)
        return "Success"    
    return "that not very poggies of you"

@app.route('/Lys/brightness/<value>')
def lys_set(value):
    if(request.form.get('api_key',"",type=str) != api_key and app.locked) :
        return "Not now kiddo"

    try:
        value = int(value)
        get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='brightness', value=str(value))
        return "Success"
    except:
        return "that not very poggies of you"

@app.route('/Lys/brightness/step/<value>')
def lys_step(value):
    if(request.form.get('api_key',"",type=str) != api_key and app.locked):
        return "Not now kiddo"

    try:
        value = int(value)
        get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='brightness_move', value=str(value))
        return "Success"
    except:
        return "that not very poggies of you"

@app.route('/Lys')
def lys_():
    if(request.form.get('api_key',"",type=str) != api_key and app.locked):
        return "Not now kiddo"

    get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='state', value='TOGGLE')
    return "Success"

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 8000,debug = True)