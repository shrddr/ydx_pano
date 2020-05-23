import requests
import os.path
import numpy as np
import cv2

def get_tile(loc,z,x,y):
    filename = f'cache/tiles/{loc}.{z}.{x}.{y}.jpg'
    if os.path.isfile(filename):
        return cv2.imread(filename)
    url = f'https://pano.maps.yandex.net/{loc}/{z}.{x}.{y}'
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)
    image = np.asarray(bytearray(r.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    if image is None:
        print(f"x{x}y{y} = NONE")
    return image


def get_pano(loc):
    filename = f'cache/{loc}.jpg'
    if os.path.isfile(filename):
        return cv2.imread(filename)
    TILESIZE = 256
    canvas = np.zeros((7*TILESIZE, 14*TILESIZE, 3), dtype='uint8')
    x = 0
    for ix in range(14):
        y = 0
        for iy in range(5):
            tile = get_tile(loc, 2, ix, iy)
            if tile is not None:
                sy, sx, _ = tile.shape
                canvas[y:y+sy,x:x+sx,:] = tile
                y += TILESIZE
        x += TILESIZE
    cv2.imwrite(filename, canvas)
    return canvas


if __name__ == "__main__":
    img = get_pano('eTHmtcFyYk2V')
    cv2.imshow('test', img)
    cv2.waitKey(0)