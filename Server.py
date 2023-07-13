from flask import Flask, render_template,request
import lirc, requests
from platypush.context import get_plugin
from dotenv import load_dotenv
import os, time as realtime, random,re
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SubmitField, StringField,validators
from datetime import datetime, time, date
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from flask import Response
from flask import stream_with_context
import PIL
import random
import os
import requests
from PIL import Image, ImageEnhance, ImageFont, ImageDraw 
import io
import re
import uuid
import numpy as np
import subprocess
from flask_apscheduler import APScheduler
import pychromecast
from pychromecast.controllers.youtube import YouTubeController
from threading import Event
import signal
import pytz
from paho.mqtt import client as mqtt_client


load_dotenv()

def resetLock():
    app.locked = False
    app.unlocked = False
    
def signal_handler(x,y):
   shutdown.set()
    
shutdown = Event()
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
 
scheduler.add_job(id="Reset_lock", func=resetLock, trigger='interval', seconds=600)

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

smart_plugs = ["Preben","Amplifier"]

sounds = {
    "honk": "honk-sound.mp3",
    "bonk": "bonk.mp3",
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
    "tobi-git": "tobi_git.mp3",
    "AMOGUS.mp3":"AMOGUS.mp3",
}

doorbell_responses = [
    "Fuck you for ringing my doorbell",
    "Ring ring goes the bell",
    "is grinding on my last gear",
    "tik tok tik tok, i am gonna do something i am going to regret",
    "Somerewhere in the distance, a doorbell rings",
    "You rang the doorbell. You monster",
    "I will turn you into a convertible",
    "Seems kinda sus to ring my doorbell",
    "lets goooo, to your funeral after i track your ip and hack you"
]

dayTimes = {
    0 : (time(9,30),time(23,30),"Monday"),
    1 : (time(9,30),time(23,30),"Tuesday"),
    2 : (time(9,30),time(23,30),"Wednesday"),
    3 : (time(9,30),time(23,30),"Thursday"),
    4 : (time(9,30),time(23,30),"Friday"),
    5 : (time(11,00),time(00,00),"Saturday"),
    6 : (time(11,00),time(00,00),"Sunday"),
}

def getCurrentTime():
    zone = pytz.timezone("Europe/Copenhagen")
    return datetime.now(zone)

api_key = os.environ.get("api_key")
wake_key = os.environ.get("wake_key")

recaptcha_public_key = os.environ.get("recaptcha_public")
recaptcha_private_key = os.environ.get("recaptcha_private")

phone_hardware_address = os.environ.get("phone_hardware_address")
desktop_hardware_address = os.environ.get("desktop_hardware_address")
doorbell_ip = os.environ.get("doorbell_ip")
path_to_wakescript = os.environ.get("path_to_wakescript")

chromecast_name = os.environ.get("chromecast_name")

zigbee2mqtt_host = os.environ.get("zigbee2mqtt_host")
zigbee2mqtt_port = int(os.environ.get("zigbee2mqtt_port"))

zigbee2mqtt_client_id = os.environ.get("zigbee2mqtt_client_id")

app.locked = False
app.isUserHome = True
app.unlocked = False

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY_CSRF")
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']= recaptcha_public_key
app.config['RECAPTCHA_PRIVATE_KEY']= recaptcha_private_key
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}


