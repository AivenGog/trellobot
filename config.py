import os
from dotenv import load_dotenv
import logging

load_dotenv(".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")


WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # currently no HTTPS support
PORT = os.getenv("PORT")

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")
