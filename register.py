import subprocess

from gcp_server import send_server
def register_self():
    ip = subprocess.getoutput("hostname -I").strip()
    data = {'ip': ip, 'type': "controller"}
    print(send_server('/register', data))

def get_devices():  
    print(send_server('/devices'))
