from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = 'توکن ربات بلهت رو اینجا بذار'
API_URL = f"https://api.bale.ai/bot{TOKEN}"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        
        if 'photo' in message:
            requests.post(f"{API_URL}/sendMessage", json={
                "chat_id": chat_id,
                "text": "✅  دریافت شد. ممنون!"
            })
        elif 'video' in message:
            requests.post(f"{API_URL}/sendMessage", json={
                "chat_id": chat_id,
                "text": "🎥 ویدیو دریافت شد. ممنون!"
            })

    return 'ok'
