from pathlib import Path
from piexif import ExifIFD, ImageIFD, load, dump
from os import getenv
from PIL import Image

def add_value_to_metadata(image, idf, key, value):
    if not (exif := image.info.get("exif")):
        exif = dump(())

    exif = load(exif)
    exif[idf][key] = value.encode("utf-8")

    return exif


def get_face_without_name():
    for image_path in Path("/function/storage", getenv("FACES_MOUNT_POINT")).iterdir():
        with Image.open(image_path) as image:
            image.load()

        if not get_value_from_metadata(image, "Exif", ExifIFD.UserComment):
            return image_path.name


def get_face_by_tg_file_unique_id(file_unique_id):
    for image_path in Path("/function/storage", getenv("FACES_MOUNT_POINT")).iterdir():
        with Image.open(image_path) as image:
            image.load()

        if get_value_from_metadata(image, "0th", ImageIFD.DocumentName) == file_unique_id:
            return image_path.name


def get_originals_by_name(name):
    originals = []

    for image_path in Path("/function/storage", getenv("FACES_MOUNT_POINT")).iterdir():
        with Image.open(image_path) as image:
            image.load()

        if get_value_from_metadata(image, "Exif", ExifIFD.UserComment) == name:
            originals.append(get_value_from_metadata(image, "0th", ImageIFD.ImageDescription))

    return originals

def get_value_from_metadata(image, idf, key):
    if not (exif := image.info.get("exif")):
        return None

    exif = load(exif)
    value = exif[idf].get(key)

    if not value:
        return None

    return value.decode("utf-8")