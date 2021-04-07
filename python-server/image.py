import requests
from PIL import Image, ImageDraw
from io import BytesIO


def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def get_rectangle(face_dictionary):
    rect = face_dictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height

    return (left, top), (right, bottom)


def draw_rectangle(img, detected_faces, face_info, path2):
    draw = ImageDraw.Draw(img)
    for face in detected_faces:
        draw.rectangle(get_rectangle(face_info), outline='red')
    img.save(path2)
