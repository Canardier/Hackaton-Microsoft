from detection import *
from get_url import *
from image import *
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import os

def auth():
    l = []
    k = []
    k.append("your-key")
    k.append("your-key")
    k.append("your-key")
    k.append("your-key")
    k.append("your-key")
    endpoint = "https://southcentralus.api.cognitive.microsoft.com/"

    for i in range(0, 5):
        l.append(FaceClient(endpoint, CognitiveServicesCredentials(k[i])))

    return l


def compute(detec1, path2, face_client, image_list, number, th_nb): 
    detec2 = face_detection(face_client, getImageUrl(path2))
    face_info = -1
    
    if len(detec1) == 0 or len(detec2) == 0:
        print("No face detected...")
        return -1

    face_info = similar_check(face_client, detec1, detec2)
    
    if face_info == -1:
        print("no matching face")
        return -1
    draw_rectangle(Image.open(path2), detec2, face_info, path2)
    res_name = r'./static/detected_' + str(th_nb) + "_" + str(number) + '.jpg'
    os.rename(r'./static/frame' + str(th_nb)  + '.jpg',res_name)    
    print('./static/detected_' + str(th_nb) + "_" + str(number) + '.jpg')
    image_list.append('detected_' + str(th_nb) + "_" + str(number) + '.jpg')
    return 0
