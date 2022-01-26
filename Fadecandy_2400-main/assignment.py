#!/usr/bin/env python

import opc
import time
from letters import *
import colorsys

client = opc.Client('localhost:7890') #connects code to LED emulator

led_colour=[(0,0,0)]*360 #sets a blank screen

def print_letters(text): #function to print input letters to the LED emulator
    global led_colour
    led_colour=[(0,0,0)]*360 #refreshes to black screen every time function is called
    n=round(29 - (len(text)*7-8)/2) #used to center the letters on the emulator
    for value in text:
        for point in value:
            
            pixel = 60*point[0] + point[1] + n

            r = 255
            g = 0
            b = 0

            new_colour = (r,g,b)
            led_colour[pixel] = new_colour

        n+=6

    client.put_pixels(led_colour) #prints LED pixels to emulator



def animation_choice(number):
    match number:
        case 1: #atuhor introduction
            print_letters([g,r,a])
            time.sleep(1)
            print_letters([i,x])
            time.sleep(1)
            print_letters([p,e,w,space,p,e,w])
            time.sleep(1)
            #creates a moving underline animation
            led = 60*5
            while led < 60*6:
                led_colour[led] = (255,0,0)
                client.put_pixels(led_colour)
                time.sleep(0.1)
                led +=1

        case 2: #prints user's name
            name = input("What is your name?")
            if len(name) < 10:
                print (len(name))
                time.sleep(1)
                chars = []
                for letter in name:
                    if letter.isalpha():
                        chars.append(globals()[letter])
                    else:
                        print("Name contains unrecognised characters")
                print(chars)
                time.sleep(1)
                print_letters(chars)
                time.sleep(1)

            else:
                print("Name is too long")
        case 3:
            return
        case 4:
            return
        case 5:
            return
        case _:
            print("Option not recognised")

animation_choice(2)
