# 读卡程序
import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
try:
    while True:
        reader = SimpleMFRC522()
        print("请放卡片")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id, text))
        sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
    exit(0)
