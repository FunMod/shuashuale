# -*- coding:UTF-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN, pull_up_dwon=GPIO.PUD_DOWN)
GPIO.setup(25, GPIO.OUT)

ledStatus = True


def my_callback(channel):
    print("button pressed!")
    global ledStatus
    ledStatus = not ledStatus
    if ledStatus:
        GPIO.output(25, GPIO.HIGH)
        pass
    else:
        GPIO.output(25, GPIO.LOW)
        pass
    pass


GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback)

while True:
    try:
        print("I'm working...")
        time.sleep(5)
        pass
    except KeyboardInterrupt:
        break
        pass
    pass

GPIO.cleanup()
