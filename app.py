import os
import requests
import keep_alive
from dotenv import load_dotenv
from flask import Flask, request, abort

# take environment variables from .env
load_dotenv()

# create Flask object called app
app = Flask(__name__)

@app.route('/')
def root():
    return 'Tradingview Discord Webhook Middleware service is online'


print(os.getenv('DISCORD_WEBHOOK'))
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # request.data contains the incoming request data as string in case it came with a mimetype Flask does not handle
        data = request.data.decode()
        payload = {"content": data}
        response = requests.post(os.getenv('DISCORD_WEBHOOK_URL'), json=payload)
        return data
    else:
        abort(400)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81)
