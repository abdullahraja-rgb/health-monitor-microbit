from microbit import *
import radio
import time

radio.config(channel=7, group=1)
radio.on()
uart.init(baudrate=115200)

def request_data(device):
    if device == "Temp":
        radio.send("SendTemp")
    elif device == "Steps":
        radio.send("SendSteps")

display.scroll("Server Ready")

while True:
    request_data("Temp")
    sleep(1000)
    message_temp = radio.receive()
    
    request_data("Steps")
    sleep(1000)
    message_steps = radio.receive()

    if message_temp and message_steps:
        display.show(Image.YES)
        try:
            temp_value = str(message_temp)
            steps_value = str(message_steps)
            combined_data = "{} {}".format(temp_value, steps_value)
            uart.write(combined_data + '\n')
        except ValueError:
            display.show(Image.NO)
    else:
        display.show(Image.ASLEEP)

    sleep(2000)
