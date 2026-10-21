from microbit import *
import time
import machine
import radio

distance = 0

radio.on()
radio.config(group=128, power=7)

heartbeat_time = running_time()
global heartbeat_led
heartbeat_led = 9

# Serves as a visual status indicator showing the micro:bit is running and active.
@run_every(s=1)
def heartbeat():
    global heartbeat_led
    heartbeat_led = 9 - heartbeat_led
    display.set_pixel(2, 4, heartbeat_led)


while True:
    # Triggering the Ultrasonic Pulse
    # pin0 acts as the Trig (Trigger) pin on the ultrasonic sensor.
    pin0.write_digital(0)
    time.sleep_us(2)
    pin0.write_digital(1)
    # It sends a 10-microsecond high pulse to signal the sensor to emit
    # an ultrasonic sound wave burst.
    time.sleep_us(10)
    pin0.write_digital(0)
    # Reading the Echo Pulse & Calculating Distance
    pulse_time = machine.time_pulse_us(pin1, 50000)
    if pulse_time < 0:
        pass
    else:
        times = pulse_time/1000000 # Convert microseconds to seconds
        velocity = 343 # Speed of sound in air (343 m/s)
        distance = 100 * times * velocity / 2 # Convert to centimeters (divide by 2 for round-trip)
    if distance > 30:
        # Transmits "o" (Open / Clear) if an object is further than 30 cm.
        radio.send("o")
    else:
        # Transmits "c" (Close / Near) if an object is within 30 cm.
        radio.send("c")
    time.sleep_ms(100)
