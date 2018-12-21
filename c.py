import requests
import shutil
import time
import threading 
import os


def getImage():
    url = "https://www.calvin.edu/img/calcam_large.jpg"
    response = requests.get(url, stream=True)
    current_time = time.strftime("%b%d-%H%M",time.gmtime())
    image_file = "img/calcam_large" + current_time + ".jpg"
    with open(image_file, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    print("Image retrieved")

def waitUntil(period=1):
    '''Waits until next minute
    '''
    end_time = (time.time() // 60 + 1) * 60
    while time.time() < end_time:
        time.sleep(period)
    return False

def startThread(threadTarget, *args, **kwargs):
    thread = threading.Thread(target=threadTarget, args=args, kwargs=kwargs)
    thread.start()
    print("Thread is waiting in background")

def makeGif():
    jpg_directory = '/img'
    images = []
    for file_name in os.listdir(jpg_directory):
        if file_name.endswith('.jpg'):
            file_path = os.path.join(jpg_directory, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave('/var/www/calcam.gif', images)

def imageLoop():
    count = 0
    while count < 4:
        getImage()
        startThread(waitUntil)
        count += 1

imageLoop()

