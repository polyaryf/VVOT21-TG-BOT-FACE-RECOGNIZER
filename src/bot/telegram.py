from json import dumps
from os import getenv
from requests import post

def send_message(reply_text, input_message):
    url = f"https://api.telegram.org/bot{getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    data = {
        "chat_id": input_message["chat"]["id"],
        "text": reply_text,
        "reply_parameters": {
            "message_id": input_message["message_id"],
        },
    }

    post(url=url, json=data)


def send_photo(photo_url, input_message, is_original):
    url = f"https://api.telegram.org/bot{getenv('TELEGRAM_BOT_TOKEN')}/sendPhoto"

    data = {
        "chat_id": input_message["chat"]["id"],
        "photo": photo_url,
        "reply_parameters": {
            "message_id": input_message["message_id"]
        }
    }

    if is_original:
        del data["photo"]
        data["reply_parameters"] = dumps(data["reply_parameters"])
        response = post(url=url, data=data, files={"photo": open(photo_url, "rb")})
    else:
        response = post(url=url, json=data)

    return response.json()["result"]["photo"][-1]["file_unique_id"]