#!/usr/bin/python3

import os
import sys
import time
import threading 
import logging
import imageio

class Giffer:
    def __init__(self, iname, idir):
        '''Initialized variables:
        Name: camera name
        Dir: directory of images
        '''
        self.name = iname
        self.dir = os.path.join(idir, iname)


    def startThread(self, threadTarget, *args, **kwargs):
        '''Runs a method in a separate thread
        Input: threadTarget, the method being started
        '''
        thread = threading.Thread(target=threadTarget, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        logging.debug("Thread is waiting in background")


    def makeGif(self, start_time, duration, frames_per_second=20, frames_per_hour=20):
        '''Make a gif from a range of images
        Start_time: time in y-m-d h:m:s format
        Duration: in hours
        '''
        images = []
        gif_path = os.path.join(self.dir, 'gif', 'calcam' + '.gif')
        image_list = os.listdir(os.path.join(self.dir, 'img'))
        image_list.sort()
        start_time = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) + 5 * 3600  # timezone?
        end_time = start_time + 3600 * duration
        start_image = str(start_time) + '.jpg'
        end_image = str(end_time) + '.jpg'
        logging.debug("Scanning images...")
        for image in image_list:
            if start_image <= image and image.endswith('.jpg'):
                start_image = image
                start_index = image_list.index(image)
                break
            else:
                continue
            logging.debug("Invalid start time, gif creation aborted...")
            return
        reverse_image_list = sorted(image_list, reverse=True)
        for image in reverse_image_list:
            if end_image >= image and image.endswith('.jpg'):
                end_image = image
                end_index = image_list.index(image)
                break
            else:
                continue
            logging.debug("Invalid end time, gif creation aborted...")
            return
        # actual start and end times
        start_time = int(start_image[:-4])
        end_time = int(end_image[:-4])
        actual_frames_per_hour =  60 / (float((end_time - start_time) / 60) / float(end_index + 1 - start_index)) # this give the right answer but i dont know why
        actual_frames_per_hour = round(actual_frames_per_hour)
        frame_multiplier = int(actual_frames_per_hour // frames_per_hour)
        if frame_multiplier < 1: frame_multiplier = 1
        logging.debug("FM: " + str(frame_multiplier))
        for index in range(start_index, end_index + 1):
            if index % frame_multiplier == 0:
                file_path = os.path.join(self.dir, 'img', image_list[index])
                images.append(imageio.imread(file_path))
        logging.debug("Creating gif...")
        imageio.mimsave(gif_path, images, fps=frames_per_second)
        logging.debug("Gif completed")

#------------------ Main ----------------------#

logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
calcam = Giffer('calcam', '/var/www/html')

from imgurpython import ImgurClient

client_id = '3d379e8763c3554'
client_secret = '7c421092f80c51565b0ff11ef72dbcd31807806f'
access_token = None #'0644ae187a3f4323ca5dd31b479fab4a3ddd4948'
refresh_token = 'c43d1d4bb46a13008934a9a4ae6b2adfdcf6e390'
client = ImgurClient(client_id, client_secret, access_token, refresh_token )
