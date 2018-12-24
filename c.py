#!/usr/bin/python3

import os
import sys
import time
import threading 
import logging
import imageio

class Camera:
    def __init__(self, iurl, iname, idir):
        '''Initialized variables:
        Url: image source
        Name: camera name
        Dir: directory for output
        '''
        self.url = iurl
        self.name = iname
        self.dir = os.path.join(idir, iname)

    def getImageEvery(self, period):
        while True:
            try:
                end_time = (time.time() // period + 1) * period
                while time.time() < end_time:
                    time.sleep(period / 60)
                image_dir = os.path.join(self.dir, 'imgs', str(int(time.time())) + '.jpg')
                image_file = imageio.imread(self.url)
                imageio.imwrite(image_dir, image_file)
                logging.debug("Image retrieved")
            except Exception:
                logging.exception("Failed to retrieve image")

    def startThread(self, threadTarget, *args, **kwargs):
        '''Runs a method in a separate thread
        Input: threadTarget, the method being started
        '''
        thread = threading.Thread(target=threadTarget, args=args, kwargs=kwargs)
        thread.start()
        logging.debug("Thread is waiting in background")


    def makeGif(self):
        images = []
        gif_dir = os.path.join(self.dir, 'gifs', str(int(time.time())) + '.gif')
        for file_name in sorted(os.listdir(image_directory)):
            print(file_name)
            if file_name.endswith('.jpg'):
               file_path = os.path.join(image_directory, file_name)
               images.append(imageio.imread(file_path))
        imageio.mimsave('/var/www/html/img/calcam.gif', images)
        logging.debug("Gif made")

#------------------ Main ----------------------#

logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
info = {'stop': False}
calcam = Camera('https://www.calvin.edu/img/calcam_large.jpg', 'calcam', '/var/www/html')
calcam.startThread(calcam.getImageEvery, 60)
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
