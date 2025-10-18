from microbit import *
import radio

radio.config(channel=7, group=1)
radio.on()

steps = 0
previous_magnitude = 0
THRESHOLD = 1500

display.show(Image.WALKING)

while True:
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    
    magnitude = (x**2 + y**2 + z**2) ** 0.5

    if (magnitude - previous_magnitude) > THRESHOLD:
        steps += 1
        display.show(str(steps % 10))
    
    previous_magnitude = magnitude

    message = radio.receive()
    if message == "SendSteps":
        radio.send("Steps:" + str(steps))
        display.show(Image.ARROW_N)
        sleep(500)
        display.show(Image.WALKING)

    sleep(100)
