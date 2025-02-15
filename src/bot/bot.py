from json import loads
from pathlib import Path
from os import getenv
from piexif import dump, ImageIFD, ExifIFD
from PIL import Image
from images import add_value_to_metadata, get_face_without_name, get_face_by_tg_file_unique_id, get_originals_by_name
from telegram import send_message, send_photo

def entrypoint(event, context):
    update = loads(event["body"])
    message = update.get("message")

    if message:
        handle_message(message)

    return { "statusCode": 200 }

def handle_message(message):
    if (text := message.get("text")) and text == "/start":
        pass

    elif text := message.get("text") and text == "/getface":
        object_key = get_face_without_name()
        if not object_key:
            send_message("Все фотографии подписаны в данный момент", message)
            return

        file_unique_id = send_photo(f"{getenv('API_GATEWAY_URL')}?face={object_key}", message, False)

        image_path = Path("/function/storage", getenv("FACES_MOUNT_POINT"), object_key)
        image = get_image(image_path)
        metadata = add_value_to_metadata(image, "0th", ImageIFD.DocumentName, file_unique_id)
        save_image(image, image_path, metadata)


    elif (text := message.get("text")) and (reply_message := message.get("reply_to_message", {})):
        file_unique_id = reply_message.get("photo", [{}])[-1].get("file_unique_id")
        if not file_unique_id:
            return

        object_key = get_face_by_tg_file_unique_id(file_unique_id)

        image_path = Path("/function/storage", getenv("FACES_MOUNT_POINT"), object_key)
        image = get_image(image_path)
        metadata = add_value_to_metadata(image, "Exif", ExifIFD.UserComment, text)
        save_image(image, image_path, metadata)

    elif (text := message.get("text")) and text.startswith("/find"):
        name = text[6:]

        originals = get_originals_by_name(name)
        if not originals:
            send_message(f"Фотографии с {name} не найдены", message)
            return

        for original in originals:
            image_path = Path("/function/storage", getenv("PHOTOS_MOUNT_POINT"), original)
            send_photo(image_path, message,True)

    else:
        send_message("Ошибка", message)

def get_image(image_path):
    with Image.open(image_path) as image:
        image.load()
    return image


def save_image(image, image_path, exif=()):
    image.save(image_path, exif=dump(exif))
