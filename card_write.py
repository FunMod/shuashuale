# 写卡程序
import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
try:
    while True:
        print("请放卡片")
        text_input = input('输入内容：')
        reader.write(text_input)
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id, text))
        sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
    exit(0)
