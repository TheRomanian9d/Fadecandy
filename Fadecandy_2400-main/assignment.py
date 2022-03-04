#!/usr/bin/env python

import opc
import time
from letters import *
import colorsys
from random import randrange
from tkinter import *
import tkinter.messagebox
import threading
import serial
import math

class StartStopAnimation: #object for starting and stopping the animation (to be inherited by Animation_n objects)
    """docstring for animation_1"""
    def __init__(self):
        self._running = True
    def on(self): #starts animation
        self._running = True
    def terminate(self): #stops animation
        self._running = False

class Animation_1(StartStopAnimation):
    """creates an animation which introduces the author""" 
    def run(self):
        while self._running:
            if not self._running: break #break loop if self._running is false
            print_letters([i],255,0,0) #call print_letters() function with given parameters
            time.sleep(1) #sleep 1 second
            if not self._running: break
            print_letters([a,m],255,0,0)
            time.sleep(1)
            if not self._running: break
            print_letters([g,r,a],255,0,0)
            time.sleep(1)
            if not self._running: break
            print_letters([a,k,a],255,0,0)
            time.sleep(1)
            if not self._running: break
            print_letters([i,x],255,0,0)
            time.sleep(1)
            if not self._running: break
            print_letters([p,e,w,space,p,e,w],255,0,0)
            time.sleep(1)
            if not self._running: break
            print_letters([w,e,l,c,o,m,e],255,0,0)
            time.sleep(1)
            if not self._running: break
            draw_undreline((255,0,0),0.1) #creates a moving underline animation using draw_underline() function

class Animation_2(StartStopAnimation):
    """creates an animation which asks the user for their name and greets them"""
    def run(self):
        while self._running:
            name = input_text.get(1.0, "end-1c").lower() #uses get() function to read what is stored in input_text and assign it to variable
            if len(name) < 10: #check to see if name is too long
                chars = []
                for letter in name: #runs through each character storen in variable
                    if letter.isalpha(): #check to see if only letters are inputted
                        chars.append(globals()[letter]) #set list with characters from input
                    else:
                        tkinter.messagebox.showerror(title = "Error", message = "Name contains unrecognised characters") #creates an error popup if unrecognised characters are inputted
                        stop_animation() #stops animation
                        break #breaks loop
                for n in range(5):
                    #prints hello to emulator 5 times in random colours
                    print_letters([h,e,l,l,o],randrange(255),randrange(255),randrange(255))
                    if not self._running: break
                    time.sleep(0.5)
                print_letters(chars,255,255,255) #prints inputted name to emulator
                if not self._running: break
                time.sleep(0.5)
                draw_undreline((255,255,255),0.1)
                for x in range(360):
                    #get rgb equivalent for 360 hues
                    rgb = hsv_convert(x)
                    for n in range(300, 360): #choose pixels for bottom line
                        led_colour[n] = rgb #make pixel colour equal to hue
                    client.put_pixels(led_colour)
                    if not self._running: break
                    time.sleep(0.01)
                break
            else:
                tkinter.messagebox.showerror(title = "Error", message = "Name is too long") #show error message box if inputted name is too long
                break

class Animation_3(StartStopAnimation):
    """creates an animation of rain dropplets of random length of 3-5 to appear at random positions and drop down the screen"""
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
    """creates an animation where the hue of the pixels can be controlled using a potentiometer on an arduino using serial communication"""
    def run(self):
        arduino = serial.Serial('COM3', 9600) #connect to arduino through serial communication on port COM3
        arduino.timeout = 1 #set timeout for arduino connection
        led_colour=[(0,0,0)]*360 #set blank screen
        while self._running:
            b = arduino.readline() #read a byte from arduino via serial communication
            string_n = b.decode() #convert byte string to unicode string
            string = string_n.rstrip() #removes /r/n from string
            hue = float(string) #convert string to float
            rgb = hsv_convert(hue) #convert hue float to rgb values
            for point in range(360): #set rgb values to each pixel
                led_colour[point] = rgb
            client.put_pixels(led_colour) #print pixels to emulator
        arduino.close() #close arduino connection

