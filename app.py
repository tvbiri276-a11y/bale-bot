from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "2119067640:Q8UDAuVI4VNkZ39aCG3dorkMuQaTWzW4HSe2Zklc"
ADMIN_ID = "mostafa_rivandi"
API_URL = f"https://tapi.bale.ai/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=data)

def send_file_to_admin(file_id, file_type, user_name):
    url = f"{API_URL}/send{file_type}"
    caption = f"📅 فایل از طرف: {user_name}\n\n🌐 www.tv7.ir\n📞 روابط عمومی: 162\n🟢 کانال‌ها: @amoozeshtv7"
    data = {
        "chat_id": ADMIN_ID,
        file_type.lower(): file_id,
        "caption": caption
    }
    requests.post(url, json=data)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "Bot is running!"

    data = request.get_json()
    print("Received data:", data)  # برای دیباگ تو لاگ‌ها

    message = data.get("message")
    if not message:
        return "no message"

    chat_id = message["chat"]["id"]
    first_name = message["from"].get("first_name", "")
    last_name = message["from"].get("last_name", "")
    full_name = f"{first_name} {last_name}".strip()

    if "text" in message and message["text"] == "/start":
        keyboard = {
            "keyboard": [
                [{"text": "📷 ارسال عکس"}, {"text": "🎥 ارسال فیلم"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
        send_message(chat_id, "لطفاً نوع فایلی که می‌خواهید ارسال کنید را انتخاب نمایید:", reply_markup=keyboard)
        return "ok"

    if "photo" in message:
        file_id = message["photo"][-1]["file_id"]
        send_file_to_admin(file_id, "Photo", full_name)
        send_message(chat_id, "✅ عکس شما دریافت شد.\n🌐 www.tv7.ir\n📞 روابط عمومی 162\n🟢 @amoozeshtv7")
        return "ok"

    if "video" in message:
        file_id = message["video"]["file_id"]
        send_file_to_admin(file_id, "Video", full_name)
        send_message(chat_id, "✅ ویدیوی شما دریافت شد.\n🌐 www.tv7.ir\n📞 روابط عمومی 162\n🟢 @amoozeshtv7")
        return "ok"

    send_message(chat_id, "لطفاً فقط عکس یا ویدیو ارسال نمایید.")
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)
