#!/usr/bin/env python

import opc
import time
from letters import *
import colorsys
from random import randrange
from tkinter import *
import threading
import serial
import math

class StartStopAnimation:
    """docstring for animation_1"""
    def __init__(self):
        self._running = True
    def on(self):
        self._running = True
    def terminate(self):
        self._running = False

class Animation_1(StartStopAnimation):
    def run(self):
        while self._running:
            print_letters([g,r,a],255,0,0)
            if not self._running: break
            time.sleep(1)
            if not self._running: break
            print_letters([i,x],255,0,0)
            if not self._running: break
            time.sleep(1)
            if not self._running: break
            print_letters([p,e,w,space,p,e,w],255,0,0)
            if not self._running: break
            time.sleep(1)
            if not self._running: break
            #creates a moving underline animation
            draw_undreline((255,0,0),0.1)

class Animation_2(StartStopAnimation):
    """docstring for Animation_2"""
    def run(self):
        while self._running:
            name = input("What is your name?\n")
            if len(name) < 10: #check to see if name is too long
                chars = []
                for letter in name:
                    if letter.isalpha(): #check to see if only letters are inputted
                        chars.append(globals()[letter]) #set list with characters from input
                    else:
                        print("Name contains unrecognised characters")
                print_letters(chars,255,255,255)
                if not self._running: break
                time.sleep(0.5)
                draw_undreline((255,255,255),0.1)
                for x in range(360): #convert rgb to hsv
                    rgb = hsv_convert(x)
                    print(rgb) #debug
                    draw_undreline(rgb,0) #set colour to underline
                    if not self._running: break
                    time.sleep(0.1)
                break
            else:
                print("Name is too long")

class Animation_3(StartStopAnimation):
    """docstring for Animation_3"""
    def run(self):
        rain = [0]*360 #list of where o droplet can be
        while self._running:
            n=0
            for pixel in rain[0:60]: #decrease the count on each pixel on the first line every iteration
                if pixel > 0:
                    rain[n] -= 1
                n+=1
            rain_point = randrange(60) #get a randon point on the first line when a drop can emerge
            if rain[rain_point] == 0:
                drop = randrange(3,6) #get a random length for each droplet
                rain[rain_point] = drop
            time.sleep(1)
            n=0
            for pixel in rain: #assign colour to each pixel according to values in rain
                if pixel > 0:
                    led_colour[n] = (0,0,255)
                else:
                    led_colour[n] = (0,0,0)
                n+=1
            client.put_pixels(led_colour) #print pixels to emulator
            n=299
            for pixel in rain[300::-1]: #copy each drop of rain to the next line
                rain[n+60]=rain[n]
                n-=1

class Animation_4(StartStopAnimation):
    """docstring for Animation_4"""
    def run(self):
        arduino = serial.Serial('COM3', 9600)
        arduino.timeout = 0.1
        led_colour=[(0,0,0)]*360
        while self._running:
            b = arduino.readline()
            string_n = b.decode()
            string = string_n.rstrip()
            hue = float(string)
            print(hue)#debug
            rgb = hsv_convert(hue)
            for point in range(360):
                led_colour[point] = rgb
            client.put_pixels(led_colour) #print pixels to emulator
        arduino.close()

class Animation_5(StartStopAnimation):
    """docstring for Animation_5"""
    def run(self):
        led_colour=[(0,0,0)]*360
        user_car = [(2,57), (2,58), (2,59), (3,57), (3,58), (3,59)]
        count = 1
        bot_car_count = 0
        bot_cars = []
        s_count = 100
        speed = 5
        while self._running:
            client.put_pixels(led_colour)
            for p in user_car:
                print(p)
                position = p[0]*60+p[1]
                led_colour[position] = (0,0,255)
            if bot_car_count % 800 == 0:
                bot_cars.append(generate_bot_car())
            print(bot_car_count)
            print(bot_cars)
            for car in bot_cars:
                for z in car:
                    position = z[0]*60+z[1]
                    led_colour[position - 1] = (0,0,0)
                    led_colour[position] = (255,0,0)
            client.put_pixels(led_colour)
            if bot_car_count % 100 == 0:
                for car in enumerate(bot_cars):
                    if car[1][0][1] < 59:
                        for c in enumerate(car[1]):
                            bot_cars[car[0]][c[0]] = (c[1][0],c[1][1]+1)
                    else:
                        bot_cars.remove(car)
            
            bot_car_count += speed
            if count % 5000 == 0: speed += 5 #decrease time it takes for bot cars to move every 50 sec
            count +=1
            time.sleep(0.01) #response time to check for any imput


            #make loop time 0.1 or 0.01 sec and make cars more every 10 or 100 loops

