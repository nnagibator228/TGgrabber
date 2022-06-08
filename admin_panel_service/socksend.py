import socket
from secret_utils import *
from base64 import b64decode, b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5


class Sender:
    def __init__(self, hostname):
        self.hostname = hostname
        self.sock = socket.socket()
        self.ip = socket.gethostbyname(self.hostname)
        self.sock.connect((self.ip, 9090))
        f = open("/run/secrets/public_key", "rb")
        self.key = RSA.importKey(f.read())
        f.close()
        self.cipher = Cipher_PKCS1_v1_5.new(self.key)

    def send(self, mess):
        self.ip = socket.gethostbyname(self.hostname)
        self.sock.close()
        self.sock = socket.socket()
        self.sock.connect((self.ip, 9090))
        message = mess
        encr = self.cipher.encrypt(message.encode())
        self.sock.send(encr)
        return "сессия перезапущена"

