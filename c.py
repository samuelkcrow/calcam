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
                image_dir = os.path.join(self.dir, 'img', str(int(time.time())) + '.jpg')
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


    def makeGif(self, start_time, end_time, frames_per_second=20, frames_per_hour=20):
        '''Make a gif from a range of images
        start and end: time stamps in seconds
        '''
        images = []
        gif_path = os.path.join(self.dir, 'gif', 'calcam' + '.gif')
        image_list = os.listdir(os.path.join(self.dir, 'img'))
        image_list.sort()
        start_image = str(start_time) + '.jpg'
        end_image = str(end_time) + '.jpg'
        logging.debug("Scanning images...")
        for index in range(len(image_list)):
            if start_image <= image_list[index] and image_list[index].endswith('.jpg'):
                start_index = index
                break
            else:
                continue
            logging.debug("Invalid start time, gif creation aborted...")
            return
        for index in range(len(image_list)):
            reverse_image_list = sorted(image_list, reverse=True)
            if end_image >= reverse_image_list[index] and reverse_image_list[index].endswith('.jpg'):
                end_index = len(image_list) - index - 1
                break
            else:
                continue
            logging.debug("Invalid end time, gif creation aborted...")
            return
        logging.debug("Creating gif...")
        # actual start and end times
        start_time = int(image_list[start_index][:-4])
        end_time = int(image_list[end_index][:-4])
        actual_frames_per_hour = len(image_list) / (end_time - start_time)
        frame_multiplier = actual_frames_per_hour // frames_per_hour + 1
        for index in range(start_index, end_index + 1):
            if index % frame_multiplier == 0:
                file_path = os.path.join(self.dir, 'img', image_list[index])
                images.append(imageio.imread(file_path))
        imageio.mimsave(gif_path, images, fps=frames_per_second)
        logging.debug("Gif completed")

#------------------ Main ----------------------#

logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
calcam = Camera('https://www.calvin.edu/img/calcam_large.jpg', 'calcam', '/var/www/html')
'''calcam.startThread(calcam.getImageEvery, 180)
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
'''
calcam.makeGif(1546550000,1546580000,20,10)
