#!/usr/bin/env python

import opc
import time
from letters import *
import colorsys
from random import randrange

client = opc.Client('localhost:7890') #connects code to LED emulator

led_colour=[(0,0,0)]*360 #sets a blank screen
s = 1.0 #used to set maximum colour to hsv chart
v = 1.0 #used to set maximum brightness to hsv chart

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

def draw_undreline(colour,sleep_time): #function to draw an underline on the bottom line of the emulator
    led = 60*5 #used to ignore the first 5 lines
    while led < 60*6:
        led_colour[led] = colour #each pixel in line 6 is chosen
        client.put_pixels(led_colour) #colour is sent to the pixel
        time.sleep(sleep_time)
        led +=1 #increase pixel number



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
            draw_undreline((255,0,0),0.1)

        case 2: #prints user's name
            name = input("What is your name?\n")
            if len(name) < 10: #check to see if name is too long
                chars = []
                for letter in name:
                    if letter.isalpha(): #check to see if only letters are inputted
                        chars.append(globals()[letter]) #set list with characters from input
                    else:
                        print("Name contains unrecognised characters")
                print_letters(chars)
                time.sleep(1)
                draw_undreline((255,0,0),0.1)
                for hue in range(360): #convert rgb to hsv
                    rgb_fractional = colorsys.hsv_to_rgb(hue/360.0, s, v) #get float between 1 and 0
                    #assign floats to rgb variants
                    r_float = rgb_fractional[0]
                    g_float = rgb_fractional[1]
                    b_float = rgb_fractional[2]
                    rgb = (r_float*255, g_float*255, b_float*255) #get tupple with real rgb vlues from variants
                    print(rgb) #debug
                    draw_undreline(rgb,0) #set colour to underline
                    time.sleep(0.03) #set speed of hue transition
            else:
                print("Name is too long")
        case 3:
            rain = [0]*360
            print(rain) #debug
            while True:
                n=0
                for pixel in rain[0:60]:
                    if pixel > 0:
                        rain[n] -= 1
                    else:
                        pass
                    n+=1
                rain_point = randrange(60)
                print(rain_point) #debug
                if rain[rain_point] == 0:
                    drop = randrange(3,6)
                    print(drop) #debug
                    rain[rain_point] = drop
                #to do: print to led and do a loop where 1 is taken away from each value that is not 0
                else:
                    pass
                #to do: shift leds down
                #to do: print to led and do a loop where 1 is taken away from each value that is not 0
                time.sleep(1)
                print(rain) #-debug- check to see how random rain points get assigned
                #put line to print to emulator
                n=0
                for pixel in rain:
                    if pixel > 0:
                        led_colour[n] = (255,0,0)
                    else:
                        led_colour[n] = (0,0,0)
                    n+=1
                print(led_colour)
                print("--------------")
                client.put_pixels(led_colour)
                n=299
                for pixel in reversed(rain[0:300]):
                    rain[n+60]=rain[n]
                    n-=1    
                


        case 4:
            return
        case 5:
            return
        case _:
            print("Option not recognised")

choice = int(input("Which animation would you like to see?\n1. Author's intro\n2. Print your name\n3. Rain effect\n\ntype number:"))
animation_choice(choice)