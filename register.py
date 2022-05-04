from cgitb import reset
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv("PASSWORD")

url = 'https://car-simulator-349213.uk.r.appspot.com/register'
ip = subprocess.getoutput("hostname -I").strip()
myobj = {'ip': ip, 'type': "controller", 'password': PASSWORD}

res = requests.post(url, json=myobj)
print(res.text)