import cv2
from pathlib import Path
from os import getenv
from json import dumps
from boto3 import client

def entrypoint(event, context):
    object_key = event["messages"][0]["details"]["object_id"]

    image_path = Path("/function/storage", getenv("MOUNT_POINT"), object_key)
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(f"{cv2.data.haarcascades}haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(image, 1.01, 4)


    for face in map(lambda val: list(map(int, val)), faces):
        client(
            service_name="sqs",
            endpoint_url="https://message-queue.api.cloud.yandex.net",
            region_name="ru-central1",
            aws_access_key_id=getenv("ACCESS_KEY_ID"),
            aws_secret_access_key=getenv("SECRET_ACCESS_KEY"),
        ).send_message(
            QueueUrl=getenv("QUEUE_URL"),
            MessageBody=dumps({"object_key": object_key, "rectangle": face})
        )

    return {"statusCode": 200}

