import socket
import subprocess
from secret_utils import *
from base64 import b64decode,b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
import os

sock = socket.socket()
f = open("/run/secrets/private_key", "rb")
key = RSA.importKey(f.read())
f.close()
cipher = Cipher_PKCS1_v1_5.new(key)
sock.bind(('', 9090))

while True:
    sock.listen(1)
    conn, addr = sock.accept()
    print('connected: ', addr)
    data = conn.recv(1024)
    error_mess = "error"
    decr = cipher.decrypt(data, error_mess)
    print(decr)
    if decr.decode("utf-8") == "restart":
        subprocess.run(['pkill', '-f', 'bot_grabber.py'])
        subprocess.Popen(['python3', '-u', 'bot_grabber.py'])
        print('Выполнен рестарт сессии')
    if decr == error_mess:
        print("Возникла ошибка декодирования")
