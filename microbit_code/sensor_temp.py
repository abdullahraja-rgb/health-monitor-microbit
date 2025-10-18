from microbit import *
import radio

radio.config(channel=7, group=1)
radio.on()

display.show(Image.HEART)

while True:
    message = radio.receive()
    
    if message == "SendTemp":
        temperature_data = temperature()
        radio.send("Temp:" + str(temperature_data))
        display.show(Image.ARROW_N)
        sleep(500)
        display.show(Image.HEART)

    sleep(100)
