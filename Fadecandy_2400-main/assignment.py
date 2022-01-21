#!/usr/bin/env python

import opc
import time
from letters import *

led_colour=[(0,0,0)]*360

client = opc.Client('localhost:7890')

def print_letters(*args):
    n=round(29 - (len(args)*7-8)/2)
    for value in args:
        for point in value:
            
            pixel = 60*point[0] + point[1] + n

            r = 255
            g = 0
            b = 0

            new_colour = (r,g,b)
            led_colour[pixel] = new_colour

        n+=6

    client.put_pixels(led_colour)
    client.put_pixels(led_colour)

"""print (enumerate(led_colour))
for item in enumerate(led_colour):
    time.sleep(1)
    print (item)
    if item[0]%2 == 0:
        #need to get values out of tuple
        r, g, b = item[1]
        print('R', r, 'G', g, 'B:',b)
        r = r-120
        g = 255
        b = 255
        
        #create changed tuple (uses some values from old and some new) 
        new_colour =(r,g,b)
        led_colour[item[0]] = new_colour
        print(new_colour)
        
    client.put_pixels(led_colour)
    client.put_pixels(led_colour)
"""
client.put_pixels(led_colour)
#need to send it twice if not constantly sending values 
#due to interpolation setting on fadecandy
client.put_pixels(led_colour)
print (led_colour)
time.sleep(1)


print_letters(g,r,a)