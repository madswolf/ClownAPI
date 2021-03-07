from flask import Flask
import lirc

app = Flask(__name__)
client = lirc.Client()

projector_remote = "AAXA_P7"
soundbar_remote = "AH59-02767A"


projector_keys = {
    "power":"POWER",
    "menu": "MENU",
    "menuUp": "UP",
    "menuDown": "DOWN",
    "menuLeft": "LEFT",
    "menuRight": "RIGHT",
    "inputMenu":"INPUT_SELECT",
    "keystoneUp": "KEYSTONE_UP",
    "keystoneDown": "KEYSTONE_DOWN",
    "back": "RETURN"
}

soundbar_keys = {
    "power":"POWER",
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


if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 8000,debug = True)