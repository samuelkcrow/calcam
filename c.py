#!/usr/bin/python3

import requests
import shutil
import time
import threading 
import os
import imageio
import sys


image_directory = os.path.join(os.path.dirname(sys.argv[0]), 'commons_lawn')
url = "https://www.calvin.edu/img/calcam_large.jpg"

def getImage():
    global image_count
    response = requests.get(url, stream=True)
    image_file = os.path.join(image_directory, str(int(time.time())) + ".jpg")
    with open(image_file, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    print("Image retrieved")

def doEvery(period, methodToCall):
    '''Calls a method every period
    Input: methodToCall, method
    '''
    try:
        while True:
            end_time = (time.time() // period + 1) * period
            while time.time() < end_time:
                time.sleep(period / 60)
            methodToCall()
    except (KeyboardInterrupt, SystemExit):
        cleanup_stop_thread()
        sys.exit()

def startThread(threadTarget, *args, **kwargs):
    '''Runs a method in a separate thread
    Input: threadTarget, the method being started
    '''
    thread = threading.Thread(target=threadTarget, args=args, kwargs=kwargs)
    thread.start()
    print("Thread is waiting in background")

def makeGif():
    images = []
    for file_name in sorted(os.listdir(image_directory)):
        print(file_name)
        if file_name.endswith('.jpg'):
           file_path = os.path.join(image_directory, file_name)
           images.append(imageio.imread(file_path))
    imageio.mimsave('/var/www/html/img/calcam.gif', images)
    print("Gif made")

#------------------ Main ----------------------#

getImage()
makeGif()
startThread(doEvery, 60, getImage)
startThread(doEvery, 300, makeGif)
print("Waiting...")
while True:
    time.sleep(10)

