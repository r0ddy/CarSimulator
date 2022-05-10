import os
from dotenv import load_dotenv
import requests

load_dotenv("/home/ctrl/Desktop/CarSimulator/.env")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = "https://car-simulator-349213.uk.r.appspot.com"

def send_server(route, data={}):
    try:
        data['password'] = PASSWORD
        res = requests.post(BASE_URL + route, json=data)
        return res.json()
    except Exception as e:
        err = {"error": e}
        print(err)
