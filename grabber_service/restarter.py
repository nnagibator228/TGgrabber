import subprocess

from flask import Flask, request, abort

flask1 = Flask(__name__)


@flask1.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        f = open("/run/secrets/rtoken", "rb")
        rtoken = str(f.read()).strip().rstrip()
        f.close()
        if data["token"] == rtoken and data["method"] == "restart":
            subprocess.run(['pkill', '-f', 'bot_grabber.py'])
            subprocess.Popen(['python3', '-u', 'bot_grabber.py'])
            return 'success', 200
        else:
            abort(403)
    else:
        abort(400)


if __name__ == "__main__":
    print("started.")
    flask1.run(host='0.0.0.0')
