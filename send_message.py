import requests
from dotenv import load_dotenv
import os

from search_shopee import search_shopee_offers

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
MIN_DISCOUNT = 0.10


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


def is_good_deal(current_price, usual_price):
    if usual_price <= 0:
        return False
    discount = (usual_price - current_price) / usual_price
    return discount >= MIN_DISCOUNT


offers = search_shopee_offers("fone bluetooth", limit=1)
offer = offers[0]
message = format_offer(name=offer["name"], price=offer["price"], link=offer["link"])
status_code = send_telegram_message(text=message)
print(status_code)