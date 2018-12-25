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


    def makeGif(self, start_time, end_time, framesPerSecond=15, picsPerHour=20):
        '''Make a gif from a range of images
        start and end: time stamps in seconds
        '''
        images = []
        gif_path = os.path.join(self.dir, 'gif', 'calcam' + '.gif')
        image_list = os.listdir(os.path.join(self.dir, 'imgs'))
        image_list.sort()
        start_image = str(start_time) + '.jpg'
        end_image = str(end_time) + '.jpg'
        for index in range(len(image_list)):
            if start_image <= image_list[index] and image_list[index].endswith('.jpg'):
                start_index = index
                break
            else:
                continue
            logging.debug("Invalid start time, gif creation aborted...")
            return
        for index in range(len(image_list)):
            logging.debug
            if end_image >= sorted(image_list, reverse=True)[index] and image_list[index].endswith('.jpg'):
                end_index = len(image_list) - index - 1
                break
            else:
                continue
            logging.debug("Invalid end time, gif creation aborted...")
            return
        for file_name in image_list[start_index:end_index]:
            file_path = os.path.join(self.dir, 'imgs', file_name)
            images.append(imageio.imread(file_path))
            logging.debug(file_name)
        imageio.mimsave(gif_path, images)
        logging.debug("Gif made")

#------------------ Main ----------------------#

logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
calcam = Camera('https://www.calvin.edu/img/calcam_large.jpg', 'calcam', '/var/www/html')
calcam.startThread(calcam.getImageEvery, 180)
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

#calcam.makeGif(1545639840,1545666340)
