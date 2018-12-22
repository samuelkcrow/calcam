#!/usr/bin/python3

import requests
import shutil
import time
import threading 
import os
import imageio
import sys


def getImage():
    global image_count
    url = "https://www.calvin.edu/img/calcam_large.jpg"
    response = requests.get(url, stream=True)
    current_time = time.strftime("%b%d-%H%M", time.gmtime())
    image_directory = os.path.join(os.path.dirname(sys.argv[0]), 'img')
    image_file = os.path.join(image_directory, 'calcam_large' + current_time + ".jpg")
    with open(image_file, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    image_count += 1
    print("Image retrieved")

def doEvery(period, methodToCall):
    '''Calls a method every period
    Input: methodToCall, method
    '''
    try:
        while True:
            end_time = (time.time() // period + period / 60) * period
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
    jpg_directory = 'img'
    images = []
    for file_name in os.listdir(jpg_directory):
        if file_name.endswith('.jpg'):
           file_path = os.path.join(jpg_directory, file_name)
           images.append(imageio.imread(file_path))
    imageio.mimsave('/var/www/html/img/calcam.gif', images)
    print("Gif made")

#------------------ Main ----------------------#

image_count = 0
getImage()
startThread(doEvery, 60, getImage)
startThread(doEvery, 3600, makeGif)
print("Hey maybe we don't have to exit gracefully if we don't want to")
while True:
    time.sleep(10)

