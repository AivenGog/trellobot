from config import *

import time
from datetime import datetime
import json
import requests
from flask import Flask, request, json
import ipaddress


def say(my_message):
    # Sending messages to telegram group by the bot
    my_message = my_message.replace("	", "")
    result = requests.post(
        url=f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": my_message,
            "parse_mode": "HTML",
            "disable_web_page_preview": "true",
        },
        timeout=30,
    ).text
    return result


def create_card(action_data, member_name):
    card_name = action_data["card"]["name"]
    card_url = f"https://trello.com/c/{action_data['card']['shortLink']}"
    list_name = action_data["list"]["name"]

    say(
        f"""🔥 {member_name} создал новую карточку!
    Статус: <b>{list_name}</b>

    <a href="{card_url}">{card_name}</a>"""
    )


def rename_card(action_data, member_name):
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
    card_name = action_data["card"]["name"]
    list_name = action_data["list"]["name"]
    say(
        f"""🗑 {member_name} удалил карточку!
    Название: <b>{card_name}</b>
    Статус: <b>{list_name}</b>"""
    )


def new_comment(action_data, member_name):
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
    card_name = action_data["card"]["name"]
    card_url = f"https://trello.com/c/{action_data['card']['shortLink']}"
    list_name = action_data["list"]["name"]
    desc = action_data["card"]["desc"]

    say(
        f"""Название: <a href="{card_url}">{card_name}</a>
    Статус: <b>{list_name}</b>

    📝 {member_name} добавил описание: <i>{desc}</i>"""
    )


print("[#] Trello bot started..")


# processing json of an action on Trello board and calling appropriate function
def main(action):
    action_type = action["type"]
    action_data = action["data"]
    member_name = action["memberCreator"]["fullName"]

    if "old" not in action["data"]:
        action["data"]["old"] = {}

    if "card" not in action_data:
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
            pass

    elif "desc" in action_data["card"]:
        new_desc(action_data, member_name)

    else:
        print(
            "❗ Unknown action on Trello.\nAdditional info was stored in unknown_actions.log",
        )
        with open("unknown_actions.log", "w", encoding="utf-8") as f:
            f.write("\n\n" + str(action))


# starting Flask server to listen to Trello webhook's requests
app = Flask(__name__)


@app.route("/", methods=["POST", "HEAD"])
def webhook():
    if ipaddress.ip_address(request.remote_addr) not in ipaddress.ip_network(
        # allow only Trello ips
        # https://developer.atlassian.com/cloud/trello/guides/rest-api/webhooks/#webhook-sources
        "104.192.142.240/28"
    ):
        print(f"New request from not white-listed ip: {request.remote_addr}. Aborted")
        abort(403)

    if request.method == "HEAD":
        # needed for inital response when webhook is created
        return {}, 200

    if request.method == "POST":
        print(f"Received data from Webhook. Type: {request.json['action']['type']}")

        if SET_LOGGING:
            print("+++++++++++++++++++++++", request.json, "--------------------------")
            with open("actions.log", "w", encoding="utf-8") as f:
                f.write("\n\n" + str(request.json))

        main(request.json["action"])
    return {}, 200


app.run(host="0.0.0.0", port=PORT)
