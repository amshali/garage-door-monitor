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

@run_every(s=1)
def heartbeat():
    global heartbeat_led
    heartbeat_led = 9 - heartbeat_led
    display.set_pixel(2, 4, heartbeat_led)


while True:
    pin0.write_digital(0)
    time.sleep_us(2)
    pin0.write_digital(1)
    time.sleep_us(10)
    pin0.write_digital(0)
    pulse_time = machine.time_pulse_us(pin1, 50000)
    if pulse_time < 0:
        pass
    else:
        times = pulse_time/1000000
        velocity = 343
        distance = 100 * times * velocity / 2
    if distance > 30:
        radio.send("o")
    else:
        radio.send("c")
    time.sleep_ms(100)

