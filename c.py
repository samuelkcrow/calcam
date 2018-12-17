import requests
import shutil
import time


def getImage():
    url = "https://www.calvin.edu/img/calcam_large.jpg"
    response = requests.get(url, stream=True)
    filename = "calcam_large" + str(int(time.time())) + ".jpg"
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

while True:
    print("Another one")
    getImage()
    time.sleep(59)

