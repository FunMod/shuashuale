import RPi.GPIO as GPIO
from card_main import Card
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

GPIO.setmode(GPIO.BCM)

GPIO.setup(38, GPIO.IN, pull_up_dwon=GPIO.PUD_DOWN)
GPIO.setup(39, GPIO.OUT)


def my_callback(channel):
    id, text = reader.read()
    Card().run


GPIO.add_event_detect(38, GPIO.RISING, callback=my_callback, bouncetime=200)

while True:
    try:
        Card().run()
    except KeyboardInterrupt:
        break
        pass
    pass

GPIO.cleanup()
