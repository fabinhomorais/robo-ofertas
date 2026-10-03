import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def format_offer(name, price, link):
    formatted_price = f"{price:.2f}".replace(".", ",")
    return f"🔥 {name}\n💰 Por R$ {formatted_price}\n🛒 {link}"


def send_telegram_message(text):
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(URL, data=data)
    return response.status_code


product_name = "Fone de Ouvido Bluetooth"
product_price = 199.90
product_link = "https://exemplo.com/fone-bluetooth"
message = format_offer(name=product_name, price=product_price, link=product_link)

status_code = send_telegram_message(text=message)
print(status_code)