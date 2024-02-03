#!/usr/bin/env python3

# deletes all webhooks on the token
# start if bot sends several same messages

from config import *

import sys
import requests
import logging

logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(name="delete_all_webhooks")
logger.info("Module has started.")

query = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
logger.debug(str(query))

webhooks_data = requests.get(
    url=f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks",
    params=query,
    timeout=60,
).json()


if len(webhooks_data) != 0:
    logger.info(f"Found {len(webhooks_data)} webhook on Token. Proceeding to deletion.")

    for webhook in webhooks_data:
        deletion_request = requests.delete(
            url=f"https://api.trello.com/1/webhooks/{webhook['id']}",
            params=query,
            timeout=60,
        )
        if deletion_request.ok:
            logger.info(f"Webhook {webhook['id']} was deleted.")
        else:
            logger.warning(f"Unable to delete webhook {webhook['id']}")

else:
    logger.warning("No webhooks were found on the Token.")
