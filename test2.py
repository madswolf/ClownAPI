# Import the required module for text 
# to speech conversion
from gtts import gTTS
from io import BytesIO
  
import requests,re
line = str(requests.get("https://server.tobloef.com/experiments/poetry").content).replace("\\n", " ").replace("\\t","")
line = re.search(r"<p>([a-zA-Z \.]+)<\/p>",line)
# This module is imported so that we can 
# play the converted audio
import os
  
# The text that you want to convert to audio
  
# Language in which you want to convert
language = 'en'
  
# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
tts = gTTS(text=line.group(1), lang=language, slow=False)

fp = BytesIO()
tts.write_to_fp(fp)
fp.seek(0)
  
from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_file(fp, format="mp3")
play(song)
