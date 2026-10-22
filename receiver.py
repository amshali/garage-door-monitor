# Microbit Garage Door Monitor - Receiver
from microbit import *
import radio

radio.config(group=128, power=7)
radio.on()

door_state = "happy"
display.show(Image.HAPPY)

last_msg_time = running_time()
last_blink_time = running_time()
blink_intensity = 0

# Custom image for an open garage door
door_open_img = Image('99999:'
                      '99999:'
                      '90009:'
                      '90009:'
                      '90009')

while True:
    # Read any available message from the radio
    message = radio.receive()
    current_time = running_time()
    
    # Update state based on the message received
    if message == "o":
        last_msg_time = current_time
        if door_state != "open":
            display.show(door_open_img)
            door_state = "open"
            
    elif message == "c":
        last_msg_time = current_time
        if door_state != "closed":
            display.clear()
            door_state = "closed"
            
    # If no message for 8 seconds (8000 milliseconds), show disconnected (sad)
    elif current_time - last_msg_time > 8000:
        if door_state != "disconnected":
            display.show(Image.SAD)
            door_state = "disconnected"

    # Toggle the heartbeat pixel every 1 seconds (1000 milliseconds)
    if current_time - last_blink_time > 1000:
        blink_intensity = 7 if blink_intensity == 0 else 0
        last_blink_time = current_time
        
    # Draw the heartbeat pixel in the center (x=2, y=2)
    display.set_pixel(2, 2, blink_intensity)
    
    # Short sleep to prevent busy waiting
    sleep(100)
