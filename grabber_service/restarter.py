import subprocess

from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        f = open("/run/secrets/rtoken", "rb")
        rtoken = str(f.read())
        f.close()
        if data["token"] == rtoken and data["method"] == "restart":
            subprocess.run(['pkill', '-f', 'bot_grabber.py'])
            subprocess.Popen(['python3', '-u', 'bot_grabber.py'])
            return 'success', 200
        else:
            abort(403)
    else:
        abort(400)
