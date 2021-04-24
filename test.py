import pyttsx3,requests,re
line = str(requests.get("https://server.tobloef.com/experiments/poetry").content).replace("\\n", " ").replace("\\t","")
line = re.search(r"<p>([a-zA-Z \.]+)<\/p>",line)
if line:
    print(line.group(1))


voiceEngine = pyttsx3.init()
voiceEngine.setProperty('rate',50)
voices = voiceEngine.getProperty('voices')
for voice in voices:
   voiceEngine.setProperty('voice', voice.id)
   voiceEngine.say('The quick brown fox jumped over the lazy dog.')
voiceEngine.say(line.group(1))
voiceEngine.runAndWait()