def is_time_between(begin_time, end_time, weekday=None, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or getCurrentTime().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def playText(text):
    tts = gTTS(text=text, lang='en', slow=False)

    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    song = AudioSegment.from_file(fp, format="mp3")
    song = song + 35
    play(song)

def bearsApiKey():
    return request.headers.get('apiKey',"",type=str) == api_key

def unauthorized_response():
    return Response("Not very poggies of you", 403)

def isAllowed():
    if bearsApiKey():
        return (True,"")
    
    if app.unlocked:
        return (True, "App unlocked: clown away while it lasts")
    
    if app.locked:
        return (False, "App locked: Clowning break")
    
    if not is_time_between(*dayTimes[getCurrentTime().weekday()]):
        return (False, "Closed: Not now kiddo")

    if not app.isUserHome:
        return (False, "Not home: Annoy me when i get back")

    return (True,"Open")

def status():
    return isAllowed()[1]
    
def isNotBot(form):
    return (request.method == 'POST' and form.validate()) or request.headers.get('apiKey',"",type=str) == api_key

class AllowedForm(FlaskForm):
    recaptcha = RecaptchaField()

class SpeakForm(AllowedForm):
    def validate_message(form,field):
        if not re.match(r"^[a-zA-ZæøåÆØÅ0-9 ,'\¨\.!?]+$",field.data):
            raise validators.ValidationError("Invalid message")
    message = StringField(u'Message',validators=[validators.input_required(),validate_message,validators.Length(max=255)])

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

@app.route('/Home/True')
def arrive():
    if bearsApiKey():
        app.isUserHome = True
        return "success"
    else: 
        return unauthorized_response()
        
@app.route('/Home/False')
def leave():
    if bearsApiKey():
        app.isUserHome = False
        return "success"
    else: 
        return unauthorized_response()

@app.route('/')
def index():
    return render_template(
        'index.html', 
        projector_keys = projector_keys, 
        soundbar_keys = soundbar_keys, 
        sounds = sounds,
        dayTimes = dayTimes,
        status=status(),
        currentTime=getCurrentTime()
        )
    
def bell():
    try:
        requests.get('http://{}/5/on'.format(doorbell_ip))
        realtime.sleep(1)
        requests.get('http://{}/5/off'.format(doorbell_ip))
        return random.choice(doorbell_responses)
    except:
        requests.get('http://{}/5/off'.format(doorbell_ip))
        return unauthorized_response()

@app.route('/doorbell',methods=['POST','GET'])
def ring():
    return "No longer open"
    form = AllowedForm(request.form)   
    if isNotBot(form):
        return bell()
    isAllowedNow = isAllowed()
    if(not isAllowedNow[0]):
        return isAllowedNow[1]
    return render_template('default.html', form=form, url='http://clown.mads.monster/doorbell')

@app.route('/message',methods=['POST','GET'])
def speak():
    return "Closed until i get a speaker for the pi that isn't the chromecast"
    isAllowedNow = isAllowed()
    if(not isAllowedNow[0]):
        return isAllowedNow[1]
    form = SpeakForm(request.form)

    if(isNotBot(form)):
        playText(form.message.data)
        return "success {}".format(form.message.data)
    return render_template('default.html', form=form, url='http://clown.mads.monster/message')
 
@app.route('/Wake/Desktop')
def WakeDesktop():
    if bearsApiKey():
        subprocess.run(path_to_wakescript)
        return "Package sent"
    else:
        return unauthorized_response()
    
@app.route('/poetry',methods=['POST','GET'])
def poetically_speak():
    return "Closed until i get a speaker for the pi that isn't the chromecast"
    isAllowedNow = isAllowed()
    if(not isAllowedNow[0]):
        return isAllowedNow[1]
    form = AllowedForm(request.form)   

    if not isNotBot(form):
        response = requests.get("https://server.tobloef.com/experiments/poetry")
        line = str(response.content).replace("\\n", " ").replace("\\t","")
        line = re.search(r"<p>([a-zA-Z \.]+)<\/p>",line)
        playText(line.group(1))
        return response.content
    return render_template('default.html', form=form, url='http://clown.mads.monster/poetry')

@app.route('/sounds/<sound>')
def play_sound(sound):
    isAllowedNow = isAllowed()
    if(not isAllowedNow[0]):
        return isAllowedNow[1]
    try:
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[chromecast_name])
        cast = chromecasts[0]
        cast.wait()
        mc = cast.media_controller
        mc.play_media("https://media.clown.mads.monster/{}".format(sounds[sound]), content_type = "audio/mpeg")
        mc.block_until_active()
        mc.play()
        return "Success"
    except:
        return unauthorized_response()
    
