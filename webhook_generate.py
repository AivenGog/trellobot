# The creation of webhook
# trellobot.py MUST BE RUNNING

import sys
from config import *
import requests
import logging

logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(name="webhook_generate")

logger.info("Module has started.")


def webhook_availability_check():
    logger.info("Checking if the webhook was already created.")
    found_webhooks = requests.get(
        url=f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks",
        params={"key": TRELLO_API_KEY, "token": TRELLO_TOKEN},
        timeout=60,
    ).json()

    if len(found_webhooks) == 0:
        logger.info("No existing webhooks were found. Creating new one.")
        return True

    logger.warning("The webhook was already created!")
    sys.exit(0)


def webhook_generate():
    logger.info("Trying to create webhook")

    board_id = requests.get(
        url=f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}",
        headers={"Accept": "application/json"},
        params={"key": TRELLO_API_KEY, "token": TRELLO_TOKEN},
        timeout=60,
    ).json()["id"]

    webhook_json_data = {
        "key": TRELLO_API_KEY,
        "description": "Trellobot webhook",
        "callbackURL": f"http://{WEBHOOK_URL}:{PORT}",
        "idModel": board_id,
    }

    logger.debug(str(webhook_json_data))

    webhook_request = requests.post(
        url=f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks/",
        json=webhook_json_data,
        timeout=60,
    )

    return webhook_request


if webhook_availability_check():
    webhook_request = webhook_generate()

if webhook_request.ok:
    logger.info(f"Webhook {webhook_request.json()['id']} was successfully created!")
    logger.debug(webhook_request.text)
else:
    logger.critical(
        "Creation of webhook was unsuccessful! Check if trellobot.py is running and your host is visible on web."
    )
    logger.error(webhook_request.json()["error"])
    logger.debug(webhook_request.text)
    sys.exit(1)
