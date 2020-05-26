"""
刷刷乐项目 v2.0
by 电子12组项目开发
改用面向对象的方法编写代码，逻辑清楚，便于后期维护
功能介绍：
    （1）卡片按照三位数字编号加上操作指令编号的格式储存信息，其中三位数字编号用于寻找数据库中对应的内容，操作指令用于选择模式、返回主菜单
        例如：666read就可以选择语音朗读模式并且找到数据库中666对应的文件，555action就可以选择互动模式，然后执行555编号对应的内容
    （2）执行程序后的基本流程如下：
        以使用666read卡片为例：刷卡666read->选择学习模式->刷卡666read->播放编号666对应的儿歌->继续刷卡333read->播放333编号对应的儿歌
        ->继续刷卡555action->判断为非read操作卡则返回主菜单->继续刷555action->选择互动（游戏）模式->继续刷action卡即可选择游戏、、、
    （3）如果刷的卡不在以上规定范围内则提示重新刷卡
    （4）其他内容有待完善、、、、、、
数据库内容：id-主键 类型int 自增（不需要调用）
       name 类型varchar 记录卡片标签（以下对应卡片标签）
       con 类型varchar 记录卡片详细内容（对应本地语音包的储存位置）
"""

from mfrc522 import SimpleMFRC522
# from time import sleep
import pymysql
import os
from gpiozero import Button
import RPi.GPIO as GPIO
reader = SimpleMFRC522()


class Card(object):  # 定义Card类
    def __init__(self):
        self.conn = pymysql.connect(  # 连接MySQL数据库
            host='localhost',
            port=3306,
            database='card_test',
            user='root',
            password='zzu2017',
            charset='utf8')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        GPIO.cleanup()
        print('异常退出！')

    def id_get(self, name):  # 获取name内容（互动标签为action，学习标签为read）
        sql = "select * from card_01 where name = %s"
        self.cursor.execute(sql, name)
        tex = self.cursor.fetchone()
        return tex[1]

    def con_get(self, con):  # 获取con内容（标签对应的本地文件）
        sql = "select * from card_01 where name = %s"
        self.cursor.execute(sql, con)
        con = self.cursor.fetchone()
        return con[2]

    def read(self, text):  # 语音输出方法
        cmd = "mplayer " + text
        os.system(cmd)

    def tts(self, text):  # TTS文本合成语音方法
        cmd = "tts_sample " + text
        os.system(cmd)

    def Butt(self):  # 按钮方法
        button = Button(2)

        while True:
            if button.is_pressed:
                print("Button is pressed")
            else:
                print("Button is not pressed")

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

    def run(self):  # 执行程序的方法
        # 接受来自NFC的信息并判断下一步操作:选择模式
        while True:
            print('请放卡片：')
            id, text = reader.read()
            if 'action' in self.id_get(text[3:]):  # 判断操作卡片指令是否为互动
                print('已选择互动模式')
                """# 互动模式接收卡片标签中的指令来执行游戏函数
                while True:
                    self.tts('请放卡片')
                    id, text = reader.read()
                    # 接下来判断卡片内容,若为操作指令卡则结束此循环并返回主菜单，若为知识卡，则输出语音
                    if 'read' in self.id_get(text[3:]):
                        self.tts('返回主菜单')
                        break
                    """
                pass
            elif 'read' in self.id_get(text[3:]):  # 判断操作卡片指令是否为朗读
                print('已选择学习模式')
                #  学习模式：刷卡直接输出语音
                """# while True:
                    # self.tts('请放卡片')
                    # id, text = reader.read()
                    # # 接下来判断卡片内容,若为操作指令卡则结束此循环并返回主菜单，若为知识卡，则输出语音
                    # if 'action' in self.id_get(text[3:]):
                    #     self.tts('返回主菜单')
                    #     break
                    # else:
                    #     self.read(self.con_get(text[0:3]))
                    # """
                self.read(self.con_get(text[0:3]))

            else:
                self.tts('请重新放卡')  # 不属于以上两种情况则语音提示重新选择操作模式


def main():  # 由Card类定义主函数对象
    card = Card()
    card.run()  # 调用run方法


if __name__ == '__main__':  # 这里执行主程序main
    while True:  # 循环执行主函数。出现错误重新运行
        try:
            main()
        except BaseException:  # 捕获异常退出
            pass