@app.route('/plugs/toggle/<plug>')
def toggle_plug(plug):
    if (not bearsApiKey()):
         return unauthorized_response()
    try:
        client = connect_mqtt()
        if(plug not in smart_plugs):
            return f"plug: {plug} not in list "
        topic = f"zigbee2mqtt/{plug}/set"
        msg = "{ \"state\": \"TOGGLE\" }"
        result = client.publish(topic,msg)
        if result[0] == 0:
            print(f"Send `{msg}` to topic `{topic}`")
            return Response("Success",200)
        else:
            print(f"Failed to send message to topic {topic}")
            return Response("Some sort of error with zigbee2mqtt", 500)
    except:
        return Response("Some sort of error with zigbee2mqtt", 500)


@app.route('/lock', methods=['GET','POST'])
def lock():
    if (bearsApiKey()):
        app.locked = not app.locked
    return "locked" if app.locked else "unlocked"

@app.route('/unlock', methods=['GET','POST'])
def unlock():
    if (bearsApiKey()):
        app.unlocked = not app.unlocked
    return "unlocked" if app.unlocked else "locked"
    
@app.route('/ir/<device>/<key>', methods=['GET','POST'])
def projector_send_key(device,key):
    isAllowedNow = isAllowed()
    if(not isAllowedNow[0]):
        return isAllowedNow[1]

    form = AllowedForm(request.form)
    if isNotBot(form):
        device = device.lower()
        key = key.lower()
        if(device in ir_devices.keys()):
            commands,remote = ir_devices[device]
            if(key in commands.keys()):
                client.send_once(remote,commands[key],repeat_count=0)
            return "Success"    
        return unauthorized_response()

    return render_template('default.html', form=form, url='http://clown.mads.monster/ir/{}/{}'.format(device,key))

@app.route('/Lys/brightness/<value>', methods=['GET','POST'])
def lys_set(value):
    isAllowedNow = isAllowed()
    if(not isAllowedNow[0]):
        return isAllowedNow[1]

    form = AllowedForm(request.form)
    if isNotBot(form):
        try:
            value = int(value)
            get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='brightness', value=str(value))
            return "Success"
        except Exception as e: 
            return unauthorized_response()

    return render_template('default.html', form=form, url='http://clown.mads.monster/Lys/brightness/{}'.format(value))

@app.route('/Lys/brightness/step/<value>', methods=['GET','POST'])
def lys_step(value):
    isAllowedNow = isAllowed()
    if(not isAllowedNow[0]):
        return isAllowedNow[1]

    form = AllowedForm(request.form)
    if isNotBot(form):
        try:
            value = int(value)
            get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='brightness_move', value=str(value))
            return "Success"
        except:
            return unauthorized_response()

    return render_template('default.html', form=form, url='http://clown.mads.monster/Lys/brightness/step/{}'.format(value))

@app.route('/Lys', methods=['GET','POST'])
def lys_():
    isAllowedNow = isAllowed()
    if(not isAllowedNow[0]):
        return isAllowedNow[1]
    form = AllowedForm(request.form)
    if isNotBot(form):
        get_plugin('zigbee.mqtt').group_set(group='stue-lys', property='state', value='TOGGLE')
        return "Success"
        
    return render_template('default.html', form=form, url='http://clown.mads.monster/Lys')

#shamelessly stolen from julian
def split_line(text, font, width):
    returntext = ""
    while text:
        if (font.getsize(text)[0]) < width:
            returntext += text
            break
        for i in range(len(text), 0, -1):
            if (font.getsize(text[:i])[0]) < width:
                if ' ' not in text[:i]:
                    returntext += text[:i] + "-\n"
                    text = text[i:]
                else:
                    for l in range(i, 0, -1):
                        if text[l] == ' ':
                            returntext += text[:l]
                            returntext += "\n"
                            text = text[l + 1:]
                            break
                break
    if len(returntext) > 3 and returntext[-3] == "-":
        returntext = returntext[:-3]
    return returntext

