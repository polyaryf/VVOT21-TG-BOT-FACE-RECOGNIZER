import cv2
from pathlib import Path
from os import getenv
from json import dumps
from boto3 import client

def entrypoint(event, context):
    object_key = event["messages"][0]["details"]["object_id"]