#assign animation objects to variables    
animation_1 = Animation_1()
animation_2 = Animation_2()
animation_3 = Animation_3()
animation_4 = Animation_4()
animation_5 = Animation_5()

def click(number):
    animation_1.on()
    animation_2.on()
    animation_3.on()
    animation_4.on()
    animation_5.on()
    animation_choice(number)

def pop_up():
    global pop
    pop = Toplevel(window)
    pop.title("Enter name")
    pop.geometry("250x150")
    pop.config(bg = "black")
    pop_label = Label(pop, text = "Please enter your name", bg = "black", fg = "white")
    pop_label.pack(pady = 10)
    input_text = Text(pop, height = 1, width = 20)
    input_text.pack(pady = 10)


def stop_animation():
    animation_1.terminate()
    animation_2.terminate()
    animation_3.terminate()
    animation_4.terminate()
    animation_5.terminate()

def generate_bot_car():
    n = randrange(4)
    bot_car = [(n,3), (n,2), (n,1), (n+1,3), (n+1,2), (n+1,1)]
    return bot_car

def hsv_convert(hue):
    rgb_fractional = colorsys.hsv_to_rgb(hue/360.0, _s, _v) #get float between 1 and 0
    #assign floats to rgb variants
    r_float = rgb_fractional[0]
    g_float = rgb_fractional[1]
    b_float = rgb_fractional[2]
    return (r_float*255, g_float*255, b_float*255) #get tupple with real rgb vlues from variants

def print_letters(text,r,g,b): #function to print input letters to the LED emulator
    global led_colour
    led_colour=[(0,0,0)]*360 #refreshes to black screen every time function is called
    n=round(29 - (len(text)*7-8)/2) #used to center the letters on the emulator
    for value in text:
        for point in value:

            pixel = 60*point[0] + point[1] + n
            r = r
            g = g
            b = b

            new_colour = (r,g,b)
            led_colour[pixel] = new_colour

        n+=6

    client.put_pixels(led_colour) #prints LED pixels to emulator

def draw_undreline(colour,sleep_time): #function to draw an underline on the bottom line of the emulator
    led = 60*5 #used to ignore the first 5 lines
    while led < 60*6:
        led_colour[led] = colour #each pixel in line 6 is chosen
        print(led)
        client.put_pixels(led_colour) #colour is sent to the pixel
        if sleep_time > 0: 
            time.sleep(sleep_time)
        else:
            pass
        led +=1 #increase pixel number

nthrd = 0

def start_new_thread(func, *args):
    global nthrd
    print (nthrd)
    if not args:
        print('if')
        globals()['%sthrd' % nthrd] = threading.Thread(target = func).start()
    else:
        print('else')
        globals()['%sthrd' % nthrd] = threading.Thread(target = lambda: func(args[0])).start()
    nthrd += 1
    print (nthrd)


def animation_choice(number):
    match number:
        case 1: #atuhor introduction
            animation_1.run()

        case 2: #prints user's name
            animation_2.run()

        case 3: #creates a rain effect
            animation_3.run()
                
        case 4: #arduino potentiometer controld led hue
            animation_4.run()

        case 5:
            animation_5.run()
        case _:
            print("Option not recognised")

client = opc.Client('localhost:7890') #connects code to LED emulator
window = Tk()
window.title("LED animations")
window.configure(background = "black")
Label (window, text = "Which animation would you like to see?", bg = "black", fg = "white", font = "none 12") .pack(pady = 5)
button1 = Button(window, text = "1. Author's intro", width = 30, command = lambda: start_new_thread(click,1)) 
button1.pack(pady = 5)
button2 = Button(window, text = "2. Print your name", width = 30, command = lambda: start_new_thread(pop_up()))
#button2 = Button(window, text = "2. Print your name", width = 30, command = lambda: start_new_thread(click,2))
button2.pack(pady = 5)
button3 = Button(window, text = "3. Rain effect", width = 30, command = lambda: start_new_thread(click,3))
button3.pack(pady = 5)
button4 = Button(window, text = "4. Potentiometer hue control", width = 30, command = lambda: start_new_thread(click,4))
button4.pack(pady = 5)
button5 = Button(window, text = "5. Car game", width = 30, command = lambda: start_new_thread(click,5))
button5.pack(pady = 5)
button6 = Button(window, text = "Stop animation", width = 30, command = lambda: start_new_thread(stop_animation()))
button6.pack(pady = 5)
led_colour=[(0,0,0)]*360 #sets a blank screen
_s = 1.0 #used to set maximum colour to hsv chart
_v = 1.0 #used to set maximum brightness to hsv chart

window.mainloop()