import os


def face_detection(face_client, single_face_image_url):
    if single_face_image_url == '':
        print("Error from noelshak...")
    single_image_name = os.path.basename(single_face_image_url)
    detected_faces = face_client.face.detect_with_url(url=single_face_image_url, recognition_model="recognition_02")
    if not detected_faces:
        #print("No detection")
        pass
    else:
        #print('Detected face ID from', single_image_name, ':')
        for face in detected_faces:
            print(face.face_id)

    return detected_faces


def similar_check(face_client, first_image_detection, second_image_detection):
    first_image = first_image_detection[0].face_id
    second_image = list(map(lambda x: x.face_id, second_image_detection))
    similar_faces = face_client.face.find_similar(face_id=first_image, face_ids=second_image)

    if len(similar_faces) == 0:
        print('No similar faces...')
        return -1

    print('\033[92m======>  Similar faces found!\033[0m')
    face_info = -1
    for face in similar_faces:
        first_image = face.face_id
        face_info = next(x for x in second_image_detection if x.face_id == first_image)
    return face_info
