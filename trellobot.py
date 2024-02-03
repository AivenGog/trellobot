#!/usr/bin/env python3

from config import *

import sys
import json
from datetime import datetime
import ipaddress
import logging

import requests
from flask import Flask, request, abort

logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(name="trellobot")
logger.info("Main module has started.")


def say(message):
    # Sending messages to telegram group by the bot
    # Enable LOGGING_LEVEL='DEBUG' to view the message
    message = message.replace("	", "")
    logger.info("Trying to send the message.")
    logger.debug(message)
    result = requests.post(
        url=f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": "true",
        },
        timeout=30,
    )

    if result.ok:
        logger.info("Message was successfully sent to telegram group.")
    else:
        logger.error("Could not send message to telegram.")


def create_card(action_data, member_name):
    logger.info(f"Starting a processing function: {sys._getframe(0).f_code.co_name}.")
    card_name = action_data["card"]["name"]
    card_url = f"https://trello.com/c/{action_data['card']['shortLink']}"
    list_name = action_data["list"]["name"]

    say(
        f"""🔥 {member_name} создал новую карточку!
    Статус: <b>{list_name}</b>

    <a href="{card_url}">{card_name}</a>"""
    )


def rename_card(action_data, member_name):
    logger.info(f"Starting a processing function: {sys._getframe(0).f_code.co_name}.")
    card_name_old = action_data["old"]["name"]
    card_name_new = action_data["card"]["name"]
    card_url = f"https://trello.com/c/{action_data['card']['shortLink']}"
    list_name = action_data["list"]["name"]

    say(
        f"""✏️ {member_name} переименовал карточку!
    Статус: <b>{list_name}</b>


    <i>{card_name_old}</i>

    -= 🔽 🔽 🔽 =-

    <a href="{card_url}">{card_name_new}</a>"""
    )


def transfer_card(action_data, member_name):
    logger.info(f"Starting a processing function: {sys._getframe(0).f_code.co_name}.")
    card_name = action_data["card"]["name"]
    card_url = f"https://trello.com/c/{action_data['card']['shortLink']}"
    list_name_old = action_data["listBefore"]["name"]
    list_name_new = action_data["listAfter"]["name"]

    say(
        f"""🔃 {member_name} поменял статус карточки!
    Название: <a href="{card_url}">{card_name}</a>

    <i>{list_name_old}</i> ➡️ ➡️ ➡️ <b>{list_name_new}</b>"""
    )


def close_card(action_data, member_name):
    logger.info(f"Starting a processing function: {sys._getframe(0).f_code.co_name}.")
    card_name = action_data["card"]["name"]
    list_name = action_data["list"]["name"]
    say(
        f"""🗑 {member_name} удалил карточку!
    Название: <b>{card_name}</b>
    Статус: <b>{list_name}</b>"""
    )


def new_comment(action_data, member_name):
    logger.info(f"Starting a processing function: {sys._getframe(0).f_code.co_name}.")
    card_name = action_data["card"]["name"]
    card_url = f"https://trello.com/c/{action_data['card']['shortLink']}"
    list_name = action_data["list"]["name"]
    comment_text = action_data["text"]

    say(
        f"""Название: <a href="{card_url}">{card_name}</a>
    Статус: <b>{list_name}</b>

    💬 Комментарий {member_name}: <i>{comment_text}</i>"""
    )


def new_attachment(action_data, member_name):
    logger.info(f"Starting a processing function: {sys._getframe(0).f_code.co_name}.")
    card_name = action_data["card"]["name"]
    card_url = f"https://trello.com/c/{action_data['card']['shortLink']}"
    list_name = action_data["list"]["name"]
    attachment_url = action_data["attachment"]["url"]

    say(
        f"""Название: <a href="{card_url}">{card_name}</a>
    Статус: <b>{list_name}</b>

    📎 <a href="{attachment_url}">Новое вложение</a> от {member_name}"""
    )


def due_time(action_data, member_name):
    logger.info(f"Starting a processing function: {sys._getframe(0).f_code.co_name}.")
    card_name = action_data["card"]["name"]
    card_url = f"https://trello.com/c/{action_data['card']['shortLink']}"
    list_name = action_data["list"]["name"]
    due = datetime.fromisoformat(action_data["card"]["due"])

    say(
        f"""Название: <a href="{card_url}">{card_name}</a>
    Статус: <b>{list_name}</b>

    ⏰ {member_name} выставил дедлайн: <i>{due.day}/{due.month}/{due.year} в {due.hour}:{due.minute}</i>"""
    )


def new_desc(action_data, member_name):
    logger.info(f"Starting a processing function: {sys._getframe(0).f_code.co_name}.")
    card_name = action_data["card"]["name"]
    card_url = f"https://trello.com/c/{action_data['card']['shortLink']}"
    list_name = action_data["list"]["name"]
    desc = action_data["card"]["desc"]

    say(
        f"""Название: <a href="{card_url}">{card_name}</a>
    Статус: <b>{list_name}</b>

    📝 {member_name} добавил описание: <i>{desc}</i>"""
    )


# processing json of an action on Trello board and calling appropriate function
def handler(action):
    action_type = action["type"]
    action_data = action["data"]
    member_name = action["memberCreator"]["fullName"]

    logger.info("Action handler has started.")
    logger.debug(f"Action: {action_type}")
    logger.debug(f"Member name: {member_name}")
    logger.debug(json.dumps(action_data, indent=2))

    if "old" not in action_data:
        action["data"]["old"] = {}

    if "card" not in action_data:
        logger.info("Received not a card action. Passing.")
        pass

    elif action_type == "commentCard":
        new_comment(action_data, member_name)

    elif action_type == "addAttachmentToCard":
        new_attachment(action_data, member_name)

    elif "listBefore" in action_data and "listAfter" in action_data:
        transfer_card(action_data, member_name)

    elif action_type == "updateCard" and "name" in action_data["old"]:
        rename_card(action_data, member_name)

    elif action_type == "createCard":
        create_card(action_data, member_name)

    elif "closed" in action_data["old"] and action_data["card"]["closed"]:
        close_card(action_data, member_name)

    elif "due" in action_data["card"]:
        try:
            due_time(action_data, member_name)
        except TypeError:
            logger.exception("Invalid due time. Passed without sending message.")
            pass

    elif "desc" in action_data["card"]:
        new_desc(action_data, member_name)

    else:
        logger.warning(
            f"Unknown action on Trello. Action type: {action_type}. To view json data set LOGGING_LEVEL='DEBUG'."
        )


# initialising Flask server to listen to Trello webhook's requests
app = Flask(__name__)


@app.route("/", methods=["POST", "HEAD"])
def webhook():
    if request.remote_addr != "127.0.0.1" and ipaddress.ip_address(
        request.remote_addr
    ) not in ipaddress.ip_network(
        # allow only Trello ips
        # https://developer.atlassian.com/cloud/trello/guides/rest-api/webhooks/#webhook-sources
        "104.192.142.240/28"
    ):
        logger.warning(
            f"New request from not white-listed ip: {request.remote_addr}. Aborted."
        )
        abort(403)

    if request.method == "HEAD":
        # needed for inital response when webhook is created
        logger.info("Received HEAD request. Returning code 200.")
        return {}, 200

    if request.method == "POST":
        logger.info(f"Received new action from Webhook. Passing to handler.")
        handler(request.json["action"])
    return {}, 200


logger.info("Starting Flask server!")
try:
    app.run(host="0.0.0.0", port=PORT)
except Exception:
    logger.exception("FATAL. Caught exception with server.")
    sys.exit(1)