class Animation_5(StartStopAnimation):
    """creates an animation where the user has to move their car to dodge incoming bot cars"""
    def run(self):
        pop_up_game()
        led_colour=[(0,0,0)]*360 #set blank screen
        global user_car #make variable global
        user_car = [(2,47), (2,48), (2,49), (3,47), (3,48), (3,49)] #define initial position for user_car
        count = 1
        bot_car_count = 0
        bot_cars = [] #start game with no bot cars
        s_count = 100
        speed = 5 #set initial speed of bot_cars
        while self._running:
            client.put_pixels(led_colour)
            led_colour = 360 * [(0,0,0)]
            #generate a new bot car every 8 places moved by the bot cars
            if bot_car_count % 800 == 0:
                bot_cars.append(generate_bot_car())
            #assign pixels of bot cars
            for car in bot_cars:
                for z in car:
                    position = z[0]*60+z[1] #calculates pixels for each bot car
                    led_colour[position - 1] = (0,0,0) #clears previous position of bot cars
                    led_colour[position] = (255,0,0) #sets new position of bot cars
            #assign pixels to of user car
            for p in user_car:
                position = p[0]*60+p[1]
                led_colour[position] = (0,0,255)
            client.put_pixels(led_colour)
            #move bot cars every 100 bot_car_count
            if bot_car_count % 100 == 0:
                for car in enumerate(bot_cars): #iterate through all bot_cars
                    if car[1][0][1] < 59: #check if bot_car has reached the end of the led strip
                        for c in enumerate(car[1]): #iterates through all bot_car tuples 
                            #if user car collides with bot car print game over message to emulator
                            if c[1] in user_car: #checks if any bot car_tuples match user_car tuples
                                while True:
                                    for x in range(360):
                                        rgb = hsv_convert(x)
                                        client.put_pixels([rgb]*360)
                                        if not self._running: break
                                        time.sleep(0.01)
                                    print_letters([g,a,m,e],52,235,55)
                                    if not self._running: break
                                    time.sleep(1)
                                    print_letters([o,v,e,r],155,52,235)
                                    if not self._running: break
                                    time.sleep(1)
                            else:
                                bot_cars[car[0]][c[0]] = (c[1][0],c[1][1]+1) #moves bot cars forward one pixel if there is no collision
                    else:
                        bot_cars.remove(car[1]) #removes bot car from bot_cars list once it reaches the end of the led strip
            bot_car_count += speed
            if count % 5000 == 0: speed += 5 #decrease time it takes for bot cars to move every 50 sec
            count +=1
            time.sleep(0.01) #response time to check for any imput

class Animation_6(StartStopAnimation):
    """creates outro animation thanking the user"""
    def run(self):
        led_colour=[(0,0,0)]*360 #set blank screen
        while self._running:
            for x in range(0, 360, 3): #increment hue in 3s
                rgb = hsv_convert(x) #get rgb values from hue
                led_colour = [rgb]*360 #assign rgb colours
                client.put_pixels(led_colour) #print rgb colours to emulator
                if not self._running: break
                time.sleep(0.01)
            for x in range(3):
                led_colour = [(0,0,0)]*360 #set blank screen
                client.put_pixels(led_colour)
                if not self._running: break
                time.sleep(0.5)
                print_letters([t,h,a,n,k,space,y,o,u],255,255,255) #prints 'thank you' to emulator
                if not self._running: break
                time.sleep(1)
            if not self._running: break
            pixl = 0
            #fill screen with green from top left and bottom right
            while pixl<180: #meet halfway
                led_colour[pixl] = (0,255,0) #turn each pixel green one by one from pixel 0
                led_colour[359-pixl] = (0,255,0) #turn each pixel green one by one from pixel 359
                client.put_pixels(led_colour)
                if not self._running: break
                time.sleep(0.01)
                pixl += 1 #increment pixel count

#assign animation objects to variables    
animation_1 = Animation_1()
animation_2 = Animation_2()
animation_3 = Animation_3()
animation_4 = Animation_4()
animation_5 = Animation_5()
animation_6 = Animation_6()

def click(number): 
    #call on() method on all animations
    animation_1.on()
    animation_2.on()
    animation_3.on()
    animation_4.on()
    animation_5.on()
    animation_6.on()
    animation_choice(number) #start animation_*number*

def pop_up_name():
    global pop #make variable global
    pop = Toplevel(window) #make a popup window open above main window
    #set popup config
    pop.title("Enter name")
    pop.geometry("250x150")
    pop.config(bg = "black")
    pop_label = Label(pop, text = "Please enter your name", bg = "black", fg = "white") #add label widget
    pop_label.pack(pady = 10)
    global input_text #make variable global
    input_text = Text(pop, height = 1, width = 20) #make text box widget
    input_text.pack(pady = 10)
    pop_button = Button(pop, text = "SUBMIT", width = 10, command = lambda: start_new_thread(click,2)) #make button widget which starts a new thread with animation 2
    pop_button.pack(pady = 10)

def pop_up_game(): #creates a pop up window 
    global pop
    #configuration for pop up window
    pop = Toplevel(window) 
    pop.title("Enter command")
    pop.geometry("250x150")
    pop.config(bg = "black")
    pop_label = Label(pop, text = "Enter command here:", bg = "black", fg = "white") #creates a label widget
    pop_label.pack(pady = 10)
    input_command = Text(pop, height = 1, width = 20) #creates a text box
    input_command.bind("<Key>", check_input) #constantly checks the input in the text box
    input_command.pack(pady = 10)

