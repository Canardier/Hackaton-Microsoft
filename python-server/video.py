import numpy as np
import cv2
import os
import threading
import queue
import time
from recoco import *
from detection import *

thread_nb = 25

def init_threads(threads, queues, detec1, client_l, res_list, count):
    for i in range(0, thread_nb):
        print("client: " + str(i))
        print(client_l[i % 5])
        
        threads.append(threading.Thread(target=th_fn, args=(queues[i], detec1, client_l[i % 5], res_list, count - i, i)))
        threads[i].start()

def wait_threads(threads):
    for	i in range(0, thread_nb):
        threads[i].join()
        
def init_queues(queues):
    for i in range(0, thread_nb):
        queues.append(queue.Queue())
        
def th_fn(queue, path1, face_client, res_list, count, th_nb):
    countframes = 0
    while not queue.empty():
        ret, frame = queue.get()
        print(count)

        if not ret:
            break
        
        if (countframes % 2) == 0:   
            resized = cv2.resize(frame, (720, 509))
            path2 = "./static/frame" + str(th_nb) + ".jpg"
            cv2.imwrite(path2, resized)
            
            try:
                compute(path1, path2, face_client, res_list, count, th_nb)
            except:
                pass
        countframes += 1
        count -= thread_nb
        
def videoFrame(path1, video, client_l):
    print("Setting recognition env")
    detec1 = face_detection(client_l[0], getImageUrl(path1))
    cap = cv2.VideoCapture(video)
    count = c2 = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    
    if not cap.isOpened():
        print('video not opened')
        return (-1)

    countframes = 0
    res_list = []
    queues = []
    threads = []
    init_queues(queues)
    print("Cutting video into frames")

    while count > int(c2) / 2:
        print(str(count) + " over " + str(c2 / 2))
        queues[int(count) % thread_nb].put(cap.read())
        count -= 1


    print("Starting face recognition")
    init_threads(threads, queues, detec1, client_l, res_list, c2)
    wait_threads(threads)    

    init_queues(queues)
    print("Cutting video into frames")

    c2 = count
    threads = []
    while count != 0:
        print(count)
        queues[int(count) % thread_nb].put(cap.read())
        count -= 1


    print("Starting face recognition")
    init_threads(threads, queues, path1, client_l, res_list, c2)
    wait_threads(threads)

    cap.release()
    cv2.destroyAllWindows()
    return res_list
