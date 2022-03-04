# Fadecandy_2400

## Assignment

Assignment.py file can be ran in python 3.10 using IDLE and will open a tkinter window with 6 animation buttons and a stop animation button when ran

The LED simulator must be running or have physical LEDs connected to show the animations

Pressing an animation button will play the animation and pressing the 'Stop animation' button will stop all animation

###### Animation 1 - Author's intro

First button prints to the LEDs an automatic animation with an introduction from the author

###### Animation 2 - Print your name

Second button brings up a pop up window prompting the user to write their name (max 9 A-Z characters) in the text box which must be submitted using the 'SUBMIT' button to start the animation. Once submitted, the pop up can be closed. The animation will print a message which includes the inputted name to the LEDs to welcome the user.

###### Animation 3 - Rain effect

The third button will print an automatic animation to the LEDs in which blue LEDs will light up at a random points on the top strip and fall down with a trail or random length between 3 and 5 LEDs

###### Animation 4 - Potentiometer hue control

The fourth button will get input from an Arduino using Serial communication on port COM3. This can be changed on line 118 in Animation_4 class from
```
        arduino = serial.Serial('COM3', 9600)
```
to 
```
        arduino = serial.Serial('COMn', 9600)
```
where COMn is the port the arduino is connected to. \Fadecandy_2400-main\potentiometer_hsv\potentiometer_hsv.ino file can be used on an arduino uno to get reading from the potentiometer on pin A0 and print it to serial to be used by python. The potentiometer can be rotated to shift through 360 hues on the LEDs.

###### Animation 5 - Car gme

The fith button will open a pop up window and start an interactive car game animation on the LEDs. The 'w' and 's' keys can be used to move the user car on the right up and down respectively. The text box in the pop up window must be selected for the 'w' and 's' commands to move the car. The purpose of the game is to dodge incoming cars by moving out of the way. If the user can collides with any incoming bot car from any angle, the game stops and a game over message is printed to the LEDs.

###### Animation 6 - Outro

Sixth button prints to the LEDs an automatic animation with a thank you message from the author

###### Stop animation

Seventh button stops all animations from running

## Simulator

The simulator provided has 360 leds arranged in a grid pattern of 6 rows with 60 leds each.

###### Basic commands
```
opc.Client() - sets up a client object that will establish communication between Python and a fadecandy server.
Required argument: an IP or localhost with correct port for the server.
```

```
.put_pixels(list) - places a list of tuples with rgb values to the fadecandy server to be displayed.
Format: [(R_value, G_value, B_value)]. Each tuple element in the list represents a single led.
```

There are a few more methods for ensuring connection and disconnect procedures, but they will not be needed with the simulator.

###### Notes

To connect to the simulator, use localhost with port 7890 when setting up your fadecandy instance in Python: 
```
client = opc.Client('localhost:7890')
```

When not using a loop, perform .put_pixels() twice to avoid interpolation issues:
```
client.put_pixels(list)
client.put_pixels(list)
```

It's highly recommended to perform any colour fading in an HSV space as opposed to RGB. Refer to the '4_hsv_rainbow.py' and 'hsv_rainbow_rolling.py' examples. Keep Value (saturation) max to begin with, play with the value for more pastel, washed out colours.  

## Other files

- 60by6.jpg - use this as a template to easily plan templates and check led numbers.
- colour spaces.pdf - basic information on the difference between RGB and HSV. 
- Fadecandy exercises.pdf - some simple tasks to get you started.
