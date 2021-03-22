from flask import Flask, render_template,request
import lirc
from platypush.context import get_plugin
from dotenv import load_dotenv
import os
from flask_wtf import Form, RecaptchaField
from wtforms import SubmitField
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
SECRET_KEY = '78w0o5tuuGex5Ktk8VvVDF9Pw3jv1MVE'
recaptcha_public_key = os.environ.get("recaptcha_public")
recaptcha_private_key = os.environ.get("recaptcha_private")
app.locked = False

app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']= recaptcha_public_key
app.config['RECAPTCHA_PRIVATE_KEY']= recaptcha_private_key
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}

def isAllowed():
    return request.headers.get('api_key',"",type=str) != api_key and app.locked

def isNotBot(form):
    return (request.method == 'POST' and form.validate()) or request.headers.get('api_key',"",type=str) == api_key

class AllowedForm(Form):
        recaptcha = RecaptchaField()
        submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html', projector_keys = projector_keys, soundbar_keys = soundbar_keys)

@app.route('/lock', methods=['POST'])
def lock():
    if (request.headers.get('api_key',"",type=str) == api_key):
        app.locked = not app.locked
    return "locked" if app.locked else "unlocked"

@app.route('/<device>/<key>', methods=['GET','POST'])
def projector_send_key(device,key):
    if(isAllowed()):
        return "Not now kiddo"

    form = AllowedForm(request.form)
    if isNotBot(form):
        device = device.lower()
        key = key.lower()

        if(device in ir_devices.keys()):
            commands,remote = ir_devices[device]
            if(key in commands.keys()):
                client.send_once(remote,commands[key],repeat_count=0)
            return "Success"    
        return "that not very poggies of you"

    return render_template('default.html', form=form, url='http://clown.mads.monster/{}/{}'.format(device,key))

@app.route('/Lys/brightness/<value>', methods=['GET','POST'])
def lys_set(value):
    if(isAllowed()):
        return "Not now kiddo"

    form = AllowedForm(request.form)
    if isNotBot(form):
        try:
            value = int(value)
            get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='brightness', value=str(value))
            return "Success"
        except:
            return "that not very poggies of you"

    return render_template('default.html', form=form, url='http://clown.mads.monster/Lys/brightness/{}'.format(value))

@app.route('/Lys/brightness/step/<value>', methods=['GET','POST'])
def lys_step(value):
    if(isAllowed()):
        return "Not now kiddo"

    form = AllowedForm(request.form)
    if isNotBot(form):
        try:
            value = int(value)
            get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='brightness_move', value=str(value))
            return "Success"
        except:
            return "that not very poggies of you"

    return render_template('default.html', form=form, url='http://clown.mads.monster/Lys/brightness/step/{}'.format(value))

@app.route('/Lys', methods=['GET','POST'])
def lys_():
    if(isAllowed()):
        return "Not now kiddo"
    form = AllowedForm(request.form)
    if isNotBot(form):
        get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='state', value='TOGGLE')
        return "Success"
        
    return render_template('default.html', form=form, url='http://clown.mads.monster/Lys')

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 8000,debug = True)
