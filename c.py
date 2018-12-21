import requests
import shutil
import time
import threading 
import os


def getImage():
    url = "https://www.calvin.edu/img/calcam_large.jpg"
    response = requests.get(url, stream=True)
    current_time = time.strftime("%b%d-%H%M",time.gmtime())
    filename = "/var/www/img/calcam_large" + current_time + ".jpg"
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    print("Image retrieved")

def waitUntil(period=1):
    '''Waits until next minute
    '''
    end_time = (time.time() // 60 + 1) * 60
    while time.time() < end_time:
        time.sleep(period)
    getImage()
    return False

def startThread(threadTarget, *args, **kwargs):
    thread = threading.Thread(target=threadTarget, args=args, kwargs=kwargs)
    thread.start()
    print("Thread is waiting in background")

def makeGif():
    with imageio.get_writer('calcam.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

getImage()
startThread(waitUntil)


