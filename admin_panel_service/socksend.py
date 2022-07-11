import requests
import json


class Sender:
    def __init__(self, hostname):
        self.url = "http://" + str(hostname) + ":5000/webhook"
        f = open("/run/secrets/rtoken", "rb")
        self.token = str(f.read())
        f.close()

    def send(self, mess):
        data = {
            'token': self.token,
            'method': mess
        }
        r = requests.post(self.url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        return "сессия перезапущена " + str(r.json())

