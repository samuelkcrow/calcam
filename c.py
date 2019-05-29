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
                old_file_size = 0
                while True:
                    image_file = os.path.join(self.dir, 'img', str(int(time.time())) + '.jpg')
                    image_contents = imageio.imread(self.url)
                    imageio.imwrite(image_file, image_contents)
                    file_size = os.stat(image_file).st_size
                    if file_size == old_file_size:
                        break
                    else:
                        old_file_size = file_size
                        os.remove(image_file)
                logging.debug("Image retrieved")
            except Exception:
                logging.exception("Failed to retrieve image")

    def startThread(self, threadTarget, *args, **kwargs):
        '''Runs a method in a separate thread
        Input: threadTarget, the method being started
        '''
        thread = threading.Thread(target=threadTarget, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        logging.debug("Thread is waiting in background")


    def makeGif_fph(self, start_time, duration, frames_per_second=20, frames_per_hour=20):
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
        

    def makeGif_day(self, start_time, duration, frames_per_second=20):
        '''Make a gif from a range of images
        Start_time: time in y-m-d h:m:s format
        Duration: in days
        '''
        images = []
        gif_path = os.path.join(self.dir, 'gif', 'calcam' + '.gif')
        image_list = os.listdir(os.path.join(self.dir, 'img'))
        image_list.sort()
        start_time = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) + 5 * 3600  # timezone?
        start_image = str(start_time) + '.jpg'
        logging.debug("Scanning images...")
        for image in image_list:
            if start_image <= image and image.endswith('.jpg'):
                start_image = image
                index = image_list.index(image)
                break
            else:
                continue
            logging.debug("Invalid start time, gif creation aborted...")
            return
        for i in range(duration):
            file_path = os.path.join(self.dir, 'img', image_list[index])
            images.append(imageio.imread(file_path))
            index += 40
            file_path = os.path.join(self.dir, 'img', image_list[index])
            images.append(imageio.imread(file_path))
            index += 40
            file_path = os.path.join(self.dir, 'img', image_list[index])
            images.append(imageio.imread(file_path))
            index += 40
            file_path = os.path.join(self.dir, 'img', image_list[index])
            images.append(imageio.imread(file_path))
            index += 358

        logging.debug("Creating gif...")
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
calcam.makeGif_fph('2019-01-18 18:00:00',36,15,5)
# calcam.makeGif_day('2019-01-14 09:00:00',30,10)
