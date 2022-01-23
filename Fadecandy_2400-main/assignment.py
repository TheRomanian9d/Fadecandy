#!/usr/bin/env python

import opc
import time
from letters import *

client = opc.Client('localhost:7890')

led_colour=[(0,0,0)]*360

def print_letters(*args):
    led_colour=[(0,0,0)]*360
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

client.put_pixels(led_colour)
#need to send it twice if not constantly sending values 
#due to interpolation setting on fadecandy
client.put_pixels(led_colour)
time.sleep(1)

def animation_choice(number):
    match status:
        case 1:
            print_letters(g,r,a)
            time.sleep(1)
            print_letters(i,x)
            time.sleep(1)
            print_letters(p,e,w,space,p,e,w)
        case 2:
            return
        case 3:
            return
        case 4:
            return
        case 5:
            return
        case _:
            print("Option not recognised")

print_letters(g,r,a)
time.sleep(1)
print_letters(i,x)
time.sleep(1)
print_letters(p,e,w,space,p,e,w)