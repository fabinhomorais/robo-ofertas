import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
message = "Olá, sou o seu robô de ofertas!"

data = {
    "chat_id": CHAT_ID,
    "text": message
}
response = requests.post(URL, data=data)
print(response.status_code)