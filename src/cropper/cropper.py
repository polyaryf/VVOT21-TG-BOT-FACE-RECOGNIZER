from json import loads
from piexif import ImageIFD, dump
from os import getenv
from pathlib import Path
from uuid import uuid4
from requests import put
from time import sleep
from PIL import Image
from requests_aws4auth import AWS4Auth

def entrypoint(event, context):
    message = loads(event["messages"][0]["details"]["message"]["body"])

    object_key = message["object_key"]
    image = get_image(Path("/function/storage", getenv("PHOTOS_MOUNT_POINT"), object_key))

    x, y, w, h = message["rectangle"]
    face = image.crop((x, y, x + w, y + h))

    metadata = {
        "0th": {
            ImageIFD.ImageDescription: object_key.encode("utf-8")
        }
    }

    save_image(face, Path("/function/storage", getenv("FACES_MOUNT_POINT"), f"{uuid4()}.jpg"), exif=metadata)

    return {
        "statusCode": 200
    }

def get_image(image_path):
    with Image.open(image_path) as image:
        image.load()
    return image

def save_image(image, image_path, exif):
    image.save(image_path, exif=dump(exif))
    sleep(1)

    put(
        f"https://storage.yandexcloud.net/{getenv('FACES_MOUNT_POINT')}/{image_path.name}",
        headers = {
            "Content-Type": "image/jpeg",
            "X-Amz-Copy-Source": f"/{getenv('FACES_MOUNT_POINT')}/{image_path.name}",
            "X-Amz-Metadata-Directive": "REPLACE",
        },
        auth = AWS4Auth(getenv("ACCESS_KEY_ID"), getenv("SECRET_ACCESS_KEY"), "ru-central1", "s3")
    )