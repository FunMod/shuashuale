import pymysql
from time import sleep
import RPi.GPIO as GPIO
import os
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()


def main():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        database='card_test',
        user='root',
        password='zzu2017',
        charset='utf8')
    cursor = conn.cursor()
    id, text = reader.read()
    print('卡号：%s,内容：%s' % (id, text))
    sql = "select * from card_01 where name = %s" % (text,)
    cursor.execute(sql)
    text = cursor.fetchone()
    print(text[2])
    cmd = "tts_sample " + text[2]
    os.system(cmd)
    sleep(5)
    cursor.close()
    conn.close()
    GPIO.cleanup()


if __name__ == '__main__':
    main()
    exit(0)