def get_margins(text, font, max_size, drawer):
    text = split_line(text,font,max_size[0])
    width_margin = round((max_size[0] - drawer.textsize(text, font)[0]) / 2)
    height_margin = round((max_size[1] - drawer.textsize(text, font)[1]) / 2)
    return width_margin, height_margin

def draw_text(text,font,pos,max_size,drawer):
        margins = list(get_margins(text,font,max_size,drawer))

        pos = (pos[0] + margins[0],pos[1] + margins[1])        
        drawer.text((pos[0]-1, pos[1]), text, font=font, fill=(0,0,0))
        drawer.text((pos[0]+1, pos[1]), text, font=font, fill=(0,0,0))
        drawer.text((pos[0], pos[1]-1), text, font=font, fill=(0,0,0))
        drawer.text((pos[0], pos[1]+1), text, font=font, fill=(0,0,0))
        drawer.text((pos[0],pos[1]),text,(255,255,255),font=font)

def openImageFromUrl(url):
    response = requests.get(url)
    return Image.open(io.BytesIO(response.content)) 

CC_COLORS = (
    (240, 240, 240), # white, 0
    (242, 178, 51),  # orange, 1
    (229, 127, 216), # magenta, 2
    (153, 178, 242), # lightBlue, 3
    (222, 222, 108), # yellow, 4
    (127, 204, 25),  # lime, 5
    (242, 178, 204), # pink, 6
    (76, 76, 76),    # gray, 7
    (153, 153, 153), # lightGray, 8
    (76, 153, 178),  # cyan, 9
    (178, 102, 229), # purple, a
    (51, 102, 204),  # blue, b
    (127, 102, 76),  # brown, c
    (87, 166, 78),   # green, d
    (204, 76, 76),   # red, e
    (25, 25, 25)     # black, f
)

def _quantize_with_colors(image, colors, dither=0):
    pal_im = Image.new("P", (1, 1))
    color_vals = []
    for color in colors:
        for val in color:
            color_vals.append(val)
    color_vals = tuple(color_vals)
    pal_im.putpalette(color_vals + colors[-1] * (256 - len(colors)))
    image = image.convert(mode="RGB")
    return image.quantize(palette=pal_im,dither=dither)

def img_to_nfp(im, new_size=None, dither=0):
    if new_size:
        im = im.resize(new_size)
    # A technique called image quantization is used to reduce the input image's
    # color palette to only the 16 ComputerCraft colors.
    im = _quantize_with_colors(im, CC_COLORS, dither)
    # After quantize, im is mode "P" (palletized), so im.getdata() returns a
    # sequence of ints representing indexes into the image's 16-color palette
    # from 0-15 (hex 0-f) for each pixel in the image. This is flattened, so
    # the values for image line two immediately follow image line one's values.
    # We use np.reshape() to turn it into a 2D numpy array whose values can be
    # accessed through arr[row][col] notation.
    data = im.getdata()
    width, height = im.size
    data_2d = np.reshape(np.array(data), (height, width))
    # convert from np array back to list for faster iteration
    data_2d = data_2d.tolist()
    nfp_im = ""
    for row in range(height):
        for col in range(width):
            # convert 0-15 decimal value to hex string (0-f)
            nfp_im += format(data_2d[row][col], "x")
        if row != len(data_2d) - 1:
            nfp_im += "\n"
    return nfp_im

@app.route('/memenfp',methods=['GET'])
def memenfp():
    # Endpoint that preprocesses an image for the ComputerCraft monitor, 
    # so that memes from mads.monster can be displayed in minecraft
    resp = requests.get(f"https://api.mads.monster/random/meme/").json()
    img = (openImageFromUrl(resp["visual"])).convert('RGB')

    drawer = ImageDraw.Draw(img)
    font = ImageFont.truetype("impact.ttf", 70)
    draw_text(resp["toptext"], font, (0, 25), (400, 50), drawer)
    draw_text(resp["bottomtext"], font, (0, 325), (400, 50), drawer)
    nfp = img_to_nfp(img,(164,81))
    return nfp

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 8000,debug = True)
