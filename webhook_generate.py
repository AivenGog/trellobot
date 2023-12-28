from config import *
import requests

board_id = requests.get(
    url=f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}",
    headers={"Accept": "application/json"},
    params={"key": TRELLO_API_KEY, "token": TRELLO_TOKEN},
    timeout=60,
).json()["id"]


json_data = {
    "key": TRELLO_API_KEY,
    "description": "Trellobot webhook",
    "callbackURL": f"http://{WEBHOOK_URL}:{PORT}",
    "idModel": board_id,
}

req = requests.post(
    url=f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks/",
    json=json_data,
    timeout=60,
)


print(req.json())

with open("webhook_json.log", "w", encoding="utf-8") as f:
    f.write(str(req.json()))