def check_input(event): #checks the input in the text box in the pop up window
    if event.char.lower() == 'w': #checks if input i 'w'
        if user_car[0][0] > 0: #checks if user car is at the top of the emulator
            for a in enumerate(user_car):
                user_car[a[0]] = (a[1][0] - 1, a[1][1]) #moves the user car up
    elif event.char.lower() == 's':
        if user_car[0][0] < 4: #checks if user car is at the bottom of the emulator
            for a in enumerate(user_car):
                user_car[a[0]] = (a[1][0] + 1, a[1][1]) #moves the user car down
    else:
        pass

def stop_animation(): #terminates all animations
    #call terminate method on all objects
    animation_1.terminate()
    animation_2.terminate()
    animation_3.terminate()
    animation_4.terminate()
    animation_5.terminate()
    animation_6.terminate()

def generate_bot_car(): #generates bot car in random lane
    n = randrange(4) #determines which lane the top of the car will be on
    bot_car = [(n,3), (n,2), (n,1), (n+1,3), (n+1,2), (n+1,1)] #sets bot car on respective lanes at left hand side of the emulator
    return bot_car

def hsv_convert(hue): #converts hue to rbg counterpart
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
            pixel = 60*point[0] + point[1] + n #gets pixel location from tuple
            led_colour[pixel] = (r,g,b) #assigns r,g,b arguments to designated pixels
        n+=6 #sets width of each letter to 6 pixels
    client.put_pixels(led_colour) #prints LED pixels to emulator

def draw_undreline(colour,sleep_time): #function to draw an underline on the bottom line of the emulator
    led = 60*5 #used to ignore the first 5 lines
    while led < 60*6:
        led_colour[led] = colour #each pixel in line 6 is chosen
        client.put_pixels(led_colour) #colour is sent to the pixel
        if sleep_time > 0: 
            time.sleep(sleep_time) #sleep for time inserted as argument
        led +=1 #increase pixel number

def start_new_thread(func, *args): #generates a new thread with a function and its parameters as arguments
    global nthrd #set global variable
    if not args: #do this if no arguments are passed for function parameter
        globals()['%sthrd' % nthrd] = threading.Thread(target = func).start() #start thread with function
    else: #do this if arguments are passed for function parameter
        globals()['%sthrd' % nthrd] = threading.Thread(target = lambda: func(args[0])).start() #start thread with function and arguments
    nthrd += 1


def animation_choice(number): #starts chosen animation by calling .run() method
    match number:
        case 1: #atuhor introduction
            animation_1.run()

        case 2: #prints user's name
            animation_2.run()

        case 3: #creates a rain effect
            animation_3.run()
                
        case 4: #arduino potentiometer controled led hue
            animation_4.run()

        case 5: #play car hame
            animation_5.run()

        case 6: #author's outro
            animation_6.run()

        case _: #show error popup if anything other than numbers 1-5 are chosen
            tkinter.messagebox.showerror(title = "Error", message = "Option not recognised") 

client = opc.Client('localhost:7890') #connects code to LED emulator
window = Tk()
window.title("LED animations") #sets title of the window
window.configure(background = "black") #set background colour of window to black
Label (window, text = "Which animation would you like to see?", bg = "black", fg = "white", font = "none 12") .pack(pady = 5) #create label widget at the top of window
#create button widgets for every animation using start_new_thread() function
button1 = Button(window, text = "1. Author's intro", width = 30, command = lambda: start_new_thread(click,1)) 
button1.pack(pady = 5)
button2 = Button(window, text = "2. Print your name", width = 30, command = lambda: start_new_thread(pop_up_name()))
button2.pack(pady = 5)
button3 = Button(window, text = "3. Rain effect", width = 30, command = lambda: start_new_thread(click,3))
button3.pack(pady = 5)
button4 = Button(window, text = "4. Potentiometer hue control", width = 30, command = lambda: start_new_thread(click,4))
button4.pack(pady = 5)
button5 = Button(window, text = "5. Car game", width = 30, command = lambda: start_new_thread(click,5))
button5.pack(pady = 5)
button6 = Button(window, text = "6. Outro", width = 30, command = lambda: start_new_thread(click,6))
button6.pack(pady = 5)
#creates button widget for button to stop animation
button7 = Button(window, text = "Stop animation", fg = "red", width = 35, command = lambda: start_new_thread(stop_animation()))
button7.pack(pady = 5)
nthrd = 0 #sets thread count to 0
led_colour=[(0,0,0)]*360 #sets a blank screen
_s = 1.0 #used to set maximum colour to hsv chart
_v = 1.0 #used to set maximum brightness to hsv chart

window.mainloop() #loops tkinter to responsive