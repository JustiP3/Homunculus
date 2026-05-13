import requests
from dotenv import load_dotenv
import os

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def send_alert(message):
    data = {
        "content": message
    }

    requests.post(WEBHOOK_URL, json=data)
