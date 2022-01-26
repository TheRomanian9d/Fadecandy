#!/usr/bin/env python

import opc
import time
from letters import *

client = opc.Client('localhost:7890')

led_colour=[(0,0,0)]*360

def print_letters(*args):
    global led_colour
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



def animation_choice(number):
    match number:
        case 1: #atuhor introduction
            print_letters(g,r,a)
            time.sleep(1)
            print_letters(i,x)
            time.sleep(1)
            print_letters(p,e,w,space,p,e,w)
            time.sleep(1)
            #create a moving underline
            led = 60*5
            while led < 60*6:
                led_colour[led] = (255,0,0)
                client.put_pixels(led_colour)
                time.sleep(0.1)
                led +=1

        case 2: #prints user's name
            return
        case 3:
            return
        case 4:
            return
        case 5:
            return
        case _:
            print("Option not recognised")

animation_choice(1)
