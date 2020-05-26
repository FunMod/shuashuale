"""
添加开关机按钮
程序要保证开机自动运行，并保持运行，如果出现故障应具备自动重新运行的能力
数据库内容：id-主键 自增（不需要调用）
       name -varchar类型记录卡片标签（以下对应卡片标签）
       con varchar 记录卡片详细内容（对应本地语音包的储存位置）
运行主程序后，首先需要判断用户选择的工作模式：
操作指令卡：（1）名词模式（2）游戏模式
    名词卡片：直接根据卡片储存的name标签找到数据库中对应的文件位置并语音输出，执行结束后等待下一张名词卡片或行为选择卡片；
    行为卡片：根据行为卡片储存的name标签调用对应的游戏函数，执行结束后等待下一张行为卡片或模式选择卡片；
操作逻辑，所有的卡既可以用来选择模式又可以播放内容，卡片中同时记录操作模式信息和要播放内容，这样就不用独立出来几张用来选模式的卡了
"""
# 首先导入开发所需要的模块
from mfrc522 import SimpleMFRC522
# from time import sleep
import pymysql
import os
from gpiozero import Button
import RPi.GPIO as GPIO
reader = SimpleMFRC522()
conn = pymysql.connect(  # 连接MySQL数据库
    host='localhost',
    port=3306,
    database='card_test',
    user='root',
    password='zzu2017',
    charset='utf8')
cursor = conn.cursor()


def id_get(name):  # 获取name内容（互动标签为action，学习标签为read）
    sql = "select * from card_01 where name = %s"
    cursor.execute(sql, name)
    tex = cursor.fetchone()
    return tex[1]


def con_get(con):  # 获取con内容（标签对应的本地文件）
    sql = "select * from card_01 where name = %s"
    cursor.execute(sql, con)
    con = cursor.fetchone()
    return con[2]


def read(text):  # 语音输出函数
    cmd = "mplayer " + text
    os.system(cmd)


def tts(text):  # TTS文本合成语音
    cmd = "tts_sample " + text
    os.system(cmd)


def Butt():  # 按钮函数
    button = Button(2)

    while True:
        if button.is_pressed:
            print("Button is pressed")
        else:
            print("Button is not pressed")


# def plus():  # 定义加法函数
#     id, text = reader.read()
#     read(text)
#     a = int(text)
#     id, text = reader.read()
#     read(text)
#     b = int(text)
#     tts('%d+%d=%d' % (a, b, a+b))


def main():
    # 接受来自NFC的信息并判断下一步操作:选择模式
    while True:
        tts('请放卡片：')
        id, text = reader.read()
        if 'action' in id_get(text[3:]):  # 判断操作卡片指令是否为互动
            tts('已选择互动模式')
            # 互动模式接收卡片标签中的指令来执行游戏函数
            while True:
                tts('请放卡片')
                id, text = reader.read()
                # 接下来判断卡片内容,若为操作指令卡则结束此循环并返回主菜单，若为知识卡，则输出语音
                if 'read' in id_get(text[3:]):
                    tts('返回主菜单')
                    break
        elif 'read' in id_get(text[3:]):  # 判断操作卡片指令是否为朗读
            tts('已选择学习模式')
            #  学习模式：刷卡直接输出语音
            while True:
                tts('请放卡片')
                id, text = reader.read()
                # 接下来判断卡片内容,若为操作指令卡则结束此循环并返回主菜单，若为知识卡，则输出语音
                if 'action' in id_get(text[3:]):
                    tts('返回主菜单')
                    break
                else:
                    read(con_get(text[0:3]))
        else:
            tts('请重新选择操作模式')  # 不属于以上两种情况则语音提示重新选择操作模式
            pass


if __name__ == '__main__':  # 这里执行主程序main
    try:
        main()
    except BaseException:  # 捕获异常退出
        # 关闭数据库和GPIO端口
        cursor.close()
        conn.close()
        GPIO.cleanup()
        exit(0)
