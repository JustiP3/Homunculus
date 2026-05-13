import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1502885789233844314/AmW3KK2l4A7jsOpq2SRKED-L-PfjHOm4vBhVKmLSS9wVLDO48-yPX8mjaEmLjwulr3iW"


data = {"content": "hello friend!"}

requests.post(WEBHOOK_URL, json=data)
