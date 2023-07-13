# Script for when the home pc shuts down
import os,sys
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("api_key")
smart_host = os.environ.get("smart_host")

url = "https://" + smart_host + "/plugs/toggle/Amplifier"
headers = { "apiKey" : api_key }

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.content)

if(response.status_code != 200):
    sys.exit(1)
