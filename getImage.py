

def getImage():
    url = "https://www.calvin.edu/img/calcam_large.jpg"
    response = requests.get(url, stream=True)
    current_time = time.strftime("%b%d-%H%M",time.gmtime())
    filename = "/var/www/img/calcam_large" + current_time + ".jpg"
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    print("Image retrieved")
