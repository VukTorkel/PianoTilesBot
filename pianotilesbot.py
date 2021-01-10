#!/usr/bin/env python3

# ppadb: pure python android debug bridge
from ppadb.client import Client
from PIL import Image
# Multiple Screen Shots: fast screenshots
import mss
import numpy as np
import time


adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no devices attaced')
    quit()

device = devices[0]

sct = mss.mss()

# coordinates for the different measuring points
# from top to which y coordinate it should work on
pixels_from_top = 700
# height and with of the snippet
width = 1
height = 20
# form left given the whole screen width
pixels_from_left = 470
row_width = int(pixels_from_left/4)
row_middle = int(row_width/2)
screens = [
    {'left': 0*row_width+row_middle, 'top': pixels_from_top, 'width': width, 'height': height}, 
    {'left': 1*row_width+row_middle, 'top': pixels_from_top, 'width': width, 'height': height}, 
    {'left': 2*row_width+row_middle, 'top': pixels_from_top, 'width': width, 'height': height}, 
    {'left': 3*row_width+row_middle, 'top': pixels_from_top, 'width': width, 'height': height},
]

phone_row_width = int(1080/4)
phone_row_middle = int(phone_row_width/2)

'''
    How to time code:
        startTim1 = time.time()
        elapsedTim1 = time.time() - startTim1
        print('finished in {} ms'.format(elapsedTim1))
'''

'''
    Getting the pixels data from the screen is possible with two options:
    1. with 'ppadb screencap' (directly from phone via adb, but slow: 0.6 - 2.2 ms)
    2. with 'scrcpy' for capturing the phone screen and 'mss' to then take the screenshot(s)
        (not directly from phone, but fast: ~0.06 ms (for 4 separate pictures))
'''


# for debugging so one can see the captured data
filename = 'C:/Users/renez/Desktop/pianotilesbot/fullscreen'

# wait to start!
input('')
print('GO!')



while True:
    # create screenshot for each row and save it into a numpy-arry
    snippets = []
    for i in range(4):
        # grab snaps the screenshot
        snippet = sct.grab(screens[i])
        # originaly we get 20 * 1 pixels width a depth of 4 (RGBA)
        # we reshape to 20,4 and cut the aplha value
        snippets.append(np.array(snippet).reshape(20,4)[:,:3])
        mss.tools.to_png(snippet.rgb, snippet.size, output=filename+str(i)+'.png')
    
    # list to array
    snippets = np.array(snippets)
    
    for row in range(4):
        for pixel in snippets[row]:
            # sum takes parameter axis
            # check if a pixel is black and if so tap it
            if(pixel.sum(0) == 0):
                device.shell(f'input touchscreen tap {row*phone_row_width+phone_row_middle} 1650')
                print(f'row {row} pressed')
                time.sleep(0.4)


 
