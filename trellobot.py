#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from datetime import datetime
import json
import requests

from config import *


def say(my_message):
    """A imprortant feature for sending messages to telegram by a bot"""
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


def get_last_action():
    query = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
    action = requests.get(
        url=f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/actions",
        params=query,
        timeout=60,
    ).json()

    return action[0]


def create_card(action, member_name):
    card_name = action["card"]["name"]
    card_url = f"https://trello.com/c/{action['card']['shortLink']}"
    list_name = action["list"]["name"]

    say(
        f"""🔥 {member_name} создал новую карточку!
    Статус: <b>{list_name}</b>

    <a href="{card_url}">{card_name}</a>"""
    )


def rename_card(action, member_name):
    card_name_old = action["old"]["name"]
    card_name_new = action["card"]["name"]
    card_url = f"https://trello.com/c/{action['card']['shortLink']}"
    list_name = action["list"]["name"]

    say(
        f"""✏️ {member_name} переименовал карточку!
    Статус: <b>{list_name}</b>

    <i>{card_name_old}</i>

    -= 🔽 🔽 🔽 =-

    <a href="{card_url}">{card_name_new}</a>"""
    )


def transfer_card(action, member_name):
    card_name = action["card"]["name"]
    card_url = f"https://trello.com/c/{action['card']['shortLink']}"
    list_name_old = action["listBefore"]["name"]
    list_name_new = action["listAfter"]["name"]

    say(
        f"""🔃 {member_name} поменял статус карточки!
    Название: <a href="{card_url}">{card_name}</a>

    <i>{list_name_old}</i> ➡️ ➡️ ➡️ <b>{list_name_new}</b>"""
    )


def close_card(action, member_name):
    card_name = action["card"]["name"]
    list_name = action["list"]["name"]
    say(
        f"""🗑 {member_name} удалил карточку!
    Статус: <b>{list_name}</b>
    Название: <b>{card_name}</b>"""
    )


def new_comment(action, member_name):
    card_name = action["card"]["name"]
    card_url = f"https://trello.com/c/{action['card']['shortLink']}"
    list_name = action["list"]["name"]
    comment_text = action["text"]

    say(
        f"""Статус: <b>{list_name}</b>
    Название: <a href="{card_url}">{card_name}</a>

    💬 Комментарий {member_name}: <i>{comment_text}</i>"""
    )


def new_attachment(action, member_name):
    card_name = action["card"]["name"]
    card_url = f"https://trello.com/c/{action['card']['shortLink']}"
    list_name = action["list"]["name"]
    attachment_url = action["attachment"]["url"]

    say(
        f"""Статус: <b>{list_name}</b>
    Название: <a href="{card_url}">{card_name}</a>

    📎 <a href="{attachment_url}">Новое вложение</a> от {member_name}"""
    )


def due_time(action, member_name):
    card_name = action["card"]["name"]
    card_url = f"https://trello.com/c/{action['card']['shortLink']}"
    list_name = action["list"]["name"]
    due = datetime.fromisoformat(action["card"]["due"])

    say(
        f"""Статус: <b>{list_name}</b>
    Название: <a href="{card_url}">{card_name}</a>

    ⏰ {member_name} выставил дедлайн: <i>{due.day}/{due.month}/{due.year} в {due.hour}:{due.minute}</i>"""
    )


def new_desc(action, member_name):
    card_name = action["card"]["name"]
    card_url = f"https://trello.com/c/{action['card']['shortLink']}"
    list_name = action["list"]["name"]
    desc = action["card"]["desc"]

    say(
        f"""📍 Статус: <b>{list_name}</b>
    Название: <a href="{card_url}">{card_name}</a>

    📝 {member_name} добавил описание: <i>{desc}</i>"""
    )


# # # #


action_old = get_last_action()
if "old" not in action_old["data"]:
    action_old["data"]["old"] = {}

# # # # # # # # # # # #

print("[#] Trello bot started..")
print("Delay: " + str(DELAY) + " sec")

while True:
    # # # # # # # # # #
    while True:  # make error catching, retry request if error occurs
        try:
            action_new = get_last_action()
            break
        except (json.decoder.JSONDecodeError, requests.exceptions.RequestException):
            print("=== Exception caught!")
            print(traceback.format_exc())
            time.sleep(5)
    # # # # # # # # # #

    # # # # # # # # # #
    if "old" not in action_new["data"]:
        action_new["data"]["old"] = {}

    # # # # # # # # # # # #
    if action_old != action_new:
        action_type = action_new["type"]
        action_data = action_new["data"]
        member_name = action_new["memberCreator"]["fullName"]

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
                "❗ Новое событие на Trello.\nНо мне не удалось отобразить изменения.\n\nДополнительная инфомация была записана в unknown_events.log",
            )
            with open("unknown_events.log", "w", encoding="utf-8") as f:
                f.write("\n\n" + str(action_new))
        # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # .replace("<", "&lt;").replace(">", "&gt;") FOR AVOID "Bad Request: can't parse entities: Unsupported start tag \"module\" at byte offset 140"
    action_old = action_new
    time.sleep(DELAY)
