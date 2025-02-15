def entrypoint(event, context):
    update = loads(event["body"])
    message = update.get("message")

    if message:
        handle_message(message)

    return { "statusCode": 200 }

def handle_message(message):
    if (text := message.get("text")) and text == "/start":
        pass
