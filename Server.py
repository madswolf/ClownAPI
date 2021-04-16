from flask import Flask, render_template,request
import lirc
from platypush.context import get_plugin
from dotenv import load_dotenv
import os
from flask_wtf import Form, RecaptchaField
from wtforms import SubmitField, StringField,validators
from datetime import datetime, time, date
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

sounds = {
    "honk": "honk-sound.mp3",
    "amogus": "among.mp3",
    "ps1": "ps_1.mp3",
    "oof": "steve-old-hurt-sound_XKZxUk4.mp3",
    "water": "y2mate_HOnnyD0.mp3",
    "tada": "win31.mp3",
    "holup": "record-scratch-sound-effect.mp3",
    "die": "you-must-die.mp3",
    "listen": "zelda-navi-listen.mp3",
    "waah": "golden.mp3",
    "bruh": "bruh.mp3",
    "bruh2": "movie_1.mp3",
    "discord": "discord.mp3",
    "why": "bully.mp3",
    "wallah": "sound-9.mp3",
    "dude": "lol_33.mp3",
    "smash": "lemme-smash.mp3",
    "discord2": "discord-leave.mp3",
    "metal-gear": "tindeck_1.mp3",
    "weed": "snoop-dogg-smoke-weed-everyday.mp3",
    "booey": "bababooey-sound-effect.mp3",
    "ah-shit": "gta-san-andreas-ah-shit-here-we-go-again_BWv0Gvc.mp3",
    "help": "untitled3_13.mp3",
    "legetøj": "toy-story_2.mp3",
    "death": "lego-yoda-death-sound-effect.mp3",
    "snask": "voice_sans.mp3",
    "classic": "murloc.mp3",
    "wrong": "my-movie_lu1KTdg.mp3",
    "mogus2": "Among_us_beatbox.mp3",
    "horny": "horny.mp3",
    "go": "lesgo.mp3",
    "convertible": "convertible.mp3",
    "FBI": "fbi-open-up-sfx.mp3",
    "bunu-moan": "uæøah.mp3",
    "cum":"cum.mp3",
    "burger": "burgerking.mp3",
}

dayTimes = {
    0 : (time(7,30),time(23,00),"Monday"),
    1 : (time(7,30),time(23,00),"Tuesday"),
    2 : (time(7,30),time(23,00),"Wednesday"),
    3 : (time(7,30),time(23,00),"Thursday"),
    4 : (time(7,30),time(23,00),"Friday"),
    5 : (time(9,00),time(1,00),"Saturday"),
    6 : (time(9,00),time(1,00),"Sunday"),
}



api_key = os.environ.get("api_key")
wake_key = os.environ.get("wake_key")
SECRET_KEY = '78w0o5tuuGex5Ktk8VvVDF9Pw3jv1MVE'
recaptcha_public_key = os.environ.get("recaptcha_public")
recaptcha_private_key = os.environ.get("recaptcha_private")
app.locked = False

app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']= recaptcha_public_key
app.config['RECAPTCHA_PRIVATE_KEY']= recaptcha_private_key
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}
def is_time_between(begin_time, end_time, weekday=None, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    print(check_time)
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time



def isAllowed():
    return (is_time_between(*dayTimes[datetime.now().weekday()]) and not app.locked) or (request.headers.get('api_key',"",type=str) == api_key)

def isNotBot(form):
    return (request.method == 'POST' and form.validate()) or request.headers.get('api_key',"",type=str) == api_key

class AllowedForm(Form):
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

class WakeForm(Form):
    def validate_code(form,field):
        if field.data != wake_key:
            raise validators.ValidationError("Wrong Key")
    key = StringField(u'Kode', validators=[validators.input_required(),validate_code])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html', projector_keys = projector_keys, soundbar_keys = soundbar_keys, sounds = sounds,dayTimes = dayTimes)

@app.route('/doorbell/<sound>', methods=['POST','GET'])
def vågnop(sound):
    form = WakeForm(request.form)   
    if isNotBot(form):
        with open('wakeuplog.txt', 'a') as log:
            log.write('Attempting to wake at {} with sound {} \n'.format(datetime.now(),sound))
        try:
            os.system("omxplayer --vol 800 -o local sounds/{}".format(sounds[sound]))
            return "Success"
        except:
            return "that not very poggies of you"

    return render_template('default.html', form=form, url='http://clown.mads.monster/doorbell/{}'.format(sound))

@app.route('/sounds/<sound>')
def play_sound(sound):
    if(not isAllowed()):
        return "Not now kiddo"
    
    try:
        os.system("omxplayer --vol 600 -o local sounds/{}".format(sounds[sound]))
        return "Success"
    except:
        return "that not very poggies of you"

@app.route('/lock', methods=['GET','POST'])
def lock():
    if (request.headers.get('api_key',"",type=str) == api_key):
        app.locked = not app.locked
    return "locked" if app.locked else "unlocked"


@app.route('/<device>/<key>', methods=['GET','POST'])
def projector_send_key(device,key):
    if(not isAllowed()):
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
    if(not isAllowed()):
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
    if(not isAllowed()):
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
    if(not isAllowed()):
        return "Not now kiddo"
    form = AllowedForm(request.form)
    if isNotBot(form):
        get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='state', value='TOGGLE')
        return "Success"
        
    return render_template('default.html', form=form, url='http://clown.mads.monster/Lys')

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 8000,debug = True)