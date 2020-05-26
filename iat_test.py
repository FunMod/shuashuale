import os


def listen():
    os.system("./iat_sample ")
    try:
        with open("text.txt", "r") as file:
            result_text = file.read()
        print("you said: ", result_text)
        return result_text
    except KeyError:
        print("KeyError")


def rec():
    os.system("arecord -d 3 -r 16000 -c 1 -t wav -f S16_LE temp.wav")


rec()
listen()
